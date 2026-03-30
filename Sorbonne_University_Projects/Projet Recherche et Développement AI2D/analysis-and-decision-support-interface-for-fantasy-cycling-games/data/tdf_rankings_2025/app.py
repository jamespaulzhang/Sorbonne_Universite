import streamlit as st
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import re
import io
import time
from collections import defaultdict
from gurobipy import Model, GRB, quicksum

# =====================================================================
# 1. Fonction d'optimisation (avec cache)
# =====================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def optimiser_equipe(valeurs_bytes, maillots_bytes, final_bytes, stages_bytes_list,
                     abandons_10, abandons_15,
                     initial_budget=140, team_size=14, time_limit=600, mip_gap=1e-6,
                     custom_points=None, custom_prices=None):
    """
    Optimisation avec Gurobi.
    Si custom_points est fourni, il écrase les points du fichier.
    Si custom_prices est fourni, il écrase les prix.
    """
    # Lecture des DataFrames depuis les bytes
    valeurs_df = pd.read_csv(io.BytesIO(valeurs_bytes))
    maillots_df = pd.read_csv(io.BytesIO(maillots_bytes))
    final_df = pd.read_csv(io.BytesIO(final_bytes))

    # Reconstruction des stages
    stages_dfs = {}
    for f_bytes, f_name in stages_bytes_list:
        match = re.search(r"stage_(\d+)_", f_name)
        if match:
            stage_num = int(match.group(1))
            stages_dfs[stage_num] = pd.read_csv(io.BytesIO(f_bytes))
    stages_dfs = dict(sorted(stages_dfs.items()))

    # 1. Prix
    prices = valeurs_df.set_index("Rider")["poids"].to_dict()
    if custom_prices:
        prices.update(custom_prices)

    R = list(prices.keys())
    T = [0, 1, 2]
    aug_price = {r: math.ceil(1.1 * prices[r]) for r in R}

    # 2. Période
    def period(i):
        if i <= 10:
            return 0
        elif i <= 15:
            return 1
        else:
            return 2

    # 3. Points
    points_stage = {
        1: 30, 2: 20, 3: 18, 4: 17, 5: 16,
        6: 15, 7: 14, 8: 13, 9: 12, 10: 11,
        11: 10, 12: 9, 13: 8, 14: 7, 15: 6,
        16: 5, 17: 4, 18: 3, 19: 2, 20: 1
    }
    points = {}
    for i, stage_df in stages_dfs.items():
        for rank, rider in enumerate(stage_df["Rider"], start=1):
            points[(rider, i)] = points_stage.get(rank, 0)

    # Maillots
    for idx, row in maillots_df.iterrows():
        etape = idx + 1
        for col, pts in zip(["Jaune", "Vert", "Pois", "Blanc", "Combatif1", "Combatif2"],
                            [8, 5, 5, 5, 5, 5]):
            if pd.notna(row[col]):
                rider = row[col]
                points[(rider, etape)] = points.get((rider, etape), 0) + pts

    # Final
    E_final = 22
    for _, row in final_df.iterrows():
        rider = row["Rider"]
        bonus = sum(row[col] for col in ["jaune", "vert", "pois", "jeune", "comba"]
                    if not pd.isna(row[col]))
        points[(rider, E_final)] = bonus

    # Appliquer les points personnalisés
    if custom_points:
        for (r, e), val in custom_points.items():
            points[(r, e)] = val

    # 4. Modèle Gurobi
    m = Model("Fantasy_TDF")
    m.Params.OutputFlag = 0
    m.Params.MIPFocus = 2
    m.Params.MIPGap = mip_gap
    m.Params.TimeLimit = time_limit
    m.Params.Heuristics = 0.5

    x = m.addVars(R, T, vtype=GRB.BINARY, name="x")
    buy = m.addVars(R, T, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="buy")
    sell = m.addVars(R, T, vtype=GRB.CONTINUOUS, lb=0, ub=1, name="sell")
    budget = m.addVars(T, lb=0, name="budget")

    # Objectif
    m.setObjective(
        quicksum(points.get((r, e), 0) * x[r, period(e)] for r in R for e in range(1, 22)) +
        quicksum(points.get((r, E_final), 0) * x[r, 2] for r in R),
        GRB.MAXIMIZE
    )

    # Contraintes
    for t in T:
        m.addConstr(quicksum(x[r, t] for r in R) == team_size)

    for r in R:
        for t in T[1:]:
            m.addConstr(buy[r, t] - sell[r, t] == x[r, t] - x[r, t-1])
            m.addConstr(buy[r, t] + sell[r, t] <= 1)

    m.addConstr(budget[0] == initial_budget - quicksum(prices[r] * x[r, 0] for r in R))

    for t in T[1:]:
        m.addConstr(budget[t] == budget[t-1] - quicksum(aug_price[r] * buy[r, t] for r in R)
                    + quicksum(prices[r] * sell[r, t] for r in R))
        m.addConstr(budget[t] >= 0)

    # ========== Règles de vente adaptées aux abandons ==========
    # Définir pour chaque période quels coureurs peuvent être vendus
    #   - Période 1 : seuls les abandons_10 peuvent être vendus
    #   - Période 2 : tous les abandons_15 peuvent être vendus
    sell_allowed = {
        1: set(abandons_10),
        2: set(abandons_15)
    }
    for t in T[1:]:
        for r in R:
            if r not in sell_allowed[t]:
                m.addConstr(sell[r, t] == 0, name=f"no_sell_{r}_{t}")

    # Les coureurs abandonneurs ne peuvent pas être présents après leur abandon
    for r in abandons_10:
        for t in [1, 2]:
            m.addConstr(x[r, t] == 0, name=f"abandon_{r}_{t}")

    for r in set(abandons_15) - set(abandons_10):
        m.addConstr(x[r, 2] == 0, name=f"abandon15_{r}")
    # =========================================================================

    # Résolution
    m.optimize()

    if m.status != GRB.OPTIMAL:
        return {"status": m.status, "message": "Pas de solution optimale trouvée"}

    # Récupération des résultats
    score_total = m.objVal
    equipes = {t: [r for r in R if x[r, t].X > 0.5] for t in T}
    budgets = {t: budget[t].X for t in T}
    transferts = {t: {"entrants": [r for r in R if buy[r, t].X > 0.5],
                      "sortants": [r for r in R if sell[r, t].X > 0.5]} for t in T[1:]}

    # Construire le DataFrame des points par coureur
    points_data = []
    for r in R:
        row = {"Coureur": r, "Prix": prices[r]}
        total = 0
        for e in range(1, 22):
            p = points.get((r, e), 0)
            row[f"Étape_{e}"] = p
            total += p
        row["Total"] = total
        row["Période_0"] = sum(points.get((r, e), 0) for e in range(1, 11))
        row["Période_1"] = sum(points.get((r, e), 0) for e in range(11, 16))
        row["Période_2"] = sum(points.get((r, e), 0) for e in range(16, 22))
        points_data.append(row)
    points_df = pd.DataFrame(points_data).set_index("Coureur")
    cols = ["Prix", "Période_0", "Période_1", "Période_2", "Total"] + [f"Étape_{e}" for e in range(1, 22)]
    points_df = points_df[cols]

    return {
        "status": m.status,
        "score_total": score_total,
        "equipes": equipes,
        "budgets": budgets,
        "transferts": transferts,
        "points_df": points_df,
        "prices": prices,
    }

