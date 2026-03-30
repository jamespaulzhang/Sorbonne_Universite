import pandas as pd
import math
from gurobipy import Model, GRB, quicksum

# =====================================================
# 1. Données : prix des coureurs
# =====================================================
prices_df = pd.read_csv("valeurs.csv")
prices = prices_df.set_index("Rider")["poids"].to_dict()

R = list(prices.keys())
T = [0, 1, 2]                     # périodes
initial_budget = 140
team_size = 14

# Prix avec majoration de 10 % pour les entrants en cours de Tour
aug_price = {r: math.ceil(1.1 * prices[r]) for r in R}

# =====================================================
# 2. Fonction de période (selon le numéro d'étape)
# =====================================================
def period(i):
    if i <= 10:
        return 0
    elif i <= 15:
        return 1
    else:
        return 2

# =====================================================
# 3. Points par étape (classement + maillots)
# =====================================================
points_stage = {
    1: 30, 2: 20, 3: 18, 4: 17, 5: 16,
    6: 15, 7: 14, 8: 13, 9: 12, 10: 11,
    11: 10, 12: 9, 13: 8, 14: 7, 15: 6,
    16: 5, 17: 4, 18: 3, 19: 2, 20: 1
}

# Dictionnaire points[(coureur, étape)] = score
points = {}

# 3.1 Points des classements d'étape
for i in range(1, 22):
    stage = pd.read_csv(f"stage_{i:02d}_2025.csv")
    for rank, rider in enumerate(stage["Rider"], start=1):
        points[(rider, i)] = points_stage.get(rank, 0)

# 3.2 Points des maillots par étape
maillots = pd.read_csv("maillots.csv")
for idx, row in maillots.iterrows():
    etape = idx + 1
    for col, pts in zip(["Jaune", "Vert", "Pois", "Blanc", "Combatif1", "Combatif2"],
                         [8, 5, 5, 5, 5, 5]):
        if pd.notna(row[col]):
            rider = row[col]
            points[(rider, etape)] = points.get((rider, etape), 0) + pts

# 3.3 Points des bonus finaux (après la dernière étape)
final = pd.read_csv("final.csv")
E_final = 22
for _, row in final.iterrows():
    rider = row["Rider"]
    bonus = sum(row[col] for col in ["jaune", "vert", "pois", "jeune", "comba"]
                if not pd.isna(row[col]))
    points[(rider, E_final)] = bonus

# ========== MODIFICATION MANUELLE (pour test) ==========
# Donner 3000 points à Bol Cees sur la 1ère étape
# points["Bol Cees", 1] = 3000
# Mettre son prix à 0 pour éliminer la contrainte budgétaire
# prices["Bol Cees"] = 1
# aug_price["Bol Cees"] = math.ceil(1.1 * 0)  # reste 0

# =====================================================
# 4. Listes d'abandons
# =====================================================
abandons_10 = [
    "Ganna Filippo", "Bissegger Stefan", "Philipsen Jasper",
    "Jeannière Emilien", "De Buyst Jasper", "Cattaneo Mattia",
    "Haig Jack", "Dunbar Eddie", "Almeida Jo",
    "Berg Marijn", "Zimmermann Georg", "Wærenskjold Søren"
]

abandons_15 = abandons_10 + [
    "Bol Cees", "Evenepoel Remco", "Skjelmose Mattias",
    "Coquard Bryan", "Cras Steff", "Van Eetvelt Lennert",
    "Poel Mathieu"
]

# =====================================================
# 5. Modèle d'optimisation
# =====================================================
m = Model("Fantasy_TDF")
m.Params.OutputFlag = 0
m.Params.MIPFocus = 2          # accent sur l'optimalité
m.Params.MIPGap = 1e-6         # optimalité stricte
m.Params.TimeLimit = 600       # temps maximal de calcul
m.Params.Heuristics = 0.5      # renforcer les heuristiques

# Variables binaires : présence du coureur à chaque période
x = m.addVars(R, T, vtype=GRB.BINARY, name="x")

# Variables continues auxiliaires pour les achats/ventes
buy = m.addVars(R, T, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="buy")
sell = m.addVars(R, T, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="sell")

