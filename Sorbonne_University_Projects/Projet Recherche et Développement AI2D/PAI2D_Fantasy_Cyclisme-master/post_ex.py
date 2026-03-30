import pulp
import pandas as pd
import math
import trait_donnees

points, E_final = trait_donnees.data_tour_de_france()
#points, E_final = data_tour_de_france()


def period(e):
    if e <= 10:
        return 0
    elif e <= 15:
        return 10
    else:
        return 15


# Le solveur CBC
print(pulp.listSolvers(onlyAvailable=True))

# Le prob est à Maximiser
prob = pulp.LpProblem("Z", pulp.LpMaximize)


# Les constantes du problèmes
# Le Budget initial
B = 140
# Les périodes
T = [0, 10, 15] # 3 périodes (0 est pour l'équipe initiale)
# Les événements
E = list(range(1, 22)) # 21 événements
# Les coureurs
P = ['Philipsen Jasper', 'Groves Kaden', 'Poel Mathieu', 'Rickaert Jonas', 'Meurisse Xandro', 'Vermeersch Gianni', 'Verstrynge Emiel', 'Dillier Silvan', 'Vauquelin Kévin', 'Capiot Amaury', 'Démare Arnaud', 'Venturini Clément', 'Le Berre Mathis', 'Rodr Cristi', 'Garc Pierna Ra', 'Costiou Ewen', 'Stannard Robert', 'Bauhaus Phil', 'Buitrago Santiago', 'Haig Jack', 'Wright Fred', 'Mohori Matej', 'Gradek Kamil', 'Martinez Lenny', 'Touzé Damien', 'Coquard Bryan', 'Buchmann Emanuel', 'Renard Alexis', 'Aranburu Alex', 'Teuns Dylan', 'Izagirre Ion', 'Thomas Benjamin', 'Berthet Clément', 'Paret- Peintre Aurélien', 'Naesen Oliver', 'Gall Felix', 'Tronchon Bastien', 'Scotson Callum', 'Armirail Bruno', 'Bissegger Stefan', 'Sweeny Harry', 'Asgreen Kasper', 'Powless Neilson', 'Healy Ben', 'Valgren Michael', 'Albanese Vincenzo', 'Baudin Alex', 'Berg Marijn', 'Russo Clément', 'Penho Paul', 'Barthe Cyril', 'Madouas Valentin', 'Martin Guillaume', 'Pacher Quentin', 'Grégoire Romain', 'Askey Lewis', 'Watson Samuel', 'Rodr Carlos', 'Swift Connor', 'Thomas Geraint', 'Foss Tobias', 'Arensman Thymen', 'Laurance Axel', 'Ganna Filippo', 'Girmay Biniam', 'Page Hugo', 'Braet Vito', 'Rutsch Jonas', 'Zimmermann Georg', 'Rex Laurenz', 'Sintmaartensdijk Roel', 'Barré Louis', 'Neilands Krists', 'Ackermann Pascal', 'Blackmore Joseph', 'Boivin Guillaume', 'Louvel Matis', 'Stewart Jake', 'Lutsenko Alexey', 'Woods Michael', 'Stuyven Jasper', 'Milan Jonathan', 'Skjelmose Mattias', 'Skuji Toms', 'Theuns Edward', 'Consonni Simone', 'Simmons Quinn', 'Nys Thibau', 'De Lie Arnaud', 'De Buyst Jasper', 'Van Eetvelt Lennert', 'Berckmoes Jenno', 'Van Moer Brent', 'Drizners Jarrad', 'Grignard Sébastien', 'Sep Eduardo', 'Garc Cortina Iv', 'Mas Enric', 'Oliveira Nelson', 'Mühlberger Gregor', 'Rubio Einer', 'Castrillo Pablo', 'Romeo Iv', 'Barta Will', 'Meeus Jordi', 'Poppel Danny', 'Lipowitz Florian', 'Rogli Primo', 'Vlasov Aleksandr', 'Pithie Laurence', 'Moscon Gianni', 'Dijke Mick', 'Merlier Tim', 'Evenepoel Remco', 'Van Wilder Ilan', 'Eenkhoorn Pascal', 'Van Lerberghe Bert', 'Cattaneo Mattia', 'Paret- Peintre Valentin', 'Schachmann Maximilian', 'Mezgec Luka', 'Groenewegen Dylan', 'Reinders Elmar', 'Dunbar Eddie', 'Connor Ben', 'Schmid Mauro', 'Durbridge Luke', 'Plapp Luke', 'Märkl Niklas', 'Bittner Pavel', 'Andresen Tobias Lund', 'Onley Oscar', 'Flynn Sean', 'Barguil Warren', 'Broek Frank', 'Naberman Tim', 'Turgis Anthony', 'Jegat Jordan', 'Gachignard Thomas', 'Cras Steff', 'Delettre Alexandre', 'Jeannière Emilien', 'Burgaudeau Mathieu', 'Vercher Mattéo', 'Jorgenson Matteo', 'Vingegaard Jonas', 'Benoot Tiesj', 'Affini Edoardo', 'Aert Wout', 'Campenaerts Victor', 'Kuss Sepp', 'Yates Simon', 'Trentin Matteo', 'Mayrhofer Marius', 'Haller Marco', 'Dainese Alberto', 'Lienhard Fabian', 'Hirschi Marc', 'Storer Michael', 'Alaphilippe Julian', 'Poga Tadej', 'Wellens Tim', 'Almeida Jo', 'Narv Jhonatan', 'Soler Marc', 'Politt Nils', 'Sivakov Pavel', 'Yates Adam', 'Wærenskjold Søren', 'Fredheim Stian', 'Johannessen Tobias Halland', 'Abrahamsen Jonas', 'Hoelgaard Markus', 'Cort Magnus', 'Leknessund Andreas', 'Johannessen Anders Halland', 'Teunissen Mike', 'Ballerini Davide', 'Tejada Harold', 'Higuita Sergio', 'Champoussin Clément', 'Velasco Simone', 'Fedorov Yevgeniy', 'Bol Cees'] # 184 coureurs
# Les prix de chaque coureurs
c = {
    "Philipsen Jasper": 16,
    "Groves Kaden": 14,
    "Poel Mathieu": 14,
    "Rickaert Jonas": 4,
    "Meurisse Xandro": 6,
    "Vermeersch Gianni": 8,
    "Verstrynge Emiel": 4,
    "Dillier Silvan": 4,
    "Vauquelin Kévin": 10,
    "Capiot Amaury": 7,
    "Démare Arnaud": 10,
    "Venturini Clément": 6,
    "Le Berre Mathis": 5,
    "Rodr Cristi": 7,
    "Garc Pierna Ra": 5,
    "Costiou Ewen": 6,
    "Stannard Robert": 5,
    "Bauhaus Phil": 12,
    "Buitrago Santiago": 12,
    "Haig Jack": 8,
    "Wright Fred": 7,
    "Mohori Matej": 9,
    "Gradek Kamil": 4,
    "Martinez Lenny": 12,
    "Touzé Damien": 4,
    "Coquard Bryan": 10,
    "Buchmann Emanuel": 8,
    "Renard Alexis": 6,
    "Aranburu Alex": 8,
    "Teuns Dylan": 8,
    "Izagirre Ion": 8,
    "Thomas Benjamin": 6,
    "Berthet Clément": 5,
    "Paret- Peintre Aurélien": 8,
    "Naesen Oliver": 6,
    "Gall Felix": 12,
    "Tronchon Bastien": 5,
    "Scotson Callum": 3,
    "Armirail Bruno": 7,
    "Bissegger Stefan": 7,
    "Sweeny Harry": 4,
    "Asgreen Kasper": 9,
    "Powless Neilson": 10,
    "Healy Ben": 11,
    "Valgren Michael": 6,
    "Albanese Vincenzo": 5,
    "Baudin Alex": 4,
    "Berg Marijn": 9,
    "Russo Clément": 6,
    "Penho Paul": 7,
    "Barthe Cyril": 5,
    "Madouas Valentin": 10,
    "Martin Guillaume": 10,
    "Pacher Quentin": 6,
    "Grégoire Romain": 10,
    "Askey Lewis": 7,
    "Watson Samuel": 7,
    "Rodr Carlos": 15,
    "Swift Connor": 5,
    "Thomas Geraint": 10,
    "Foss Tobias": 8,
    "Arensman Thymen": 13,
    "Laurance Axel": 10,
    "Ganna Filippo": 12,
    "Girmay Biniam": 14,
    "Page Hugo": 7,
    "Braet Vito": 6,
    "Rutsch Jonas": 5,
    "Zimmermann Georg": 6,
    "Rex Laurenz": 7,
    "Sintmaartensdijk Roel": 3,
    "Barré Louis": 7,
    "Neilands Krists": 7,
    "Ackermann Pascal": 10,
    "Blackmore Joseph": 9,
    "Boivin Guillaume": 4,
    "Louvel Matis": 4,
    "Stewart Jake": 5,
    "Lutsenko Alexey": 9,
    "Woods Michael": 9,
    "Stuyven Jasper": 9,
    "Milan Jonathan": 14,
    "Skjelmose Mattias": 12,
    "Skuji Toms": 7,
    "Theuns Edward": 4,
    "Consonni Simone": 6,
    "Simmons Quinn": 4,
    "Nys Thibau": 11,
    "De Lie Arnaud": 11,
    "De Buyst Jasper": 4,
    "Van Eetvelt Lennert": 11,
    "Berckmoes Jenno": 6,
    "Van Moer Brent": 6,
    "Drizners Jarrad": 3,
    "Grignard Sébastien": 3,
    "Sep Eduardo": 4,
    "Garc Cortina Iv": 7,
    "Mas Enric": 12,
    "Oliveira Nelson": 5,
    "Mühlberger Gregor": 4,
    "Rubio Einer": 7,
    "Castrillo Pablo": 9,
    "Romeo Iv": 5,
    "Barta Will": 4,
    "Meeus Jordi": 11,
    "Poppel Danny": 7,
    "Lipowitz Florian": 11,
    "Rogli Primo": 16,
    "Vlasov Aleksandr": 12,
    "Pithie Laurence": 7,
    "Moscon Gianni": 6,
    "Dijke Mick": 4,
    "Merlier Tim": 16,
    "Evenepoel Remco": 18,
    "Van Wilder Ilan": 9,
    "Eenkhoorn Pascal": 3,
    "Van Lerberghe Bert": 4,
    "Cattaneo Mattia": 7,
    "Paret- Peintre Valentin": 9,
    "Schachmann Maximilian": 7,
    "Mezgec Luka": 7,
    "Groenewegen Dylan": 13,
    "Reinders Elmar": 3,
    "Dunbar Eddie": 10,
    "Connor Ben": 13,
    "Schmid Mauro": 7,
    "Durbridge Luke": 5,
    "Plapp Luke": 7,
    "Märkl Niklas": 3,
    "Bittner Pavel": 8,
    "Andresen Tobias Lund": 3,
    "Onley Oscar": 8,
    "Flynn Sean": 3,
    "Barguil Warren": 8,
    "Broek Frank": 6,
    "Naberman Tim": 3,
    "Turgis Anthony": 7,
    "Jegat Jordan": 6,
    "Gachignard Thomas": 4,
    "Cras Steff": 9,
    "Delettre Alexandre": 5,
    "Jeannière Emilien": 7,
    "Burgaudeau Mathieu": 6,
    "Vercher Mattéo": 5,
    "Jorgenson Matteo": 14,
    "Vingegaard Jonas": 19,
    "Benoot Tiesj": 8,
    "Affini Edoardo": 5,
    "Aert Wout": 13,
    "Campenaerts Victor": 8,
    "Kuss Sepp": 13,
    "Yates Simon": 13,
    "Trentin Matteo": 8,
    "Mayrhofer Marius": 3,
    "Haller Marco": 6,
    "Dainese Alberto": 9,
    "Lienhard Fabian": 3,
    "Hirschi Marc": 10,
    "Storer Michael": 10,
    "Alaphilippe Julian": 10,
    "Poga Tadej": 20,
    "Wellens Tim": 9,
    "Almeida Jo": 15,
    "Narv Jhonatan": 9,
    "Soler Marc": 8,
    "Politt Nils": 7,
    "Sivakov Pavel": 7,
    "Yates Adam": 14,
    "Wærenskjold Søren": 9,
    "Fredheim Stian": 7,
    "Johannessen Tobias Halland": 8,
    "Abrahamsen Jonas": 7,
    "Hoelgaard Markus": 6,
    "Cort Magnus": 10,
    "Leknessund Andreas": 6,
    "Johannessen Anders Halland": 6,
    "Teunissen Mike": 7,
    "Ballerini Davide": 7,
    "Tejada Harold": 8,
    "Higuita Sergio": 6,
    "Champoussin Clément": 8,
    "Velasco Simone": 6,
    "Fedorov Yevgeniy": 6,
    "Bol Cees": 8
}