# =====================================================================
# 2. Analyse de stabilité (intervalle de tolérance)
# =====================================================================
def stabilite_interval(base_res, rider, period_target, var_type="points",
                       n_steps=20, max_factor=2.0, precision=0.001,
                       fast=True):
    """
    Calcule l'intervalle de tolérance pour un coureur sur une période donnée.
    var_type : "points" (variation des points du coureur sur la période) ou "prix".
    fast : si True, utilise des paramètres rapides (time_limit=30, mip_gap=0.01).
    Retourne (low, high) facteur multiplicatif tel que la sélection du coureur
    dans l'équipe optimale de la période reste inchangée.
    """
    if rider not in base_res["points_df"].index:
        return None, None

    selected = rider in base_res["equipes"][period_target]

    # Paramètres rapides pour les sous-optimisations
    opt_kwargs = {}
    if fast:
        opt_kwargs["time_limit"] = 30
        opt_kwargs["mip_gap"] = 0.01
    else:
        opt_kwargs["time_limit"] = st.session_state.time_limit
        opt_kwargs["mip_gap"] = st.session_state.mip_gap

    def test_factor(k):
        # Créer des modifications
        custom_points = {}
        if var_type == "points":
            # Modifier les points du coureur sur toutes les étapes de la période
            for e in range(1, 22):
                if period_target == 0 and e <= 10:
                    custom_points[(rider, e)] = base_res["points_df"].loc[rider, f"Étape_{e}"] * k
                elif period_target == 1 and 11 <= e <= 15:
                    custom_points[(rider, e)] = base_res["points_df"].loc[rider, f"Étape_{e}"] * k
                elif period_target == 2 and e >= 16:
                    custom_points[(rider, e)] = base_res["points_df"].loc[rider, f"Étape_{e}"] * k
        else:
            custom_prices = {rider: base_res["prices"][rider] * k}
            custom_points = None

        # Récupérer les bytes depuis la session
        if "valeurs_bytes" not in st.session_state:
            st.error("Données manquantes pour l'analyse.")
            return None

        res = optimiser_equipe(
            st.session_state.valeurs_bytes,
            st.session_state.maillots_bytes,
            st.session_state.final_bytes,
            st.session_state.stages_bytes_list,
            st.session_state.abandons_10,
            st.session_state.abandons_15,
            initial_budget=st.session_state.initial_budget,
            team_size=st.session_state.team_size,
            **opt_kwargs,  # Utilise les paramètres rapides
            custom_points=custom_points,
            custom_prices=custom_prices if var_type == "prix" else None
        )
        if res["status"] != GRB.OPTIMAL:
            return None
        new_selected = rider in res["equipes"][period_target]
        return new_selected == selected

    # Recherche binaire pour la borne inférieure
    # On cherche le plus petit facteur (<=1) qui fait changer le statut
    low = 0.0
    high = 1.0
    # D'abord, trouver un facteur où le statut change (en descendant)
    found_change = False
    # On explore quelques points pour localiser la zone
    test_factors = np.linspace(0.1, 1.0, n_steps)
    progress_bar = st.progress(0)
    for i, factor in enumerate(test_factors):
        progress_bar.progress((i+1)/(2*n_steps))  # première moitié
        res = test_factor(factor)
        if res is None:
            continue
        if res != selected:
            # Le changement se produit entre le facteur précédent et celui-ci
            # On prend le précédent comme borne basse
            if i > 0:
                low = test_factors[i-1]
            else:
                low = 0.0
            high = factor
            found_change = True
            break
    if not found_change:
        # Pas de changement, la borne inférieure est 0
        low = 0.0
    else:
        # Affiner par dichotomie
        for _ in range(15):  # 15 itérations suffisent pour la précision
            mid = (low + high) / 2
            progress_bar.progress(0.5 + 0.5 * (_/15))  # deuxième moitié
            res = test_factor(mid)
            if res is None:
                continue
            if res == selected:
                low = mid
            else:
                high = mid
    progress_bar.empty()

    # Borne supérieure (facteur >=1)
    low_up = 1.0
    high_up = max_factor
    found_change_up = False
    # Trouver un facteur où le statut change (en montant)
    test_factors_up = np.linspace(1.0, max_factor, n_steps)
    progress_bar = st.progress(0)
    for i, factor in enumerate(test_factors_up):
        progress_bar.progress((i+1)/(2*n_steps))
        res = test_factor(factor)
        if res is None:
            continue
        if res != selected:
            low_up = test_factors_up[i-1] if i>0 else 1.0
            high_up = factor
            found_change_up = True
            break
    if not found_change_up:
        high_up = max_factor
    else:
        for _ in range(15):
            mid = (low_up + high_up) / 2
            progress_bar.progress(0.5 + 0.5 * (_/15))
            res = test_factor(mid)
            if res is None:
                continue
            if res == selected:
                low_up = mid
            else:
                high_up = mid
    progress_bar.empty()

    # Retourner les intervalles
    return low, high_up