# Budget à chaque période
budget = m.addVars(T, lb=0, name="budget")

# Objectif : somme des points sur toutes les étapes + bonus finaux
m.setObjective(
    quicksum(points.get((r, e), 0) * x[r, period(e)] for r in R for e in range(1, 22)) +
    quicksum(points.get((r, E_final), 0) * x[r, 2] for r in R),
    GRB.MAXIMIZE
)

# =====================================================
# 6. Contraintes
# =====================================================
# Taille de l'équipe à chaque période
for t in T:
    m.addConstr(quicksum(x[r, t] for r in R) == team_size)

# Dynamique d'équipe : buy - sell = variation de présence
for r in R:
    for t in T[1:]:  # t = 1,2
        m.addConstr(buy[r, t] - sell[r, t] == x[r, t] - x[r, t-1])
        # Interdiction d'acheter et vendre le même coureur dans la même période
        m.addConstr(buy[r, t] + sell[r, t] <= 1)

# Budget initial
m.addConstr(budget[0] == initial_budget - quicksum(prices[r] * x[r, 0] for r in R))

# Budget dynamique (avec ventes et achats)
for t in T[1:]:
    m.addConstr(
        budget[t] == budget[t-1]
        - quicksum(aug_price[r] * buy[r, t] for r in R)
        + quicksum(prices[r] * sell[r, t] for r in R)
    )
    m.addConstr(budget[t] >= 0)

# =====================================================
# 7. Règles des transferts
# =====================================================
# Définition des périodes où un coureur peut être vendu :
#   - Période 1 : seuls les abandons_10 peuvent être vendus
#   - Période 2 : tous les abandons_15 (incluant abandons_10) peuvent être vendus
sell_allowed = {
    1: set(abandons_10),
    2: set(abandons_15)
}

for t in T[1:]:
    for r in R:
        if r not in sell_allowed[t]:
            m.addConstr(sell[r, t] == 0, name=f"no_sell_{r}_{t}")

# Les coureurs abandonneurs ne peuvent pas apparaître en période 1 et 2
for r in abandons_10:
    for t in [1, 2]:
        m.addConstr(x[r, t] == 0, name=f"abandon_{r}_{t}")

for r in set(abandons_15) - set(abandons_10):
    m.addConstr(x[r, 2] == 0, name=f"abandon15_{r}")

# =====================================================
# 8. Debug / Tests
# =====================================================
coeff = sum(points.get(("Ganna Filippo", e), 0) for e in range(1, 22) if period(e) == 0)
print(f"Ganna Filippo period 0 total points: {coeff}")
print(f"Prix de Ganna Filippo : {prices.get('Ganna Filippo', 'Inconnu')}")

print("Nombre de contraintes avant résolution :", m.NumConstrs)

# =====================================================
# 9. Résolution
# =====================================================
m.optimize()

# =====================================================
# 10. Affichage des résultats
# =====================================================
if m.status == GRB.OPTIMAL:
    print("\nScore total :", m.objVal)

    # Afficher la valeur de Ganna pour vérifier
    print("Ganna Filippo en période 0 :", x["Ganna Filippo", 0].X)

    for t in T:
        print(f"\n====== Période {t} ======")
        team = [r for r in R if x[r, t].X > 0.5]

        for r in team:
            print(f"{r:30s} | Prix={prices[r]}")

        if t > 0:
            print("\n--- Achats ---")
            for r in R:
                if buy[r, t].X > 0.5:
                    print(f"+ {r} (coût {aug_price[r]})")

            print("\n--- Ventes ---")
            for r in R:
                if sell[r, t].X > 0.5:
                    print(f"- {r} (gain {prices[r]})")

        print("Budget restant :", budget[t].X)

else:
    print("Problème non résolu à l'optimalité. Status:", m.status)
    if m.status == GRB.INFEASIBLE:
        print("Le modèle est infaisable. Calcul de l'IIS...")
        m.computeIIS()
        m.write("infeasible.ilp")
        print("IIS écrit dans infeasible.ilp")