from collections import deque
import heapq
import time
import random
import matplotlib.pyplot as plt
import os
import sys

try:
    import gurobipy as gp
    from gurobipy import GRB
    GUROBI_AVAILABLE = True
except ImportError:
    GUROBI_AVAILABLE = False
    print("Gurobi n'est pas installé. La génération avec contraintes utilisera une méthode heuristique.")

# ==================== CONFIGURATION DES DOSSIERS ====================

# Définition des noms de dossiers
INSTANCES_DIR = "instances"
RESULTATS_DIR = "resultats"
GRAPHIQUES_DIR = "graphiques"

def creer_dossiers():
    """
    Crée les dossiers nécessaires pour le stockage des fichiers générés
    """
    dossiers = [INSTANCES_DIR, RESULTATS_DIR, GRAPHIQUES_DIR]
    for dossier in dossiers:
        if not os.path.exists(dossier):
            try:
                os.makedirs(dossier)
                print(f"Dossier créé: {dossier}")
            except Exception as e:
                print(f"Erreur lors de la création du dossier {dossier}: {e}")

# Créer les dossiers au démarrage du programme
creer_dossiers()

# ==================== FONCTIONS DE BASE ====================

# Directions : Nord 0, Est 1, Sud 2, Ouest 3
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
dir_map = {"nord": 0, "est": 1, "sud": 2, "ouest": 3}

def is_position_safe(x, y, M, N, grid):
    """
    Vérifie si la position (x,y) est sûre pour le robot.
    Le robot au croisement (x,y) couvre les cases dont les indices de ligne sont dans [x-1, x] ∩ [0, M-1]
    et les indices de colonne dans [y-1, y] ∩ [0, N-1].
    """
    # Vérifie si le croisement est dans les limites valides
    if x < 0 or x > M or y < 0 or y > N:
        return False
    
    # Vérifie si toutes les cases couvertes sont libres d'obstacles
    for i in range(max(0, x-1), min(M, x+1)):
        for j in range(max(0, y-1), min(N, y+1)):
            if grid[i][j] == 1:
                return False
    return True

# ==================== ALGORITHMES DE RECHERCHE ====================

def solve_bfs(M, N, grid, start_x, start_y, end_x, end_y, start_dir):
    """ 
    Implémente un BFS pour trouver le chemin optimal du robot. 
    """
    if not is_position_safe(start_x, start_y, M, N, grid):
        return -1, []
    if not is_position_safe(end_x, end_y, M, N, grid):
        return -1, []

    start_dir = dir_map[start_dir]
    start = (start_x, start_y, start_dir, 0, [])  # x, y, dir, time, commands

    visited = set()
    visited.add((start_x, start_y, start_dir))
    queue = deque([start])

    turn_order = ["G", "D"]
    step_order = [1, 2, 3]

    while queue:
        x, y, d, time, commands = queue.popleft()

        if (x, y) == (end_x, end_y):
            return time, commands

        # Actions de rotation
        for action in turn_order:
            if action == "D":
                nd = (d + 1) % 4
            else:
                nd = (d - 1) % 4

            state_id = (x, y, nd)
            if state_id not in visited:
                visited.add(state_id)
                queue.append((x, y, nd, time + 1, commands + [action]))

        # Actions d'avancement
        dx, dy = dirs[d]
        for steps in step_order:
            nx = x + dx * steps
            ny = y + dy * steps

            # Vérifie chaque case intermédiaire
            valid = True
            for s in range(1, steps + 1):
                check_x = x + dx * s
                check_y = y + dy * s
                if not is_position_safe(check_x, check_y, M, N, grid):
                    valid = False
                    break

            if not valid or nx < 0 or nx > M or ny < 0 or ny > N:
                continue

            state_id = (nx, ny, d)
            if state_id not in visited:
                visited.add(state_id)
                queue.append((nx, ny, d, time + 1, commands + [f"a{steps}"]))

    return -1, []

def dijkstra(M, N, grid, start_x, start_y, end_x, end_y, start_dir):
    """
    Implémente l'algorithme de Dijkstra pour trouver le chemin optimal du robot.
    """
    if not is_position_safe(start_x, start_y, M, N, grid):
        return -1, []
    if not is_position_safe(end_x, end_y, M, N, grid):
        return -1, []
    
    start_dir = dir_map[start_dir]
    start = (start_x, start_y, start_dir)

    pq = [(0, start_x, start_y, start_dir, [])]
    dist = {start: 0}

    turn_order = ["G", "D"]
    step_order = [1, 2, 3]

    while pq:
        cost, x, y, d, commands = heapq.heappop(pq)
        state = (x, y, d)

        if cost > dist[state]:
            continue

        if (x, y) == (end_x, end_y):
            return cost, commands

        # Actions de rotation
        for action in turn_order:
            if action == "D":
                nd = (d + 1) % 4
            else:
                nd = (d - 1) % 4

            ns = (x, y, nd)
            new_cost = cost + 1
            new_commands = commands + [action]

            if ns not in dist or new_cost < dist[ns]:
                dist[ns] = new_cost
                heapq.heappush(pq, (new_cost, x, y, nd, new_commands))

        # Actions d'avancement
        for steps in step_order:
            dx, dy = dirs[d]
            nx = x + dx * steps
            ny = y + dy * steps

            valid = True
            for s in range(1, steps + 1):
                check_x, check_y = x + dx * s, y + dy * s
                if not is_position_safe(check_x, check_y, M, N, grid):
                    valid = False
                    break

            if not valid or nx < 0 or nx > M or ny < 0 or ny > N:
                continue

            ns = (nx, ny, d)
            new_cost = cost + 1
            new_commands = commands + [f"a{steps}"]

            if ns not in dist or new_cost < dist[ns]:
                dist[ns] = new_cost
                heapq.heappush(pq, (new_cost, nx, ny, d, new_commands))

    return -1, []

def bellman_robot_path(M, N, grid, start_x, start_y, end_x, end_y, start_dir):
    """
    Implémentation de l'algorithme de Bellman (programmation dynamique)
    pour trouver le chemin optimal du robot.
    """
    if not is_position_safe(start_x, start_y, M, N, grid):
        return -1, []
    if not is_position_safe(end_x, end_y, M, N, grid):
        return -1, []
    
    start_dir = dir_map[start_dir]
    
    # Initialisation des tables DP
    dp = [[[ (float('inf'), None, None) for _ in range(4)] 
           for _ in range(N+1)] for _ in range(M+1)]
    
    # Table pour reconstruire le chemin
    prev = [[[ None for _ in range(4)] for _ in range(N+1)] for _ in range(M+1)]
    
    # Initialisation de l'état de départ
    dp[start_x][start_y][start_dir] = (0, None, None)
    
    # Algorithme de Bellman - relâchement des arcs
    changed = True
    iteration = 0
    max_iterations = (M+1) * (N+1) * 4 * 5
    
    while changed and iteration < max_iterations:
        changed = False
        iteration += 1
        
        # Parcours de tous les états possibles
        for x in range(M+1):
            for y in range(N+1):
                for d in range(4):
                    current_time, _, _ = dp[x][y][d]
                    
                    if current_time == float('inf'):
                        continue
                    
                    # Actions de rotation
                    for turn, new_d in [("G", (d-1)%4), ("D", (d+1)%4)]:
                        new_time = current_time + 1
                        
                        if new_time < dp[x][y][new_d][0]:
                            dp[x][y][new_d] = (new_time, turn, (x, y, d))
                            prev[x][y][new_d] = (x, y, d, turn)
                            changed = True
                    
                    # Actions d'avancement
                    for steps in [1, 2, 3]:
                        dx, dy = dirs[d]
                        new_x = x + dx * steps
                        new_y = y + dy * steps
                        
                        # Vérification du chemin
                        valid = True
                        for s in range(1, steps + 1):
                            check_x, check_y = x + dx * s, y + dy * s
                            if not is_position_safe(check_x, check_y, M, N, grid):
                                valid = False
                                break
                        
                        if not valid or new_x < 0 or new_x > M or new_y < 0 or new_y > N:
                            continue
                        
                        new_time = current_time + 1
                        action = f"a{steps}"
                        
                        if new_time < dp[new_x][new_y][d][0]:
                            dp[new_x][new_y][d] = (new_time, action, (x, y, d))
                            prev[new_x][new_y][d] = (x, y, d, action)
                            changed = True
    
    # Recherche de la solution optimale
    best_time = float('inf')
    best_state = None
    
    for d in range(4):
        time_val, _, _ = dp[end_x][end_y][d]
        if time_val < best_time:
            best_time = time_val
            best_state = (end_x, end_y, d)
    
    if best_time == float('inf'):
        return -1, []
    
    # Reconstruction du chemin
    commands = []
    current_state = best_state
    
    while current_state != (start_x, start_y, start_dir):
        x, y, d = current_state
        prev_info = prev[x][y][d]
        
        if prev_info is None:
            break
            
        prev_x, prev_y, prev_d, command = prev_info
        commands.append(command)
        current_state = (prev_x, prev_y, prev_d)
    
    commands.reverse()
    return best_time, commands

