import pandas as pd
from gurobipy import Model, GRB, quicksum

# ----------------------------
# 1. Lire les prix des coureurs
# ----------------------------
prices = pd.read_csv("valeurs.csv")
prices = prices.set_index("Rider")["poids"].to_dict()

# ----------------------------
# 2. Initialiser le tableau des scores
# ----------------------------
scores = {r: 0 for r in prices.keys()}

# ----------------------------
# 3. Points pour le classement par étape
# ----------------------------
points_stage = {
    1: 30, 2: 20, 3: 18, 4: 17, 5: 16,
    6: 15, 7: 14, 8: 13, 9: 12, 10: 11,
    11: 10, 12: 9, 13: 8, 14: 7, 15: 6,
    16: 5, 17: 4, 18: 3, 19: 2, 20: 1
}

for i in range(1, 22):
    stage = pd.read_csv(f"stage_{i:02d}_2025.csv")
    for rank, rider in enumerate(stage["Rider"], start=1):
        if rider in scores:
            scores[rider] += points_stage.get(rank, 0)

# ----------------------------
# 4. Maillots (par étape)
# ----------------------------
maillots = pd.read_csv("maillots.csv")

for _, row in maillots.iterrows():
    for col, pts in zip(["Jaune","Vert","Pois","Blanc","Combatif1","Combatif2"], [8,5,5,5,5,5]):
        if pd.notna(row[col]):
            scores[row[col]] += pts

# ----------------------------
# 5. Bonus final
# ----------------------------
final = pd.read_csv("final.csv")

for _, row in final.iterrows():
    rider = row["Rider"]
    if rider not in scores:
        continue
    for col in ["jaune", "vert", "pois", "jeune", "comba"]:
        if not pd.isna(row[col]):
            scores[rider] += row[col]

# ----------------------------
# 6. Modèle ILP avec Gurobi
# ----------------------------
m = Model("Fantasy_Cycling")
m.Params.OutputFlag = 0  # désactiver les logs

x = {r: m.addVar(vtype=GRB.BINARY, name=f"x_{r}") for r in scores}

# Fonction objectif
m.setObjective(quicksum(scores[r]*x[r] for r in scores), GRB.MAXIMIZE)

# Contrainte : exactement 14 coureurs
m.addConstr(quicksum(x[r] for r in scores) == 14)

# Contrainte : budget ≤ 140
m.addConstr(quicksum(prices[r]*x[r] for r in scores) <= 140)

# Résolution
m.optimize()

# ----------------------------
# 7. Affichage du résultat
# ----------------------------
selected = [r for r in scores if x[r].X > 0.5]

total_score = sum(scores[r] for r in selected)
total_cost = sum(prices[r] for r in selected)

print("Composition optimale :")
for r in selected:
    print(f"{r:30s} | Prix={prices[r]:2d} | Score={scores[r]}")

print("\nCoût total :", total_cost)
print("Score total :", total_score)