#augmentation pour les périodes suivantes
c_augmentation = {
    p: math.ceil(1.1 * c[p])
    for p in P
}

#variable achat = 1 si on achete le joueur p à la période t, 0 sinon
achat = pulp.LpVariable.dicts("achat", (P, T), 0, 1, cat="Binary")
#variable vente = 1 si on achete le joueur p à la période t, 0 sinon
vente = pulp.LpVariable.dicts("vente", (P, T), 0, 1, cat="Binary")


## Variables de décision
# le budget restant r à la période t
r = pulp.LpVariable.dicts("r", T, lowBound=0) # >=0
# le choix d'un coureur p à la période t
x = pulp.LpVariable.dicts("x", (P, T), cat=pulp.LpBinary)


# z = pulp.LpVariable.dicts("z", (P, T), cat=pulp.LpBinary)

# Le prob à maximiser
prob += pulp.lpSum(
    points.get((p, e), 0) * x[p][period(e)]
    for p in P
    for e in E
) + pulp.lpSum(
    points.get((p, E_final), 0) * x[p][15]
    for p in P
)


# Listes de contraintes
# Budget Dyn
for i in range(1, len(T)):
    t_1 = T[i-1]
    t = T[i]

    for p in P:
        # Si x[p][t]=1 et x[p][t_1]=0, alors la variable achat[p][t] sera égale à 1, c'est à dire le cycliste p est ajouté au temps t
        # Si x[p][t]=0 et x[p][t_1]=1, alors la variable vente[p][t] sera égale à 1, c'est à dire le cycliste p est vendu au temps t
        # Si x[p][t]=0 et x[p][t_1]=0, alors achat[p][t] et vente[p][t] seront égale à 0, ainsi le joueur n'est pas selectionné
        # Si x[p][t]=1 et x[p][t_1]=1, alors achat[p][t] et vente[p][t] seront égale à 0. 
        # En effet, on ne peut pas acheter et vendre un joueur dans la même période il n'y aura jamais achat[p][t]=1 et vente[p][t]=1 en même temps
        prob += x[p][t] - x[p][t_1] == achat[p][t] - vente[p][t]

    # Le budget restant pour la période actuelle est le budget restant de la période précédente - les achats faits + les joueurs vendus
    prob += r[t] == r[t_1] - pulp.lpSum(c_augmentation[p] * achat[p][t] for p in P) + pulp.lpSum(c[p] * vente[p][t] for p in P)
    prob += r[t] >= 0