# ==================== FONCTIONS POUR LES TESTS ====================

def generate_random_instance(size, num_obstacles):
    """
    Génère une instance aléatoire pour les tests de performance.
    """
    M = N = size
    grid = [[0 for _ in range(N)] for _ in range(M)]
    
    # Placement des obstacles
    obstacles_placed = 0
    while obstacles_placed < num_obstacles:
        i = random.randint(0, M-1)
        j = random.randint(0, N-1)
        if grid[i][j] == 0:
            grid[i][j] = 1
            obstacles_placed += 1
    
    # Génération des points valides
    directions = ["nord", "est", "sud", "ouest"]
    
    # Point de départ
    while True:
        start_x = random.randint(0, M)
        start_y = random.randint(0, N)
        if is_position_safe(start_x, start_y, M, N, grid):
            break
    
    # Point d'arrivée
    while True:
        end_x = random.randint(0, M)
        end_y = random.randint(0, N)
        if is_position_safe(end_x, end_y, M, N, grid) and (start_x, start_y) != (end_x, end_y):
            break
    
    start_dir = random.choice(directions)
    
    return M, N, grid, start_x, start_y, end_x, end_y, start_dir

def write_instance_to_file(f, M, N, grid, start_x, start_y, end_x, end_y, start_dir):
    """
    Écrit une instance dans le fichier au format demandé.
    """
    f.write(f"{M} {N}\n")
    for i in range(M):
        f.write(" ".join(str(grid[i][j]) for j in range(N)) + "\n")
    f.write(f"{start_x} {start_y} {end_x} {end_y} {start_dir}\n")

# ==================== TESTS DE PERFORMANCE (c) ====================

def run_size_performance_tests():
    """
    (c) Tests de performance en fonction de la taille de la grille
    """
    algorithms = {
        'BFS': solve_bfs,
        'Dijkstra': dijkstra,
        'Bellman': bellman_robot_path
    }
    
    sizes = [10, 20, 30, 40, 50]
    num_tests_per_size = 10
    
    print("Génération des instances pour les tests de taille...")
    
    # Chemins des fichiers
    instances_file = os.path.join(INSTANCES_DIR, "instances_taille.txt")
    resultats_detaille_file = os.path.join(RESULTATS_DIR, "resultats_detaille_taille.txt")
    graphique_file = os.path.join(GRAPHIQUES_DIR, "performance_taille.png")
    resultats_moyens_file = os.path.join(RESULTATS_DIR, "resultats_moyens_taille.txt")
    
    # Génération des instances
    with open(instances_file, 'w') as f:
        for size in sizes:
            num_obstacles = size
            for instance_num in range(num_tests_per_size):
                M, N, grid, sx, sy, ex, ey, start_dir = generate_random_instance(size, num_obstacles)
                write_instance_to_file(f, M, N, grid, sx, sy, ex, ey, start_dir)
        f.write("0 0\n")
    
    print("Exécution des tests de performance...")
    
    # Fichier pour les résultats détaillés
    with open(resultats_detaille_file, 'w') as f_det:
        f_det.write("Taille | Instance | Algorithme | Temps (s) | Solution | Commandes\n")
        f_det.write("-------|----------|------------|-----------|----------|----------\n")
    
    results = {algo: [] for algo in algorithms}
    detailed_results = {algo: {size: [] for size in sizes} for algo in algorithms}
    
    # Lecture et traitement des instances
    with open(instances_file, 'r') as f:
        data = f.read().strip().split('\n')
    
    idx = 0
    instance_counter = 0
    
    while idx < len(data):
        line = data[idx]
        if line == "0 0":
            break
        
        M, N = map(int, line.split())
        current_size = M
        
        grid = []
        for i in range(M):
            idx += 1
            grid.append(list(map(int, data[idx].split())))
        
        idx += 1
        parts = data[idx].split()
        sx, sy, ex, ey = map(int, parts[:4])
        start_dir = parts[4]
        
        instance_counter += 1
        
        # Tests pour chaque algorithme
        for algo_name, algo_func in algorithms.items():
            start_time = time.time()
            time_result, commands = algo_func(M, N, grid, sx, sy, ex, ey, start_dir)
            end_time = time.time()
            
            exec_time = end_time - start_time
            detailed_results[algo_name][current_size].append(exec_time)
            
            # Écriture des résultats détaillés
            with open(resultats_detaille_file, 'a') as f_det:
                solution_str = f"{time_result}" if time_result != -1 else "-1"
                commands_str = ' '.join(commands) if commands else "Aucun chemin"
                f_det.write(f"{current_size:6} | {instance_counter:8} | {algo_name:10} | {exec_time:.6f} | {solution_str:8} | {commands_str}\n")
        
        idx += 1
    
    # Calcul des moyennes
    for algo in algorithms:
        for size in sizes:
            if detailed_results[algo][size]:
                avg_time = sum(detailed_results[algo][size]) / len(detailed_results[algo][size])
                results[algo].append((size, avg_time))
    
    # Affichage des résultats moyens
    print("\n=== RÉSULTATS MOYENS TESTS TAILLE ===")
    print("Taille | BFS (s)     | Dijkstra (s) | Bellman (s)")
    print("-------|-------------|-------------|-------------")
    for i in range(len(sizes)):
        size = sizes[i]
        bfs_time = results['BFS'][i][1] if i < len(results['BFS']) else 0
        dijkstra_time = results['Dijkstra'][i][1] if i < len(results['Dijkstra']) else 0
        bellman_time = results['Bellman'][i][1] if i < len(results['Bellman']) else 0
        print(f"{size:6} | {bfs_time:.6f}   | {dijkstra_time:.6f}   | {bellman_time:.6f}")
    
    # Génération du graphique
    plt.figure(figsize=(10, 6))
    for algo in algorithms:
        sizes_plot = [size for size, _ in results[algo]]
        times_plot = [time for _, time in results[algo]]
        plt.plot(sizes_plot, times_plot, marker='o', label=algo)
    
    plt.xlabel('Taille de la grille (N × N)')
    plt.ylabel('Temps d\'exécution moyen (s)')
    plt.title('Performance des algorithmes en fonction de la taille de la grille')
    plt.legend()
    plt.grid(True)
    plt.savefig(graphique_file)
    print(f"\nGraphique sauvegardé dans '{graphique_file}'")
    
    # Sauvegarde des résultats moyens
    with open(resultats_moyens_file, 'w') as f:
        f.write("Taille | BFS (s) | Dijkstra (s) | Bellman (s)\n")
        f.write("-------|---------|-------------|------------\n")
        for i in range(len(sizes)):
            size = sizes[i]
            bfs_time = results['BFS'][i][1] if i < len(results['BFS']) else 0
            dijkstra_time = results['Dijkstra'][i][1] if i < len(results['Dijkstra']) else 0
            bellman_time = results['Bellman'][i][1] if i < len(results['Bellman']) else 0
            f.write(f"{size:6} | {bfs_time:.6f} | {dijkstra_time:.6f}   | {bellman_time:.6f}\n")
    
    print(f"Résultats détaillés sauvegardés dans '{resultats_detaille_file}'")
    print(f"Résultats moyens sauvegardés dans '{resultats_moyens_file}'")
    print(f"Fichier d'instances sauvegardé dans '{instances_file}'")
    
    return results

# ==================== TESTS DE PERFORMANCE (d) ====================