# =====================================================================
# 3. Analyse des dépendances (co-occurrence)
# =====================================================================
def analyse_dependances(base_res, period_target, n_scenarios=50, noise_std=0.05,
                        top_n_coureurs=30):
    """
    Génère des scénarios de perturbations aléatoires sur les points de tous les coureurs,
    recalcule l'équipe optimale pour la période, et calcule les co-occurrences.
    Retourne une matrice de co-occurrence (numpy) et la liste des coureurs.
    """
    points_df = base_res["points_df"].copy()
    # On ne garde que les coureurs avec un ratio intéressant pour limiter le temps
    points_df["Ratio"] = points_df["Total"] / points_df["Prix"]
    # Prendre les top_n_coureurs les plus fréquents ou ceux de l'équipe de base
    base_team = base_res["equipes"][period_target]
    candidates = list(set(base_team) | set(points_df.nlargest(top_n_coureurs, "Ratio").index))
    n = len(candidates)
    idx_map = {r: i for i, r in enumerate(candidates)}
    co_occur = np.zeros((n, n))

    for scenario in range(n_scenarios):
        # Générer un bruit multiplicatif sur les points de tous les coureurs
        custom_points = {}
        for r in candidates:
            factor = np.random.normal(1, noise_std)
            # Appliquer le facteur à toutes les étapes (pour simplifier)
            for e in range(1, 22):
                original = base_res["points_df"].loc[r, f"Étape_{e}"]
                custom_points[(r, e)] = original * max(0, factor)  # éviter négatif
        # Lancer l'optimisation avec ces points
        res = optimiser_equipe(
            st.session_state.valeurs_bytes,
            st.session_state.maillots_bytes,
            st.session_state.final_bytes,
            st.session_state.stages_bytes_list,
            st.session_state.abandons_10,
            st.session_state.abandons_15,
            initial_budget=st.session_state.initial_budget,
            team_size=st.session_state.team_size,
            time_limit=st.session_state.time_limit,
            mip_gap=st.session_state.mip_gap,
            custom_points=custom_points
        )
        if res["status"] != GRB.OPTIMAL:
            continue
        team = set(res["equipes"][period_target])
        # Mettre à jour la matrice de co-occurrence
        for r1 in team:
            if r1 not in idx_map:
                continue
            i = idx_map[r1]
            for r2 in team:
                if r2 not in idx_map:
                    continue
                j = idx_map[r2]
                co_occur[i, j] += 1
    # Normaliser en fréquence
    max_occ = n_scenarios
    co_occur /= max_occ
    return co_occur, candidates

