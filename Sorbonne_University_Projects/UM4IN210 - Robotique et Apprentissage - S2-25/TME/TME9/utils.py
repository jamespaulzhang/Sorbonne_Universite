import networkx as nx
from deap import gp
from matplotlib import pyplot as plt
import math
import numpy as np


def tree_width(G, root, parents):
    # Fonction récursive pour calculer la largeur d'un arbre
    neighbors = list(G.neighbors(root))
    children = [c for c in neighbors if c not in parents]
    width = 0
    for c in children:
        width += tree_width(G, c, parents+[root])
    return max(1, width)


def tree_layout(G, root):
    # Fonction pour générer les positions des noeuds d'un arbre pour l'affichage
    pos = {}
    queue = [(root, 0, 0)]

    while queue:
        node, depth, index = queue.pop(0)
        pos[node] = (index, -depth)

        neighbors = list(G.neighbors(node))
        children = [c for c in neighbors if c not in pos.keys()]
        if children:
            width = tree_width(G, node, list(pos.keys()))
            offset = -(width) * 0.5
            for i, child in enumerate(children):
                if child not in pos.keys():
                    child_width = tree_width(G, child, list(pos.keys()))
                    queue.append(
                        (child, depth + 1, index + offset + child_width/2))
                    offset += child_width

    return pos


def plot_symbolic_tree(ind):
    # Fonction pour afficher un arbre symbolique

    nodes, edges, labels = gp.graph(ind)
    for key, label in labels.items():
        try:
            cst = float(label)
            labels[key] = "%.2f" % cst
        except:
            pass
        if label == "ARG0":
            labels[key] = r"$\theta_1$"
        if label == "ARG1":
            labels[key] = r"$\theta_2$"
        if label == "protectedDiv":
            labels[key] = "div"

    # Construction du graphe
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Positions des noeuds
    pos = tree_layout(G, 0)

    # Affichage
    nx.draw(G, pos, with_labels=False, node_size=500,
            node_color='skyblue')  # Draw nodes
    nx.draw_networkx_labels(
        G, pos, labels=labels, font_size=12, font_color='black')
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

    plt.show()


def display_function(f, train_inputs, train_outputs, test_inputs, test_outputs, ood_inputs, ood_outputs, f_true):

    # Plot the training outputs for different values of theta_2
    plt.figure(figsize=(20, 4))
    for k, theta_2 in enumerate([0, math.pi/4, math.pi/2]):

        plt.subplot(1, 4, k+1)
        for i in range(len(train_inputs)):
            if train_inputs[i, 1] == theta_2:
                plt.scatter(train_inputs[i, 0],
                            train_outputs[i], color="tab:blue")
        for i in range(len(test_inputs)):
            if test_inputs[i, 1] == theta_2:
                plt.scatter(test_inputs[i, 0],
                            test_outputs[i], color="tab:orange")
        for i in range(len(ood_inputs)):
            if ood_inputs[i, 1] == theta_2:
                plt.scatter(ood_inputs[i, 0],
                            ood_outputs[i], color="tab:green")
        plt.plot(np.linspace(0, 2*math.pi, 100), f_true(np.linspace(0, 2*math.pi, 100),
                                                   theta_2), label='true', color="black")
        plt.plot(np.linspace(0, 2*math.pi, 100), f(np.linspace(0, 2*math.pi, 100), theta_2),
                 label='predicted', color="tab:blue")
        plt.xticks([0, math.pi, 2*math.pi], ['0', r'$\pi$', r'$2\pi$'])
        plt.xlabel(r'$\theta_1$')
        plt.ylabel('x')
        plt.ylim(-2.5, 2.5)
        plt.legend()
        plt.title(r'$\theta_2 = $' + str(round(theta_2, 2)))
    plt.show()