def run_obstacle_performance_tests():
    """
    (d) Tests de performance en fonction du nombre d'obstacles
    """
    algorithms = {
        'BFS': solve_bfs,
        'Dijkstra': dijkstra,
        'Bellman': bellman_robot_path
    }
    
    M = N = 20  # Taille fixe
    obstacle_counts = [10, 20, 30, 40, 50]
    num_tests_per_count = 10
    
    print("Génération des instances pour les tests d'obstacles...")
    
    # Chemins des fichiers
    instances_file = os.path.join(INSTANCES_DIR, "instances_obstacles.txt")
    resultats_detaille_file = os.path.join(RESULTATS_DIR, "resultats_detaille_obstacles.txt")
    graphique_file = os.path.join(GRAPHIQUES_DIR, "performance_obstacles.png")
    resultats_moyens_file = os.path.join(RESULTATS_DIR, "resultats_moyens_obstacles.txt")
    
    # Génération des instances
    with open(instances_file, 'w') as f:
        for num_obstacles in obstacle_counts:
            for instance_num in range(num_tests_per_count):
                _, _, grid, sx, sy, ex, ey, start_dir = generate_random_instance(M, num_obstacles)
                write_instance_to_file(f, M, N, grid, sx, sy, ex, ey, start_dir)
        f.write("0 0\n")
    
    print("Exécution des tests de performance...")
    
    # Fichier pour les résultats détaillés
    with open(resultats_detaille_file, 'w') as f_det:
        f_det.write("Obstacles | Instance | Algorithme | Temps (s) | Solution | Commandes\n")
        f_det.write("----------|----------|------------|-----------|----------|----------\n")
    
    results = {algo: [] for algo in algorithms}
    detailed_results = {algo: {obs: [] for obs in obstacle_counts} for algo in algorithms}
    
    # Lecture et traitement des instances
    with open(instances_file, 'r') as f:
        data = f.read().strip().split('\n')
    
    idx = 0
    instance_counter = 0
    
    while idx < len(data):
        line = data[idx]
        if line == "0 0":
            break
        
        M, N = map(int, line.split())
        grid = []
        for i in range(M):
            idx += 1
            grid.append(list(map(int, data[idx].split())))
        
        # Compter les obstacles
        obstacle_count = sum(sum(row) for row in grid)
        
        idx += 1
        parts = data[idx].split()
        sx, sy, ex, ey = map(int, parts[:4])
        start_dir = parts[4]
        
        instance_counter += 1
        
        # Tests pour chaque algorithme
        for algo_name, algo_func in algorithms.items():
            start_time = time.time()
            time_result, commands = algo_func(M, N, grid, sx, sy, ex, ey, start_dir)
            end_time = time.time()
            
            exec_time = end_time - start_time
            detailed_results[algo_name][obstacle_count].append(exec_time)
            
            # Écriture des résultats détaillés
            with open(resultats_detaille_file, 'a') as f_det:
                solution_str = f"{time_result}" if time_result != -1 else "-1"
                commands_str = ' '.join(commands) if commands else "Aucun chemin"
                f_det.write(f"{obstacle_count:9} | {instance_counter:8} | {algo_name:10} | {exec_time:.6f} | {solution_str:8} | {commands_str}\n")
        
        idx += 1
    
    # Calcul des moyennes
    for algo in algorithms:
        for obs_count in obstacle_counts:
            if detailed_results[algo][obs_count]:
                avg_time = sum(detailed_results[algo][obs_count]) / len(detailed_results[algo][obs_count])
                results[algo].append((obs_count, avg_time))
    
    # Affichage des résultats moyens
    print("\n=== RÉSULTATS MOYENS TESTS OBSTACLES ===")
    print("Obstacles | BFS (s)    | Dijkstra (s) | Bellman (s)")
    print("----------|------------|-------------|-------------")
    for i in range(len(obstacle_counts)):
        obs = obstacle_counts[i]
        bfs_time = results['BFS'][i][1] if i < len(results['BFS']) else 0
        dijkstra_time = results['Dijkstra'][i][1] if i < len(results['Dijkstra']) else 0
        bellman_time = results['Bellman'][i][1] if i < len(results['Bellman']) else 0
        print(f"{obs:9} | {bfs_time:.6f}  | {dijkstra_time:.6f}   | {bellman_time:.6f}")
    
    # Génération du graphique
    plt.figure(figsize=(10, 6))
    for algo in algorithms:
        obstacles_plot = [obs for obs, _ in results[algo]]
        times_plot = [time for _, time in results[algo]]
        plt.plot(obstacles_plot, times_plot, marker='s', label=algo)
    
    plt.xlabel('Nombre d\'obstacles')
    plt.ylabel('Temps d\'exécution moyen (s)')
    plt.title('Performance des algorithmes en fonction du nombre d\'obstacles (grille 20×20)')
    plt.legend()
    plt.grid(True)
    plt.savefig(graphique_file)
    print(f"\nGraphique sauvegardé dans '{graphique_file}'")
    
    # Sauvegarde des résultats moyens
    with open(resultats_moyens_file, 'w') as f:
        f.write("Obstacles | BFS (s) | Dijkstra (s) | Bellman (s)\n")
        f.write("----------|---------|-------------|------------\n")
        for i in range(len(obstacle_counts)):
            obs = obstacle_counts[i]
            bfs_time = results['BFS'][i][1] if i < len(results['BFS']) else 0
            dijkstra_time = results['Dijkstra'][i][1] if i < len(results['Dijkstra']) else 0
            bellman_time = results['Bellman'][i][1] if i < len(results['Bellman']) else 0
            f.write(f"{obs:9} | {bfs_time:.6f} | {dijkstra_time:.6f}   | {bellman_time:.6f}\n")
    
    print(f"Résultats détaillés sauvegardés dans '{resultats_detaille_file}'")
    print(f"Résultats moyens sauvegardés dans '{resultats_moyens_file}'")
    print(f"Fichier d'instances sauvegardé dans '{instances_file}'")
    
    return results

# ==================== GÉNÉRATION AVEC CONTRAINTES ET GUROBI (e) ====================

