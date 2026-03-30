import random
import math
import pulp
import streamlit as st
import pandas as pd

# ==============================
# STREAMLIT UI
# ==============================

st.set_page_config(page_title="Fantasy Cyclisme", layout="wide")
st.title("Fantasy Cyclisme - Démo avec transferts")


# Le paramètrage
with st.sidebar:
    st.header("Paramètres")
    seed = st.number_input("Seed", min_value=0, max_value=10_000, value=0, step=1)
    NB_COURSES = st.number_input("Nombre de courses", min_value=1, max_value=50, value=6, step=1)

    # Ici on garde ton schéma : 2 fenêtres de transfert => périodes [0, t1, t2]
    t1 = st.number_input("Période transfert 1 (avant la course 3)", min_value=1, max_value=int(NB_COURSES), value=3, step=1)
    t2 = st.number_input("Période transfert 2 (avant la course 5)", min_value=1, max_value=int(NB_COURSES), value=5, step=1)

    TAILLE_EQUIPE = st.number_input("Taille équipe", min_value=1, max_value=10, value=3, step=1)
    BUDGET_INITIAL = st.number_input("Budget initial", min_value=1, max_value=500, value=100, step=1)
    MAX_TRANSFERTS = st.number_input("Max transferts par fenêtre", min_value=0, max_value=10, value=1, step=1)

    st.markdown("---")
    nb_coureurs = st.number_input("Nombre de coureurs", min_value=5, max_value=100, value=9, step=1)
    cout_min = st.number_input("Coût min", min_value=1, max_value=100, value=10, step=1)
    cout_max = st.number_input("Coût max", min_value=1, max_value=100, value=10, step=1)
    pts_min = st.number_input("Points min/course", min_value=0, max_value=100, value=1, step=1)
    pts_max = st.number_input("Points max/course", min_value=0, max_value=100, value=20, step=1)

# Contrôle périodes
if not (0 < t1 <= NB_COURSES and 0 < t2 <= NB_COURSES and t1 < t2):
    st.error("Il faut que 1 <= t1 < t2 <= NB_COURSES.")
    st.stop()

PERIODES = [0, int(t1), int(t2)]

def period(e: int) -> int:
    # courses 1..(t1-1) => période 0
    # courses t1..(t2-1) => période t1
    # courses t2..NB_COURSES => période t2
    if e < t1:
        return 0
    elif e < t2:
        return int(t1)
    return int(t2)

# ==============================
# SOLVER
# ==============================

def solve_instance(seed: int):
    random.seed(seed)

    P = [f"Coureur_{i}" for i in range(1, int(nb_coureurs) + 1)]

    # coûts
    if cout_min > cout_max:
        raise ValueError("cout_min doit être <= cout_max")
    c = {p: random.randint(int(cout_min), int(cout_max)) for p in P}

    # points
    if pts_min > pts_max:
        raise ValueError("pts_min doit être <= pts_max")
    points = {(p, e): random.randint(int(pts_min), int(pts_max))
              for p in P for e in range(1, int(NB_COURSES) + 1)}
    
    # Zéros de 3 à 6
    points[("Coureur_1", 1)] = 0
    points[("Coureur_1", 2)] = 0
    points[("Coureur_1", 3)] = 1
    points[("Coureur_1", 4)] = 60
    points[("Coureur_1", 5)] = 0
    points[("Coureur_1", 6)] = 0

    points[("Coureur_2", 1)] = 40
    points[("Coureur_2", 2)] = 50
    points[("Coureur_2", 3)] = 0
    points[("Coureur_2", 4)] = 10
    points[("Coureur_2", 5)] = 0
    points[("Coureur_2", 6)] = 0
    c_augmentation = {p: math.ceil(1.1 * c[p]) for p in P}

    prob = pulp.LpProblem("FantasyCyclisme_Exemple_Transfert", pulp.LpMaximize)

    x = pulp.LpVariable.dicts("x", (P, PERIODES), cat=pulp.LpBinary)
    achat = pulp.LpVariable.dicts("achat", (P, PERIODES), cat=pulp.LpBinary)
    vente = pulp.LpVariable.dicts("vente", (P, PERIODES), cat=pulp.LpBinary)
    r = pulp.LpVariable.dicts("budget", PERIODES, lowBound=0)

    # Objectif
    prob += pulp.lpSum(
        points[(p, e)] * x[p][period(e)]
        for p in P
        for e in range(1, int(NB_COURSES) + 1)
    )

    # Taille équipe constante
    for t in PERIODES:
        prob += pulp.lpSum(x[p][t] for p in P) == int(TAILLE_EQUIPE)

    # Budget initial
    prob += pulp.lpSum(c[p] * x[p][0] for p in P) <= int(BUDGET_INITIAL)
    prob += r[0] == int(BUDGET_INITIAL) - pulp.lpSum(c[p] * x[p][0] for p in P)

    # Evolution équipe + budget
    for t in PERIODES[1:]:
        t_prev = PERIODES[PERIODES.index(t) - 1]

        for p in P:
            prob += x[p][t] - x[p][t_prev] == achat[p][t] - vente[p][t]
            prob += achat[p][t] + vente[p][t] <= 1

            # Cohérence logique
            prob += achat[p][t] <= 1 - x[p][t_prev]
            prob += achat[p][t] <= x[p][t]
            prob += vente[p][t] <= x[p][t_prev]
            prob += vente[p][t] <= 1 - x[p][t]

        prob += r[t] == (
            r[t_prev]
            - pulp.lpSum(c_augmentation[p] * achat[p][t] for p in P)
            + pulp.lpSum(c[p] * vente[p][t] for p in P)
        )
        prob += r[t] >= 0

    # Limite transferts (entrants)
    for t in PERIODES[1:]:
        prob += pulp.lpSum(achat[p][t] for p in P) <= int(MAX_TRANSFERTS)

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    status = pulp.LpStatus[prob.status]

    def equipe(t):
        return [p for p in P if pulp.value(x[p][t]) == 1]

    # Score total
    score_total = sum(
        points[(p, e)] * pulp.value(x[p][period(e)])
        for p in P
        for e in range(1, int(NB_COURSES) + 1)
    )

    # DataFrames pour affichage
    df_points = pd.DataFrame(
        {"Coureur": P, **{f"Course_{e}": [points[(p, e)] for p in P] for e in range(1, int(NB_COURSES) + 1)}}
    )
    df_points["Total"] = df_points[[f"Course_{e}" for e in range(1, int(NB_COURSES) + 1)]].sum(axis=1)
    df_points = df_points.sort_values("Coureur", ascending=True)

    equipes = {}
    budgets = {t: float(pulp.value(r[t])) for t in PERIODES}
    transferts = {}
    for t in PERIODES:
        equipes[t] = equipe(t)

    for t in PERIODES[1:]:
        transferts[t] = {
            "entrants": [p for p in P if pulp.value(achat[p][t]) == 1],
            "sortants": [p for p in P if pulp.value(vente[p][t]) == 1],
        }

    return {
        "status": status,
        "score_total": float(score_total),
        "df_points": df_points,
        "equipes": equipes,
        "budgets": budgets,
        "transferts": transferts,
        "c": c,
    }