# =====================================================================
# 4. Interface Streamlit
# =====================================================================
st.set_page_config(page_title="Fantasy Cyclisme - Optimisation Gurobi", layout="wide")
st.title("Optimisation d'équipe pour le jeu « On connaît nos classiques »")

# Initialisation des variables de session pour les bytes
if "valeurs_bytes" not in st.session_state:
    st.session_state.valeurs_bytes = None
if "maillots_bytes" not in st.session_state:
    st.session_state.maillots_bytes = None
if "final_bytes" not in st.session_state:
    st.session_state.final_bytes = None
if "stages_bytes_list" not in st.session_state:
    st.session_state.stages_bytes_list = []
if "abandons_10" not in st.session_state:
    st.session_state.abandons_10 = []
if "abandons_15" not in st.session_state:
    st.session_state.abandons_15 = []

# Paramètres
with st.sidebar:
    fast_stability = st.checkbox("Utiliser le mode rapide pour l'analyse de stabilité (moins précis mais plus rapide)", value=True)

    st.header("Paramètres généraux")
    initial_budget = st.number_input("Budget initial (M€)", min_value=0, value=140, step=10)
    team_size = st.number_input("Taille de l'équipe", min_value=1, max_value=30, value=14, step=1)
    time_limit = st.number_input("Temps limite (secondes)", min_value=10, value=600, step=60)
    mip_gap = st.number_input("MIP Gap", min_value=0.0, max_value=0.1, value=1e-6, format="%e")

    st.markdown("---")
    st.header("Fichiers de données")
    uploaded_valeurs = st.file_uploader("valeurs.csv", type="csv")
    uploaded_maillots = st.file_uploader("maillots.csv", type="csv")
    uploaded_final = st.file_uploader("final.csv", type="csv")
    uploaded_stages = st.file_uploader("Étapes (stage_01_2025.csv ... stage_21_2025.csv)", accept_multiple_files=True, type="csv")

    st.markdown("---")
    st.header("Listes d'abandons (optionnel)")
    abandons_10_text = st.text_area("Abandons après période 0 (un nom par ligne)", 
                                    "Ganna Filippo\nBissegger Stefan\nPhilipsen Jasper\nJeannière Emilien\nDe Buyst Jasper\nCattaneo Mattia\nHaig Jack\nDunbar Eddie\nAlmeida Jo\nBerg Marijn\nZimmermann Georg\nWærenskjold Søren")
    abandons_15_text = st.text_area("Abandons supplémentaires après période 1 (un nom par ligne)",
                                    "Bol Cees\nEvenepoel Remco\nSkjelmose Mattias\nCoquard Bryan\nCras Steff\nVan Eetvelt Lennert\nPoel Mathieu")

    st.markdown("---")
    run_button = st.button("Lancer l'optimisation")