def generate_constrained_grid_heuristic(M, N, P):
    """
    Méthode heuristique pour générer une grille avec contraintes lorsque Gurobi n'est pas disponible.
    
    Cette méthode utilise une approche aléatoire guidée par les contraintes pour placer les obstacles.
    
    Retourne:
    - Une grille valide si une solution existe (None sinon)
    
    Contraintes vérifiées:
    1. Exactement P obstacles au total
    2. Au plus max_per_row = floor(2P/M) obstacles par ligne
    3. Au plus max_per_col = floor(2P/N) obstacles par colonne
    4. Aucune séquence "101" (obstacle-espace-obstacle) dans aucune ligne ou colonne
    """
    # =============================================
    # 1. VÉRIFICATION INITIALE DE FAISABILITÉ
    # =============================================
    if P < 0 or P > M * N:
        print(f"ERREUR: P={P} doit être entre 0 et {M*N}")
        return None
    
    # Cas trivial: P = 0 (grille vide)
    if P == 0:
        return [[0 for _ in range(N)] for _ in range(M)]
    
    # Calcul des limites selon l'énoncé (division entière)
    max_per_row = (2 * P) // M
    max_per_col = (2 * P) // N
    
    # =============================================
    # 2. VÉRIFICATION PRÉALABLE DES CONTRAINTES
    # =============================================
    print(f"\nPARAMÈTRES HEURISTIQUES:")
    print(f"  Taille: {M}x{N}, Obstacles: {P}")
    print(f"  Max par ligne: {max_per_row} (2P/M = {2*P/M:.2f})")
    print(f"  Max par colonne: {max_per_col} (2P/N = {2*P/N:.2f})")
    
    # Vérification si les contraintes sont trop strictes (avertissement seulement)
    if P > 0 and (max_per_row == 0 or max_per_col == 0):
        print("\nATTENTION: Contraintes très strictes!")
        print(f"  max_per_row={max_per_row}, max_per_col={max_per_col}")
        print("  Cela peut rendre le problème infaisable.")
    
    # =============================================
    # 3. INITIALISATION DES STRUCTURES DE DONNÉES
    # =============================================
    grid = [[0 for _ in range(N)] for _ in range(M)]
    row_counts = [0] * M  # Nombre d'obstacles par ligne
    col_counts = [0] * N  # Nombre d'obstacles par colonne
    
    obstacles_placed = 0
    max_attempts = M * N * 20  # Nombre maximum de tentatives
    attempts = 0
    
    # =============================================
    # 4. PLACEMENT HEURISTIQUE DES OBSTACLES
    # =============================================
    print(f"\nDÉBUT DE LA GÉNÉRATION HEURISTIQUE...")
    start_time = time.time()
    
    while obstacles_placed < P and attempts < max_attempts:
        attempts += 1
        
        # Choix aléatoire d'une position
        i = random.randint(0, M-1)
        j = random.randint(0, N-1)
        
        # Vérifier si la position est disponible
        if grid[i][j] == 1:
            continue  # Case déjà occupée
        
        # =============================================
        # 4.1 VÉRIFICATION DES CONTRAINTES DE BASE
        # =============================================
        # Vérification des limites par ligne et colonne
        if row_counts[i] >= max_per_row:
            continue  # Ligne déjà saturée
        
        if col_counts[j] >= max_per_col:
            continue  # Colonne déjà saturée
        
        # =============================================
        # 4.2 VÉRIFICATION DES CONTRAINTES "101"
        # =============================================
        valid_position = True
        
        # Vérification horizontale
        # 1. Éviter de créer un motif 1-0-1 en plaçant un obstacle
        if j >= 2:
            # Motif: 1-0-? (où ? serait le nouvel obstacle)
            if grid[i][j-2] == 1 and grid[i][j-1] == 0:
                valid_position = False
        
        if j <= N-3:
            # Motif: ?-0-1 (où ? serait le nouvel obstacle)
            if grid[i][j+1] == 0 and grid[i][j+2] == 1:
                valid_position = False
        
        # 2. Éviter de compléter un motif 1-0-1 existant
        if j >= 1 and j <= N-2:
            # Motif: 1-?-1
            if grid[i][j-1] == 1 and grid[i][j+1] == 1:
                valid_position = False
        
        # Vérification verticale
        # 1. Éviter de créer un motif 1-0-1 en plaçant un obstacle
        if i >= 2:
            # Motif: 1-0-? (où ? serait le nouvel obstacle)
            if grid[i-2][j] == 1 and grid[i-1][j] == 0:
                valid_position = False
        
        if i <= M-3:
            # Motif: ?-0-1 (où ? serait le nouvel obstacle)
            if grid[i+1][j] == 0 and grid[i+2][j] == 1:
                valid_position = False
        
        # 2. Éviter de compléter un motif 1-0-1 existant
        if i >= 1 and i <= M-2:
            # Motif: 1-?-1
            if grid[i-1][j] == 1 and grid[i+1][j] == 1:
                valid_position = False
        
        # =============================================
        # 4.3 PLACEMENT DE L'OBSTACLE SI VALIDE
        # =============================================
        if valid_position:
            grid[i][j] = 1
            row_counts[i] += 1
            col_counts[j] += 1
            obstacles_placed += 1
            
            # Feedback visuel pour les grandes grilles
            if obstacles_placed % max(1, P // 10) == 0:
                print(f"  Progression: {obstacles_placed}/{P} obstacles placés")
    
    end_time = time.time()
    print(f"FIN DE LA GÉNÉRATION HEURISTIQUE ({end_time - start_time:.2f}s)")
    
    # =============================================
    # 5. VÉRIFICATION COMPLÈTE DE TOUTES LES CONTRAINTES
    # =============================================
    print(f"\nVÉRIFICATION DES CONTRAINTES...")
    
    # 5.1 Vérification du nombre total d'obstacles
    total_obstacles = sum(sum(row) for row in grid)
    if total_obstacles != P:
        print(f" ERREUR: Nombre total d'obstacles incorrect")
        print(f"   Attendu: {P}, Trouvé: {total_obstacles}")
        return None
    
    print(f" Obstacles totaux: {P}/{P}")
    
    # 5.2 Vérification des contraintes par ligne
    row_violations = []
    for i in range(M):
        row_count = sum(grid[i])
        if row_count > max_per_row:
            row_violations.append((i, row_count, max_per_row))
    
    if row_violations:
        print(f" ERREUR: Contraintes de ligne violées")
        for i, count, max_allowed in row_violations[:3]:  # Affiche seulement 3 violations
            print(f"   Ligne {i}: {count} obstacles, max autorisé = {max_allowed}")
        if len(row_violations) > 3:
            print(f"   ... et {len(row_violations) - 3} autres violations")
        return None
    
    print(f" Contraintes par ligne: respectées (max {max_per_row})")
    
    # 5.3 Vérification des contraintes par colonne
    col_violations = []
    for j in range(N):
        col_count = sum(grid[i][j] for i in range(M))
        if col_count > max_per_col:
            col_violations.append((j, col_count, max_per_col))
    
    if col_violations:
        print(f" ERREUR: Contraintes de colonne violées")
        for j, count, max_allowed in col_violations[:3]:
            print(f"   Colonne {j}: {count} obstacles, max autorisé = {max_allowed}")
        if len(col_violations) > 3:
            print(f"   ... et {len(col_violations) - 3} autres violations")
        return None
    
    print(f" Contraintes par colonne: respectées (max {max_per_col})")
    
    # 5.4 Vérification des contraintes "101"
    violations_101 = []
    
    # Vérification horizontale
    for i in range(M):
        for j in range(N-2):
            if grid[i][j] == 1 and grid[i][j+1] == 0 and grid[i][j+2] == 1:
                violations_101.append(("horizontal", i, j))
    
    # Vérification verticale
    for j in range(N):
        for i in range(M-2):
            if grid[i][j] == 1 and grid[i+1][j] == 0 and grid[i+2][j] == 1:
                violations_101.append(("vertical", i, j))
    
    if violations_101:
        print(f" ERREUR: Contraintes 101 violées")
        for direction, i, j in violations_101[:3]:
            if direction == "horizontal":
                print(f"   Horizontal: ({i},{j})-({i},{j+1})-({i},{j+2}) = 1-0-1")
            else:
                print(f"   Vertical: ({i},{j})-({i+1},{j})-({i+2},{j}) = 1-0-1")
        if len(violations_101) > 3:
            print(f"   ... et {len(violations_101) - 3} autres violations")
        return None
    
    print(f"Contraintes 101: aucune violation")
    
    # =============================================
    # 6. RÉSUMÉ FINAL
    # =============================================
    print(f"\n GRILLE HEURISTIQUE VALIDE GÉNÉRÉE")
    print(f"   Taille: {M}x{N}")
    print(f"   Obstacles: {P} ({P/(M*N)*100:.1f}% de la grille)")
    print(f"   Taux de remplissage moyen par ligne: {total_obstacles/M:.1f}/{max_per_row}")
    print(f"   Taux de remplissage moyen par colonne: {total_obstacles/N:.1f}/{max_per_col}")
    print(f"   Temps de génération: {end_time - start_time:.2f}s")
    
    return grid

def generate_constrained_grid_gurobi_with_weights(M, N, P):
    """
    (e) Génère une grille avec contraintes en utilisant Gurobi pour résoudre le programme linéaire
    et retourne également la matrice des poids aléatoires
    
    Retourne:
    - Une grille valide si une solution existe
    - La matrice des poids aléatoires (0-1000) utilisée
    - None si aucune solution n'existe avec les contraintes données
    
    Note: Cette fonction tente d'utiliser Gurobi. Si Gurobi n'est pas disponible (non installé ou
    licence expirée), elle utilise une méthode heuristique comme solution de repli.
    """
    
    # Vérification initiale: Gurobi est-il installé et importé avec succès?
    if not GUROBI_AVAILABLE:
        print("Gurobi n'est pas installé. Utilisation de la méthode heuristique.")
        # Utilisation de la méthode heuristique comme solution de repli
        grid = generate_constrained_grid_heuristic(M, N, P)
        # Pour la méthode heuristique, nous générons aussi des poids aléatoires
        # pour maintenir la cohérence avec l'interface de retour
        if grid is not None:
            weights = [[random.randint(0, 1000) for _ in range(N)] for _ in range(M)]
            return grid, weights
        return None, None
    
    # Gurobi est installé, nous tentons de l'utiliser
    # Mais nous devons gérer les erreurs potentielles (licence expirée, etc.)
    try:
        # Première étape: tester si Gurobi fonctionne correctement (y compris la licence)
        # en créant un modèle minimal et en l'optimisant
        test_model = gp.Model("TestModel")
        test_model.setParam('OutputFlag', 0)
        test_model.addVar(vtype=GRB.BINARY, name="test_var")
        test_model.optimize()
        
        # Si aucune exception n'est levée ci-dessus, Gurobi fonctionne correctement
        
        # Création du modèle principal pour la génération de grille
        model = gp.Model("GridGeneration")
        
        # Variables de décision: x[i][j] = 1 si la case (i,j) contient un obstacle
        x = {}
        for i in range(M):
            for j in range(N):
                x[i,j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
        
        # Génération de poids aléatoires entre 0 et 1000 pour chaque case
        # Ces poids sont utilisés dans la fonction objectif pour sélectionner
        # les obstacles ayant les poids les plus bas
        weights = [[0] * N for _ in range(M)]
        for i in range(M):
            for j in range(N):
                weights[i][j] = random.randint(0, 1000)
        
        # Fonction objectif: minimiser la somme des poids des cases sélectionnées comme obstacles
        # Cela signifie que nous préférons placer des obstacles sur des cases avec des poids faibles
        model.setObjective(
            gp.quicksum(weights[i][j] * x[i,j] for i in range(M) for j in range(N)),
            GRB.MINIMIZE
        )
        
        # Contrainte principale: exactement P obstacles dans la grille
        model.addConstr(
            gp.quicksum(x[i,j] for i in range(M) for j in range(N)) == P,
            "total_obstacles"
        )
        
        # Calcul des contraintes selon l'énoncé:
        # - maximum par ligne = floor(2P/M) (division entière)
        # - maximum par colonne = floor(2P/N) (division entière)
        max_per_row = (2 * P) // M
        max_per_col = (2 * P) // N
        
        # Contraintes: limite du nombre d'obstacles par ligne (2P/M maximum par ligne)
        for i in range(M):
            model.addConstr(
                gp.quicksum(x[i,j] for j in range(N)) <= max_per_row,
                f"row_limit_{i}"
            )
        
        # Contraintes: limite du nombre d'obstacles par colonne (2P/N maximum par colonne)
        for j in range(N):
            model.addConstr(
                gp.quicksum(x[i,j] for i in range(M)) <= max_per_col,
                f"col_limit_{j}"
            )
        
        # Contraintes pour éviter la séquence "101" (obstacle-espace-obstacle)
        # Ces contraintes empêchent d'avoir deux obstacles séparés par exactement une case vide
        # Horizontalement: pour chaque ligne i et chaque colonne j (sauf les deux dernières colonnes)
        for i in range(M):
            for j in range(N-2):
                # Contrainte: x[i,j] + x[i,j+2] ≤ 1 + x[i,j+1]
                # Si x[i,j+1] = 0 (case vide au milieu), alors x[i,j] + x[i,j+2] ≤ 1
                # (interdit d'avoir deux obstacles avec une case vide entre eux)
                # Si x[i,j+1] = 1 (obstacle au milieu), alors la contrainte est relâchée
                model.addConstr(
                    x[i,j] + x[i,j+2] <= 1 + x[i,j+1],
                    f"no_101_horizontal_{i}_{j}"
                )
        
        # Verticalement: pour chaque colonne j et chaque ligne i (sauf les deux dernières lignes)
        for j in range(N):
            for i in range(M-2):
                # Même logique que pour les contraintes horizontales
                model.addConstr(
                    x[i,j] + x[i+2,j] <= 1 + x[i+1,j],
                    f"no_101_vertical_{i}_{j}"
                )
        
        # Configuration du solveur: désactiver la sortie détaillée pour un affichage plus propre
        model.setParam('OutputFlag', 0)
        # Lancement de la résolution du problème d'optimisation
        model.optimize()
        
        # Analyse du statut de la solution retournée par Gurobi
        if model.status == GRB.OPTIMAL:
            # Une solution optimale a été trouvée
            # Construction de la grille à partir des valeurs des variables
            grid = [[0 for _ in range(N)] for _ in range(M)]
            for i in range(M):
                for j in range(N):
                    # Si la valeur de la variable est > 0.5, on considère qu'il y a un obstacle
                    if x[i,j].x > 0.5:
                        grid[i][j] = 1
            
            # ============================================================
            # VÉRIFICATION COMPLÈTE DE TOUTES LES CONTRAINTES
            # ============================================================
            
            # 1. Vérification du nombre total d'obstacles
            total_obstacles = sum(sum(row) for row in grid)
            if total_obstacles != P:
                print(f"ERREUR: Nombre total d'obstacles incorrect.")
                print(f"  Attendu: {P}, Trouvé: {total_obstacles}")
                return None, None
            
            # 2. Vérification des contraintes par ligne
            for i in range(M):
                row_count = sum(grid[i])
                if row_count > max_per_row:
                    print(f"ERREUR: Contrainte de ligne violée.")
                    print(f"  Ligne {i}: {row_count} obstacles, max autorisé = {max_per_row}")
                    return None, None
            
            # 3. Vérification des contraintes par colonne
            for j in range(N):
                col_count = sum(grid[i][j] for i in range(M))
                if col_count > max_per_col:
                    print(f"ERREUR: Contrainte de colonne violée.")
                    print(f"  Colonne {j}: {col_count} obstacles, max autorisé = {max_per_col}")
                    return None, None
            
            # 4. Vérification des contraintes "101" (obstacle-espace-obstacle)
            # Vérification horizontale
            for i in range(M):
                for j in range(N-2):
                    if grid[i][j] == 1 and grid[i][j+1] == 0 and grid[i][j+2] == 1:
                        print(f"ERREUR: Contrainte 101 horizontale violée.")
                        print(f"  Position: ({i},{j})-({i},{j+1})-({i},{j+2})")
                        print(f"  Valeurs: 1-0-1 (interdit)")
                        return None, None
            
            # Vérification verticale
            for j in range(N):
                for i in range(M-2):
                    if grid[i][j] == 1 and grid[i+1][j] == 0 and grid[i+2][j] == 1:
                        print(f"ERREUR: Contrainte 101 verticale violée.")
                        print(f"  Position: ({i},{j})-({i+1},{j})-({i+2},{j})")
                        print(f"  Valeurs: 1-0-1 (interdit)")
                        return None, None
            
            # Si toutes les vérifications passent, la grille est valide
            print(f"VÉRIFICATION: Toutes les contraintes sont respectées")
            print(f"  - Obstacles totaux: {P}/{P}")
            print(f"  - Max par ligne: {max_per_row} (respecté)")
            print(f"  - Max par colonne: {max_per_col} (respecté)")
            print(f"  - Contraintes 101: aucune violation")
            
            return grid, weights
        
        elif model.status == GRB.INFEASIBLE:
            # Le problème n'a pas de solution réalisable avec les contraintes données
            print("Le problème est infaisable avec les contraintes données.")
            print(f"  M={M}, N={N}, P={P}")
            print(f"  Max par ligne: {max_per_row} (2P/M = {2*P/M:.2f})")
            print(f"  Max par colonne: {max_per_col} (2P/N = {2*P/N:.2f})")
            return None, None
        
        else:
            # Autre statut (par exemple, temps limite dépassé, interruption utilisateur, etc.)
            print(f"Gurobi n'a pas trouvé de solution optimale. Statut: {model.status}")
            return None, None
            
    except (gp.GurobiError, AttributeError, NameError) as e:
        # Capture des erreurs spécifiques à Gurobi, y compris les problèmes de licence
        # AttributeError et NameError peuvent survenir si l'importation a échoué partiellement
        print(f"Erreur Gurobi (peut-être une licence expirée ou non configurée): {e}")
        print("Utilisation de la méthode heuristique à la place.")
        
        # Solution de repli: utiliser la méthode heuristique
        grid = generate_constrained_grid_heuristic(M, N, P)
        if grid is not None:
            # Génération de poids aléatoires pour la méthode heuristique également
            weights = [[random.randint(0, 1000) for _ in range(N)] for _ in range(M)]
            return grid, weights
        return None, None
    
    except Exception as e:
        # Capture de toute autre exception inattendue
        print(f"Erreur inattendue avec Gurobi: {e}")
        print("Utilisation de la méthode heuristique à la place.")
        
        # Solution de repli: utiliser la méthode heuristique
        grid = generate_constrained_grid_heuristic(M, N, P)
        if grid is not None:
            weights = [[random.randint(0, 1000) for _ in range(N)] for _ in range(M)]
            return grid, weights
        return None, None

def display_weights(weights, M, N, grid):
    """
    Affiche la matrice des poids aléatoires de manière lisible
    """
    print("\n" + "="*60)
    print("MATRICE DES POIDS ALÉATOIRES (0-1000)")
    print("="*60)
    
    # Affiche l'en-tête des colonnes
    header = "      "
    for j in range(N):
        header += f"{j:5d}"
    print(header)
    print("      " + "-" * (5*N))
    
    # Affiche chaque ligne avec les poids
    for i in range(M):
        row_str = f"{i:3d}:  "
        for j in range(N):
            # Si la case contient un obstacle, on l'entoure de crochets
            if grid[i][j] == 1:
                row_str += f"[{weights[i][j]:3d}] "
            else:
                row_str += f" {weights[i][j]:3d}  "
        print(row_str)
    
    # Affiche les statistiques
    print("\n" + "="*60)
    print("STATISTIQUES DES POIDS:")
    
    # Tous les poids
    all_weights = [weights[i][j] for i in range(M) for j in range(N)]
    print(f"  Tous les poids: min={min(all_weights)}, max={max(all_weights)}, "
          f"moyenne={sum(all_weights)/len(all_weights):.1f}")
    
    # Poids des obstacles
    obstacle_weights = []
    obstacle_positions = []
    for i in range(M):
        for j in range(N):
            if grid[i][j] == 1:
                obstacle_weights.append(weights[i][j])
                obstacle_positions.append((i, j))
    
    if obstacle_weights:
        print(f"  Poids des obstacles ({len(obstacle_weights)}): min={min(obstacle_weights)}, "
              f"max={max(obstacle_weights)}, moyenne={sum(obstacle_weights)/len(obstacle_weights):.1f}")
        print(f"  Somme des poids des obstacles: {sum(obstacle_weights)}")
        
        # Affiche les obstacles avec les poids les plus bas (ceux qui ont été sélectionnés)
        print(f"\n  Obstacles sélectionnés (poids les plus bas):")
        sorted_obstacles = sorted(zip(obstacle_positions, obstacle_weights), key=lambda x: x[1])
        for (i, j), w in sorted_obstacles[:5]:  # Affiche les 5 premiers
            print(f"    Position ({i},{j}): poids = {w}")
        
        # Si il y a plus d'obstacles, mentionne le nombre
        if len(sorted_obstacles) > 5:
            print(f"  ... et {len(sorted_obstacles)-5} autres obstacles")
            # Affiche l'obstacle avec le poids le plus élevé (le plus "coûteux")
            print(f"\n  Obstacle avec le poids le plus élevé (coûteux):")
            (i, j), w = max(zip(obstacle_positions, obstacle_weights), key=lambda x: x[1])
            print(f"    Position ({i},{j}): poids = {w}")
    else:
        print("  Aucun obstacle dans la grille")
    
    print("="*60)

def save_weights_to_file(weights, grid, M, N, P, filename):
    """
    Sauvegarde les poids dans un fichier texte
    """
    with open(filename, 'w') as f:
        f.write(f"# Matrice de poids aléatoires pour grille {M}x{N} avec P={P} obstacles\n")
        f.write(f"# Poids générés aléatoirement entre 0 et 1000\n")
        f.write(f"# Les obstacles sont indiqués par [poids]\n\n")
        
        f.write("Format: Ligne,Colonne,Est_Obstacle,Poids\n")
        f.write("-" * 50 + "\n")
        
        total_weight = 0
        obstacle_weight = 0
        
        for i in range(M):
            for j in range(N):
                is_obstacle = grid[i][j]
                weight = weights[i][j]
                total_weight += weight
                if is_obstacle:
                    obstacle_weight += weight
                f.write(f"{i},{j},{is_obstacle},{weight}\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"STATISTIQUES:\n")
        f.write(f"Somme de tous les poids: {total_weight}\n")
        f.write(f"Somme des poids des obstacles: {obstacle_weight}\n")
        f.write(f"Nombre d'obstacles: {P}\n")
        f.write(f"Poids moyen de tous les cases: {total_weight/(M*N):.2f}\n")
        if P > 0:
            f.write(f"Poids moyen des obstacles: {obstacle_weight/P:.2f}\n")
            f.write(f"Pourcentage du poids total utilisé: {(obstacle_weight/total_weight)*100:.2f}%\n")
    
    print(f"Poids sauvegardés dans '{filename}'")

def interactive_constrained_generation():
    """
    Interface interactive pour la génération de grilles avec contraintes utilisant Gurobi
    et test des trois algorithmes sur la même grille
    
    Note: Selon l'énoncé du problème, M ≤ 50 et N ≤ 50
    """
    print("\n=== GÉNÉRATION DE GRILLES AVEC CONTRAINTES (GUROBI) ===")
    print("Test des trois algorithmes sur la même grille")
    
    if not GUROBI_AVAILABLE:
        print("ATTENTION: Gurobi n'est pas installé.")
        print("La génération utilisera une méthode heuristique moins optimale.")
        print("Pour une solution optimale, installez Gurobi: pip install gurobipy")
    
    try:
        # =============================================
        # Saisie des paramètres avec validation
        # =============================================
        # Validation de M (hauteur - nombre de lignes) selon l'énoncé (≤ 50)
        while True:
            try:
                M = int(input("Hauteur de la grille (M, nombre de lignes, 1-50): "))
                if M <= 0:
                    print("Erreur: M doit être positif")
                    continue
                if M > 50:
                    print("Erreur: Selon l'énoncé, M doit être ≤ 50")
                    continue
                break
            except ValueError:
                print("Erreur: Veuillez entrer un nombre entier valide")
        
        # Validation de N (largeur - nombre de colonnes) selon l'énoncé (≤ 50)
        while True:
            try:
                N = int(input("Largeur de la grille (N, nombre de colonnes, 1-50): "))
                if N <= 0:
                    print("Erreur: N doit être positif")
                    continue
                if N > 50:
                    print("Erreur: Selon l'énoncé, N doit être ≤ 50")
                    continue
                break
            except ValueError:
                print("Erreur: Veuillez entrer un nombre entier valide")
        
        max_obstacles = M * N
        while True:
            try:
                P = int(input(f"Nombre d'obstacles (P, 0 à {max_obstacles}): "))
                if P < 0 or P > max_obstacles:
                    print(f"Erreur: P doit être entre 0 et {max_obstacles}")
                    continue
                break
            except ValueError:
                print("Erreur: Veuillez entrer un nombre entier valide")
        
        # =============================================
        # Vérification préalable (avertissements seulement)
        # =============================================
        # Avertissement si P est très élevé
        if P > M * N - 2:
            free_cells = M * N - P
            print(f"\nATTENTION: Avec P = {P} obstacles dans une grille {M}x{N},")
            print(f"   il ne reste que {free_cells} case{'s' if free_cells > 1 else ''} libre{'s' if free_cells > 1 else ''}.")
            confirm = input("Voulez-vous continuer? (o/n): ").lower()
            if confirm != 'o':
                print("Opération annulée.")
                return
        
        # =============================================
        # Génération de la grille avec Gurobi
        # =============================================
        # Calcul des contraintes selon l'énoncé (division entière)
        max_per_row = (2 * P) // M
        max_per_col = (2 * P) // N
        
        print(f"\nContraintes appliquées (selon l'énoncé):")
        print(f"- Obstacles totaux: {P}")
        print(f"- Max par ligne: {max_per_row} (2P/M = {2*P/M:.2f}, arrondi à l'entier inférieur)")
        print(f"- Max par colonne: {max_per_col} (2P/N = {2*P/N:.2f}, arrondi à l'entier inférieur)")
        print(f"- Aucune séquence '101' (1-0-1) dans aucune ligne ou colonne")
        
        # Avertissement si les contraintes sont très strictes
        if P > 0 and (max_per_row == 0 or max_per_col == 0):
            print("\nATTENTION: Les contraintes sont très strictes!")
            print("   Avec ces paramètres, chaque ligne et chaque colonne peut avoir au plus 0 obstacle,")
            print("   mais vous voulez placer P > 0 obstacles. Ce problème est probablement infaisable.")
            print("   Vous pourriez obtenir une solution None (pas de grille).")
        
        print("\nGénération de la grille avec Gurobi...")
        print("Étape 1: Génération des poids aléatoires (0-1000) pour chaque case...")
        start_time = time.time()
        grid, weights = generate_constrained_grid_gurobi_with_weights(M, N, P)
        end_time = time.time()
        
        print(f"Grille générée en {end_time - start_time:.2f} secondes")
        
        # Si la grille est None, le problème est infaisable
        if grid is None:
            print("\nAucune grille n'a pu être générée avec les contraintes données.")
            print("   Le problème est probablement infaisable avec les paramètres choisis.")
            print("\nSuggestions:")
            print("1. Augmenter M ou N (taille de la grille)")
            print("2. Réduire P (nombre d'obstacles)")
            print("3. Modifier manuellement les contraintes (non conforme à l'énoncé)")
            return
        
        # =============================================
        # Affichage des poids aléatoires
        # =============================================
        if weights is not None:
            print("\n=== MATRICE DES POIDS ALÉATOIRES ===")
            print("Chaque case a reçu un poids aléatoire entre 0 et 1000.")
            print("L'algorithme minimise la somme des poids des cases sélectionnées comme obstacles.")
            
            # Demande à l'utilisateur s'il veut voir les poids
            view_weights = input("\nVoulez-vous afficher la matrice des poids? (o/n): ").lower()
            if view_weights == 'o':
                display_weights(weights, M, N, grid)
            
            # Demande à l'utilisateur s'il veut sauvegarder les poids dans un fichier
            save_weights = input("\nVoulez-vous sauvegarder les poids dans un fichier? (o/n): ").lower()
            if save_weights == 'o':
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                weights_file = os.path.join(RESULTATS_DIR, f"poids_grille_{M}x{N}_P{P}_{timestamp}.txt")
                save_weights_to_file(weights, grid, M, N, P, weights_file)
        else:
            print("\nNote: Méthode heuristique utilisée - pas de poids aléatoires générés.")
        
        # =============================================
        # Analyse de la grille générée
        # =============================================
        # Comptage des cases libres dans la grille générée
        free_cells = sum(1 for i in range(M) for j in range(N) if grid[i][j] == 0)
        print(f"\nGrille générée: {free_cells} case{'s' if free_cells > 1 else ''} libre{'s' if free_cells > 1 else ''} sur {M*N}")
        
        # Avertissements selon le nombre de cases libres
        if free_cells == 0:
            print("ATTENTION: La grille ne contient aucune case libre.")
        elif free_cells == 1:
            print("ATTENTION: La grille ne contient qu'une seule case libre.")
        elif free_cells == 2:
            print("ATTENTION: La grille ne contient que deux cases libres.")
        
        # Affichage de la grille sous forme visuelle
        print("\nGrille générée avec succès:")
        print("   " + " ".join(str(j) for j in range(N)))  # En-tête des colonnes
        for i in range(M):
            print(f"{i}: " + " ".join("X" if cell == 1 else "." for cell in grid[i]))
        
        # =============================================
        # Vérification détaillée des contraintes
        # =============================================
        total_obstacles = sum(sum(row) for row in grid)
        print(f"\nVérification des contraintes:")
        print(f"- Obstacles totaux: {total_obstacles} / {P} (attendu)")
        
        # Vérification des contraintes par ligne
        row_violations = []
        for i in range(M):
            row_count = sum(grid[i])
            if row_count > max_per_row:
                row_violations.append(f"Ligne {i}: {row_count} obstacles (dépasse {max_per_row})")
        
        # Vérification des contraintes par colonne
        col_violations = []
        for j in range(N):
            col_count = sum(grid[i][j] for i in range(M))
            if col_count > max_per_col:
                col_violations.append(f"Colonne {j}: {col_count} obstacles (dépasse {max_per_col})")
        
        # Vérification des contraintes "101"
        violations_101 = []
        # Horizontalement
        for i in range(M):
            for j in range(N-2):
                if grid[i][j] == 1 and grid[i][j+1] == 0 and grid[i][j+2] == 1:
                    violations_101.append(f"Horizontal: ({i},{j})-({i},{j+1})-({i},{j+2})")
        # Verticalement
        for j in range(N):
            for i in range(M-2):
                if grid[i][j] == 1 and grid[i+1][j] == 0 and grid[i+2][j] == 1:
                    violations_101.append(f"Vertical: ({i},{j})-({i+1},{j})-({i+2},{j})")
        
        # Affichage des violations éventuelles
        if row_violations:
            print("- Violations par ligne:")
            for violation in row_violations:
                print(f"  {violation}")
        
        if col_violations:
            print("- Violations par colonne:")
            for violation in col_violations:
                print(f"  {violation}")
        
        if violations_101:
            print("- Violations de contrainte 101:")
            for violation in violations_101[:5]:  # Limiter à 5 violations pour la lisibilité
                print(f"  {violation}")
            if len(violations_101) > 5:
                print(f"  ... et {len(violations_101) - 5} autres violations")
        
        # Avertissement si des violations sont détectées (normalement improbable avec Gurobi)
        if row_violations or col_violations or violations_101:
            print("\nATTENTION: La grille générée viole certaines contraintes!")
            print("   Cela ne devrait pas arriver avec une solution Gurobi optimale.")
        
        # =============================================
        # Calcul des positions sûres pour le robot
        # IMPORTANT: Le robot se place sur un CROISEMENT, pas sur une case
        # Un croisement (x,y) est sûr si les 4 cases autour sont libres
        # (ou moins si sur un bord)
        # =============================================
        safe_positions = []
        for x in range(M + 1):  # x va de 0 à M (croisements)
            for y in range(N + 1):  # y va de 0 à N (croisements)
                if is_position_safe(x, y, M, N, grid):
                    safe_positions.append((x, y))
        
        # =============================================
        # Vérification s'il existe des positions sûres
        # =============================================
        if len(safe_positions) == 0:
            print(f"\nATTENTION: Aucun croisement n'est sûr pour placer le robot!")
            
            # Cas particulier: P = M*N (toute la grille est remplie d'obstacles)
            if P == M * N:
                print("   Vous avez choisi P = M × N = {} obstacles.".format(P))
                print("   Cela signifie que toute la grille est remplie d'obstacles.")
                print("   Aucune position n'est disponible pour placer le robot.")
            else:
                print("   Même s'il reste des cases libres, tous les croisements")
                print("   sont adjacents à au moins un obstacle.")
            
            print("\nOptions:")
            print("1. Réduire le nombre d'obstacles (P)")
            print("2. Augmenter la taille de la grille (M ou N)")
            print("3. Annuler cette génération")
            
            choice = input("\nQue voulez-vous faire? (1/2/3): ").strip()
            if choice == "1":
                # Retour à la saisie de P
                while True:
                    try:
                        new_P = int(input(f"Nouveau nombre d'obstacles (P, 0 à {max_obstacles-1}): "))
                        if new_P < 0 or new_P >= max_obstacles:
                            print(f"Erreur: P doit être entre 0 et {max_obstacles-1} pour avoir au moins une chance de placer le robot")
                            continue
                        # Mettre à jour P et régénérer la grille
                        P = new_P
                        
                        # Régénérer la grille avec le nouveau P
                        print("\nRégénération de la grille avec P = {}...".format(P))
                        start_time = time.time()
                        grid, weights = generate_constrained_grid_gurobi_with_weights(M, N, P)
                        end_time = time.time()
                        
                        if grid is None:
                            print("Impossible de générer une grille avec ces paramètres.")
                            return
                        
                        print(f"Grille régénérée en {end_time - start_time:.2f} secondes")
                        
                        # Recalculer les positions sûres
                        safe_positions = []
                        for x in range(M + 1):
                            for y in range(N + 1):
                                if is_position_safe(x, y, M, N, grid):
                                    safe_positions.append((x, y))
                        
                        if len(safe_positions) > 0:
                            print(f"{len(safe_positions)} croisement(s) sûr(s) trouvé(s).")
                            break
                        else:
                            print("Aucun croisement sûr même avec P = {}. Essayez une valeur plus faible.".format(P))
                            continue
                            
                    except ValueError:
                        print("Erreur: Veuillez entrer un nombre entier valide")
            elif choice == "2":
                # Pour simplifier, on annule et demande à relancer
                print("Opération annulée. Veuillez relancer la génération avec des dimensions plus grandes.")
                return
            else:
                print("Opération annulée.")
                return
        
        # Si on a des positions sûres, continuer
        print(f"\nCroisements sûrs disponibles pour placer le robot ({len(safe_positions)}):")
        for pos in safe_positions[:10]:  # Afficher seulement les 10 premiers pour ne pas submerger l'utilisateur
            print(f"  ({pos[0]}, {pos[1]})")
        if len(safe_positions) > 10:
            print(f"  ... et {len(safe_positions) - 10} autres croisements sûrs")
        
        # =============================================
        # Saisie du point de départ (croisement)
        # =============================================
        print("\n=== POINT DE DÉPART ===")
        print("Note: Le robot se place sur un CROISEMENT, pas sur une case.")
        print(f"Coordonnées: x ∈ [0, {M}] (ligne du croisement), y ∈ [0, {N}] (colonne du croisement)")
        
        while True:
            try:
                start_x = int(input(f"Coordonnée x du croisement de départ (0 à {M}): "))
                start_y = int(input(f"Coordonnée y du croisement de départ (0 à {N}): "))
                
                if is_position_safe(start_x, start_y, M, N, grid):
                    break
                else:
                    print("Position de départ non valide (croisement non sûr)!")
                    print("Voici quelques croisements sûrs:", safe_positions[:min(5, len(safe_positions))])
            except ValueError:
                print("Veuillez entrer des nombres valides!")
        
        # =============================================
        # Saisie du point d'arrivée (croisement)
        # =============================================
        print("\n=== POINT D'ARRIVÉE ===")
        print("Note: Le point d'arrivée peut être le même que le point de départ.")
        
        while True:
            try:
                end_x = int(input(f"Coordonnée x du croisement d'arrivée (0 à {M}): "))
                end_y = int(input(f"Coordonnée y du croisement d'arrivée (0 à {N}): "))
                
                if is_position_safe(end_x, end_y, M, N, grid):
                    # Avertissement si départ et arrivée sont identiques
                    if (start_x, start_y) == (end_x, end_y):
                        print("Note: Le point de départ et d'arrivée sont identiques.")
                        print("Le robot ne devra pas se déplacer (temps = 0 secondes).")
                    break
                else:
                    print("Position d'arrivée non valide (croisement non sûr)!")
                    print("Voici quelques croisements sûrs:", safe_positions[:min(5, len(safe_positions))])
            except ValueError:
                print("Veuillez entrer des nombres valides!")
        
        # =============================================
        # Saisie de la direction initiale
        # =============================================
        print("\n=== DIRECTION INITIALE ===")
        print("Direction initiale du robot:")
        for i, dir_name in enumerate(["nord", "est", "sud", "ouest"]):
            print(f"{i+1}. {dir_name}")
        
        while True:
            try:
                dir_choice = int(input("Choix (1-4): "))
                if 1 <= dir_choice <= 4:
                    start_dir = ["nord", "est", "sud", "ouest"][dir_choice-1]
                    break
                else:
                    print("Choix invalide! Veuillez entrer un nombre entre 1 et 4")
            except ValueError:
                print("Veuillez entrer un nombre valide!")
        
        # =============================================
        # Test et comparaison des trois algorithmes
        # =============================================
        algorithms = {
            'BFS': solve_bfs,
            'Dijkstra': dijkstra,
            'Bellman': bellman_robot_path
        }
        
        print("\n" + "="*60)
        print("COMPARAISON DES TROIS ALGORITHMES")
        print("="*60)
        
        results = {}
        
        for algo_name, algo_func in algorithms.items():
            print(f"\n--- Exécution de {algo_name} ---")
            start_time = time.time()
            time_result, commands = algo_func(M, N, grid, start_x, start_y, end_x, end_y, start_dir)
            end_time = time.time()
            exec_time = end_time - start_time
            
            results[algo_name] = {
                'time_result': time_result,
                'commands': commands,
                'exec_time': exec_time
            }
            
            if time_result == -1:
                print(f"Résultat: Aucun chemin trouvé")
            else:
                print(f"Résultat: {time_result} secondes")
                print(f"Nombre de commandes: {len(commands)}")
                if len(commands) <= 20:
                    print(f"Commandes: {' '.join(commands)}")
                else:
                    print(f"Commandes (premières 20): {' '.join(commands[:20])}...")
            print(f"Temps de calcul: {exec_time:.6f} secondes")
        
        # =============================================
        # Sauvegarde des résultats dans un fichier
        # =============================================
        resultats_file = os.path.join(RESULTATS_DIR, "resultats_comparaison_algorithmes.txt")
        
        with open(resultats_file, 'w') as f:
            f.write(f"Grille {M}x{N} avec {P} obstacles\n")
            f.write("Grille:\n")
            for i in range(M):
                f.write(" ".join("X" if cell == 1 else "." for cell in grid[i]) + "\n")
            f.write(f"\nDépart: ({start_x}, {start_y}), Direction: {start_dir}\n")
            f.write(f"Arrivée: ({end_x}, {end_y})\n")
            
            # Ajouter les informations sur les poids si disponibles
            if weights is not None:
                f.write("\nINFORMATIONS SUR LES POIDS ALÉATOIRES:\n")
                f.write("Chaque case a reçu un poids aléatoire entre 0 et 1000.\n")
                f.write("L'objectif est de minimiser la somme des poids des obstacles.\n")
                
                obstacle_weights = [weights[i][j] for i in range(M) for j in range(N) if grid[i][j] == 1]
                if obstacle_weights:
                    f.write(f"Somme des poids des obstacles: {sum(obstacle_weights)}\n")
                    f.write(f"Poids moyen des obstacles: {sum(obstacle_weights)/len(obstacle_weights):.2f}\n")
            
            f.write("\nVIOLATIONS DES CONTRAINTES:\n")
            if row_violations:
                f.write("Violations par ligne:\n")
                for violation in row_violations:
                    f.write(f"  {violation}\n")
            if col_violations:
                f.write("Violations par colonne:\n")
                for violation in col_violations:
                    f.write(f"  {violation}\n")
            if violations_101:
                f.write("Violations de contrainte 101:\n")
                for violation in violations_101:
                    f.write(f"  {violation}\n")
            
            f.write("\nCOMPARAISON DES ALGORITHMES:\n")
            f.write(f"{'Algorithme':<12} | {'Temps solution':<14} | {'Temps calcul (s)':<16} | {'Commandes'}\n")
            f.write("-" * 80 + "\n")
            
            for algo_name in algorithms:
                result = results[algo_name]
                if result['time_result'] == -1:
                    time_str = "Aucun chemin"
                    commands_str = "N/A"
                else:
                    time_str = f"{result['time_result']} secondes"
                    commands_str = ' '.join(result['commands'])
                
                f.write(f"{algo_name:<12} | {time_str:<14} | {result['exec_time']:<16.6f} | {commands_str}\n")
            
            # Analyse de cohérence entre les algorithmes
            f.write("\nANALYSE DE COHÉRENCE:\n")
            valid_results = [(algo, res) for algo, res in results.items() if res['time_result'] != -1]
            
            if len(valid_results) == 0:
                f.write("Aucun algorithme n'a trouvé de chemin.\n")
            elif len(valid_results) == 1:
                f.write(f"Seul {valid_results[0][0]} a trouvé un chemin.\n")
            else:
                times = [res['time_result'] for _, res in valid_results]
                if all(t == times[0] for t in times):
                    f.write("Tous les algorithmes donnent le même temps de solution (cohérent).\n")
                else:
                    f.write("Les algorithmes donnent des temps de solution différents:\n")
                    for algo, res in valid_results:
                        f.write(f"  - {algo}: {res['time_result']} secondes\n")
        
        print(f"\nRésultats détaillés sauvegardés dans '{resultats_file}'")
        
        # =============================================
        # Sauvegarde AUTOMATIQUE de l'instance
        # =============================================
        default_filename = "instances_generees_par_gurobi.txt"
        full_path = os.path.join(INSTANCES_DIR, default_filename)
        
        save = input(f"\nVoulez-vous sauvegarder cette instance dans '{default_filename}'? (o/n): ").lower()
        if save == 'o':
            # Vérifier si le fichier existe déjà
            if os.path.exists(full_path):
                overwrite = input(f"  Le fichier '{default_filename}' existe déjà. Voulez-vous l'écraser? (o/n): ").lower()
                if overwrite != 'o':
                    print("Sauvegarde annulée.")
                    return
            
            with open(full_path, 'w') as f:
                write_instance_to_file(f, M, N, grid, start_x, start_y, end_x, end_y, start_dir)
                f.write("0 0\n")
            print(f"Instance sauvegardée dans '{full_path}'")
        else:
            print("Instance non sauvegardée.")
    
    except ValueError:
        print("Erreur: Veuillez entrer des nombres valides!")
    except KeyboardInterrupt:
        print("\nOpération annulée!")

# ==================== FONCTION PRINCIPALE ====================

def solve_file_with_algorithm(filename, algorithm_name):
    """
    Résout un fichier d'instances avec un algorithme spécifique
    """
    algorithms = {
        'BFS': solve_bfs,
        'Dijkstra': dijkstra,
        'Bellman': bellman_robot_path
    }
    
    if algorithm_name not in algorithms:
        print("Algorithme non reconnu!")
        return
    
    algo_func = algorithms[algorithm_name]
    
    if not os.path.exists(filename):
        print(f"Fichier {filename} non trouvé!")
        return
    
    with open(filename, 'r') as f:
        data = f.read().strip().split('\n')
    
    idx = 0
    results = []
    total_time = 0
    
    while idx < len(data):
        line = data[idx]
        if line == "0 0":
            break
        
        M, N = map(int, line.split())
        grid = []
        for i in range(M):
            idx += 1
            grid.append(list(map(int, data[idx].split())))
        
        idx += 1
        parts = data[idx].split()
        sx, sy, ex, ey = map(int, parts[:4])
        start_dir = parts[4]
        
        start_time = time.time()
        time_result, commands = algo_func(M, N, grid, sx, sy, ex, ey, start_dir)
        end_time = time.time()
        
        total_time += (end_time - start_time)
        
        if time_result == -1:
            results.append("-1")
        else:
            results.append(f"{time_result} {' '.join(commands)}")
        
        idx += 1
    
    # Affichage des résultats
    print(f"\n=== RÉSULTATS AVEC {algorithm_name} ===")
    for res in results:
        print(res)
    
    print(f"\nTemps total de calcul: {total_time:.6f} secondes")
    
    # Sauvegarde des résultats
    output_file = os.path.join(RESULTATS_DIR, f"resultats_{algorithm_name.lower()}.txt")
    with open(output_file, 'w') as f:
        for res in results:
            f.write(res + '\n')
    print(f"Résultats sauvegardés dans '{output_file}'")

def main_menu():
    """
    Menu principal interactif
    """
    while True:
        print("\n" + "="*50)
        print("         ROBOT PATHFINDER - MENU PRINCIPAL")
        print("="*50)
        print("1. Tests de performance - Taille de grille (c)")
        print("2. Tests de performance - Nombre d'obstacles (d)")
        print("3. Génération avec contraintes et Gurobi (e)")
        print("4. Résoudre un fichier avec BFS")
        print("5. Résoudre un fichier avec Dijkstra")
        print("6. Résoudre un fichier avec Bellman")
        print("7. Quitter")
        print("-"*50)
        
        if not GUROBI_AVAILABLE:
            print("NOTE: Gurobi n'est pas installé. L'option 3 utilisera une méthode heuristique.")
        
        choice = input("Votre choix (1-7): ")
        
        if choice == '1':
            run_size_performance_tests()
        
        elif choice == '2':
            run_obstacle_performance_tests()
        
        elif choice == '3':
            interactive_constrained_generation()
        
        elif choice == '4':
            filename = input("Nom du fichier d'instances: ")
            solve_file_with_algorithm(filename, 'BFS')
        
        elif choice == '5':
            filename = input("Nom du fichier d'instances: ")
            solve_file_with_algorithm(filename, 'Dijkstra')
        
        elif choice == '6':
            filename = input("Nom du fichier d'instances: ")
            solve_file_with_algorithm(filename, 'Bellman')
        
        elif choice == '7':
            print("Au revoir!")
            break
        
        else:
            print("Choix invalide! Veuillez choisir entre 1 et 7.")
        
        input("\nAppuyez sur Entrée pour continuer...")

# ==================== POINT D'ENTRÉE ====================

if __name__ == "__main__":
    print("Bienvenue dans le système de résolution de chemins pour robots!")
    main_menu()