# Budget Initial
prob += pulp.lpSum(c[p] * x[p][0] for p in P) + r[0] == B, "Budget_Initial"

# Nombre de coureurs à chaque période
for t in T:
    prob += pulp.lpSum(x[p][t] for p in P) == 14


# Résolution du problème !!
status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
# print("Status :", pulp.LpStatus[status])


# print("Objectif =", prob.objective)
expr = prob.objective  # LpAffineExpression

for var, coef in expr.items():
    pass
    # print(var.name, coef)
    # print(len(prob.objective))
    # print(type(prob.objective))

# print("Nb contraintes =", len(prob.constraints))
# prob.writeLP("modele_tdf.lp")

# print(pulp.value(x["Vingegaard Jonas"][10]))

def equipe_opt(t):
    return [p for p in P if pulp.value(x[p][t]) == 1]

team = equipe_opt(15)
print(f"\nÉquipe optimale à la période t={t}")
for p in team:
    print(f"{p} | {points.get((p, 22), 0)}")

#Code pour visualiser les transferts à chaque étapes
"""
for i in range(1, len(T)):
    t_1 = T[i-1]
    t = T[i]

    print(f"\n----- Période {t_1} à {t} -----")

    print(f"--- Achats à la période {t} ---")
    cout_achat = 0
    for p in P:
        if pulp.value(achat[p][t]) == 1:
            cout = c_augmentation[p]
            cout_achat += cout
            print(f"  - {p} (avec un coût augmenté) : {cout}")
    print(f"Coût total des achats: {cout_achat}")

    print(f"\n--- Ventes à la période {t} ---")
    gain_vente = 0
    for p in P:
        if pulp.value(vente[p][t]) == 1:
            gain = c[p]
            gain_vente += gain
            print(f"  - {p} (coût initial) : {gain}")
    print(f"Revenu total des ventes : {gain_vente}")


    changement_budget = cout_achat - gain_vente
    print(f"\nChangement de budget après les transferts de la période {t} : {changement_budget}")
"""