# ==============================
# RUN BUTTON
# ==============================

run = st.button("Résoudre")

if run:
    try:
        res = solve_instance(int(seed))
    except Exception as ex:
        st.exception(ex)
        st.stop()

    st.subheader("Statut solveur")
    st.write(res["status"])

    st.subheader("Données générées (points)")
    df = res["df_points"].copy()
    df["Coureur"] = df["Coureur"].astype(object)  # colonne texte en objet python
    st.dataframe(df, use_container_width=True)

    st.subheader("Résultat optimisation")
    colA, colB = st.columns([1, 1])
    with colA:
        st.metric("Score total optimal", int(res["score_total"]))
    with colB:
        st.write("Périodes :", PERIODES)

    per = -1
    for t in PERIODES:
        per += 1
        st.markdown(f"### Équipe période {per}")
        team = res["equipes"][t]
        df_team = pd.DataFrame({
            "Coureur": team,
            "Coût": [res["c"][p] for p in team],
        })
        df = res["df_points"].copy()

        # forcer type compatible Streamlit
        df["Coureur"] = df["Coureur"].astype(object)

        # AJOUT DE LA COLONNE COÛT
        df["Coût"] = df["Coureur"].map(res["c"]).astype(int)

        # (optionnel) placer Coût juste après Coureur
        cols = ["Coureur", "Coût"] + [c for c in df.columns if c not in ("Coureur", "Coût")]
        df = df[cols]

        st.dataframe(df, use_container_width=True)
        st.write("Budget restant :", int(res["budgets"][t]))

        if t != 0:
            tr = res["transferts"][t]
            st.write("Entrants :", tr["entrants"] if tr["entrants"] else "aucun")
            st.write("Sortants :", tr["sortants"] if tr["sortants"] else "aucun")

    st.subheader("Score par course")

    df_pts = res["df_points"].copy()
    df_pts["Coureur"] = df_pts["Coureur"].astype(object)
    df_pts = df_pts.set_index("Coureur")

    rows = []
    for e in range(1, int(NB_COURSES) + 1):
        t = period(e)
        team = res["equipes"][t]
        score_e = int(df_pts.loc[team, f"Course_{e}"].sum())

        rows.append({
            "Course": int(e),
            "Période": int(t),
            "Équipe": ", ".join(map(str, team)),
            "Score": int(score_e),
        })

    df_score = pd.DataFrame(rows)

    df_score["Équipe"] = df_score["Équipe"].astype(object)
    df_score["Course"] = df_score["Course"].astype(int)
    df_score["Période"] = df_score["Période"].astype(int)
    df_score["Score"] = df_score["Score"].astype(int)

    st.dataframe(df_score, use_container_width=True)

    st.metric("Somme des scores par course", int(df_score["Score"].sum()))

else:
    st.info("Régle les paramètres à gauche puis clique sur « Résoudre ».")