if run_button:
    if not all([uploaded_valeurs, uploaded_maillots, uploaded_final, uploaded_stages]):
        st.error("Veuillez charger tous les fichiers nécessaires.")
        st.stop()

    # Stocker les bytes en session pour les analyses post-opt
    st.session_state.valeurs_bytes = uploaded_valeurs.read()
    st.session_state.maillots_bytes = uploaded_maillots.read()
    st.session_state.final_bytes = uploaded_final.read()
    st.session_state.stages_bytes_list = [(f.read(), f.name) for f in uploaded_stages]
    st.session_state.abandons_10 = [line.strip() for line in abandons_10_text.splitlines() if line.strip()]
    st.session_state.abandons_15 = st.session_state.abandons_10 + [line.strip() for line in abandons_15_text.splitlines() if line.strip()]
    st.session_state.initial_budget = initial_budget
    st.session_state.team_size = team_size
    st.session_state.time_limit = time_limit
    st.session_state.mip_gap = mip_gap

    # Lancement de l'optimisation principale
    with st.spinner("Optimisation en cours... (peut prendre plusieurs minutes)"):
        result = optimiser_equipe(
            st.session_state.valeurs_bytes,
            st.session_state.maillots_bytes,
            st.session_state.final_bytes,
            st.session_state.stages_bytes_list,
            st.session_state.abandons_10,
            st.session_state.abandons_15,
            initial_budget=initial_budget,
            team_size=team_size,
            time_limit=time_limit,
            mip_gap=mip_gap
        )

    if result["status"] != GRB.OPTIMAL:
        st.error(f"Problème : statut Gurobi {result['status']} – pas de solution optimale trouvée.")
        st.stop()

    st.success("Optimisation réussie !")
    st.metric("Score total optimal", f"{result['score_total']:.1f}")

    # ========================
    # Affichage des résultats principaux
    # ========================
    points_df = result["points_df"].copy()

    st.subheader("Points par coureur et par période")
    styled = points_df.style.background_gradient(subset=["Période_0", "Période_1", "Période_2", "Total"], cmap="Blues")
    st.dataframe(styled, use_container_width=True)

    st.subheader("Bar chart : Points / Coût par coureur")
    points_df["Ratio"] = points_df["Total"] / points_df["Prix"]
    points_df["Ratio"] = points_df["Ratio"].fillna(0)
    selected_period = st.selectbox("Période pour la couleur", [0, 1, 2], format_func=lambda x: f"Période {x}")
    equipe_sel = result["equipes"][selected_period]
    points_df["Ratio_periode"] = points_df[f"Période_{selected_period}"] / points_df["Prix"]
    points_df["Ratio_periode"] = points_df["Ratio_periode"].fillna(0)
    df_plot = points_df[["Prix", f"Période_{selected_period}", "Ratio_periode"]].copy()
    df_plot = df_plot.sort_values("Ratio_periode", ascending=False)
    df_plot["Couleur"] = ["red" if nom in equipe_sel else "skyblue" for nom in df_plot.index]

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(df_plot.index, df_plot["Ratio_periode"], color=df_plot["Couleur"], edgecolor='black', linewidth=0.8)
    ax.set_xticklabels(df_plot.index, rotation=90, fontsize=8)
    ax.set_ylabel("Points / Coût")
    ax.set_title(f"Ratio (Points Période {selected_period} / Prix) – Rouge = dans l'équipe à cette période")
    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label='Dans l’équipe', markerfacecolor='red', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='Hors équipe', markerfacecolor='skyblue', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    # ========================
    # Analyse post-optimale
    # ========================
    st.subheader("Analyse post-optimale")
    tab1, tab2 = st.tabs(["Stabilité", "Dépendances"])

    with tab1:
        st.write("Analyse de stabilité (intervalle de tolérance)")
        period_stab = st.selectbox("Période", [0, 1, 2], key="stab_period", format_func=lambda x: f"Période {x}")
        team_stab = result["equipes"][period_stab]
        if not team_stab:
            st.warning("Aucun coureur dans cette période.")
        else:
            rider_stab = st.selectbox("Coureur", team_stab)
            var_type = st.radio("Type de variation", ["Points", "Prix"], index=0)
            if st.button("Calculer l'intervalle de tolérance"):
                with st.spinner("Calcul en cours (plusieurs optimisations)..."):
                    low, high = stabilite_interval(
                        result, rider_stab, period_stab,
                        var_type="points" if var_type == "Points" else "prix",
                        fast=fast_stability
                    )
                if low is not None:
                    if var_type == "Points":
                        st.info(f"Intervalle de tolérance pour **{rider_stab}** (période {period_stab}) :\n"
                                f"- Facteur multiplicatif sur ses points : [{low:.3f}, {high:.3f}]\n"
                                f"- Il reste dans l'équipe tant que ses points varient entre -{100*(1-low):.1f}% et +{100*(high-1):.1f}%.")
                    else:
                        st.info(f"Intervalle de tolérance pour **{rider_stab}** (période {period_stab}) :\n"
                                f"- Facteur multiplicatif sur son prix : [{low:.3f}, {high:.3f}]\n"
                                f"- Il reste dans l'équipe tant que son prix varie entre -{100*(1-low):.1f}% et +{100*(high-1):.1f}%.")
                else:
                    st.error("Impossible de calculer l'intervalle (problème d'optimisation).")

    with tab2:
        st.write("Analyse des dépendances (co-occurrence)")
        period_dep = st.selectbox("Période", [0, 1, 2], key="dep_period", format_func=lambda x: f"Période {x}")
        n_scenarios = st.slider("Nombre de scénarios", 10, 200, 50, step=10)
        noise_std = st.slider("Niveau de bruit (écart-type relatif)", 0.01, 0.2, 0.05, step=0.01)
        top_n = st.slider("Nombre de coureurs à considérer", 10, 100, 30, step=10)
        if st.button("Lancer l'analyse des dépendances"):
            with st.spinner(f"Génération de {n_scenarios} scénarios (peut être très long)..."):
                co_occur, candidates = analyse_dependances(
                    result, period_dep, n_scenarios, noise_std, top_n_coureurs=top_n
                )
            if co_occur is not None:
                fig, ax = plt.subplots(figsize=(12, 10))
                sns.heatmap(co_occur, xticklabels=candidates, yticklabels=candidates,
                            annot=False, cmap="Blues", ax=ax)
                ax.set_title(f"Fréquence de co-occurrence (période {period_dep})")
                st.pyplot(fig)

                # Extraire les paires les plus fréquentes
                pairs = []
                for i in range(len(candidates)):
                    for j in range(i+1, len(candidates)):
                        freq = co_occur[i, j]
                        if freq > 0:
                            pairs.append((candidates[i], candidates[j], freq))
                pairs.sort(key=lambda x: x[2], reverse=True)
                st.write("Paires les plus fréquentes (co-occurrence > 0.3) :")
                df_pairs = pd.DataFrame([(p[0], p[1], f"{p[2]*100:.1f}%") for p in pairs if p[2] > 0.3],
                                        columns=["Coureur A", "Coureur B", "Fréquence"])
                st.dataframe(df_pairs, use_container_width=True)
            else:
                st.error("Erreur lors de l'analyse des dépendances.")

    # Détail des équipes par période
    for t in [0, 1, 2]:
        st.markdown(f"### Période {t}")
        team = result["equipes"][t]
        df_team = points_df.loc[team].copy()
        df_team["Coureur"] = df_team.index
        df_team = df_team[["Coureur", "Prix", "Période_0", "Période_1", "Période_2", "Total"]]
        styled_team = df_team.style.background_gradient(subset=["Total"], cmap="Greens")
        st.dataframe(styled_team, use_container_width=True)
        st.write(f"Budget restant : {result['budgets'][t]:.2f} M€")
        if t in result["transferts"]:
            tr = result["transferts"][t]
            if tr["entrants"]:
                st.write("**Entrants** :", ", ".join(tr["entrants"]))
            if tr["sortants"]:
                st.write("**Sortants** :", ", ".join(tr["sortants"]))

    # Score par étape
    st.subheader("Score par étape")
    rows = []
    for e in range(1, 22):
        t = 0 if e <= 10 else (1 if e <= 15 else 2)
        team = result["equipes"][t]
        score_e = sum(points_df.loc[r, f"Étape_{e}"] for r in team if r in points_df.index)
        rows.append({"Étape": e, "Période": t, "Score": score_e})
    df_score = pd.DataFrame(rows)
    st.dataframe(df_score, use_container_width=True)
    st.metric("Somme des scores par étape", df_score["Score"].sum())