#Code pour visualiser les équipes optimale à chaque période (sans l'augmentation du coût)
"""
for t in T:
    print(f"\n===== Équipe période {t} =====")
    cout_total = 0
    equipe = equipe_opt(t)

    total = 0

    for p in equipe:
        s = sum(
            points.get((p, e), 0)
            for e in E
            if period(e) == t
        )
        cout_total += c[p]


        total += s
        print(f"{p} | pts {s} | coût {c[p]}")

    print(f"\nTotal période : {total}")
    print(f"Voici le coût totale de l'équipe {cout_total}")

bonus_total = sum(
    points.get((p, E_final), 0)
    for p in equipe_opt(15)
)

print(f"Bonus final :{bonus_total}")

total_global = 0

for t in T:
    for p in equipe_opt(t):
        total_global += sum(
            points.get((p, e), 0)
            for e in E
            if period(e) == t
        )

total_global += bonus_total

print(f"\nTotal recalculé sans la solution du programme linéaire : {total_global}")
print(f"Valeur de la solution du programme linéaire : {pulp.value(prob.objective)}")


"""



#Code pour visualiser les équipes optimale à chaque période (avec l'augmentation du coût)
"""
for t in T:
    print(f"\n===== Équipe période {t} =====")
    equipe = equipe_opt(t)

    total_points = 0
    cout_total = 0


    for p in equipe:
        s = sum(
            points.get((p, e), 0)
            for e in E
            if period(e) == t
        )
        total_points += s
        if pulp.value(achat[p][t]) == 1:
            cout_cycliste = c_augmentation[p]
        else:
            cout_cycliste = c[p]

        cout_total += cout_cycliste
        print(f"{p} | pts {s} | coût {cout_cycliste}")

    print(f"Total points période : {total_points}")
    print(f"Coût total de l'équipe (avec augmentation) à la période {t}: {cout_total}")

bonus_total = sum(
    points.get((p, E_final), 0)
    for p in equipe_opt(15)
)

print(f"\nBonus final : {bonus_total}")

total_global = 0

for t in T:
    for p in equipe_opt(t):
        total_global += sum(
            points.get((p, e), 0)
            for e in E
            if period(e) == t
        )

total_global += bonus_total

print(f"\nTotal recalculé sans la solution du programme linéaire : {total_global}")
print(f"Valeur de la solution du programme linéaire : {pulp.value(prob.objective)}")
"""