import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt
# import pylab

FOLDER = 'grafos'
EDGE_WEIGHT_TYPE = ''
EDGE_WEIGHT_FORMAT = ''
DIMENSION = 0
GRAPH_MATRIX = None
PROBLEMS = open('problems.txt', 'w')

CLARKE_SOLUTION = None
ECONOMIES_TUPLES = None
SOLUTIONS = []


def initGlobalVariables():
    global EDGE_WEIGHT_FORMAT, EDGE_WEIGHT_TYPE, DIMENSION, GRAPH_MATRIX, CLARKE_SOLUTION, ECONOMIES_TUPLES, SOLUTIONS
    EDGE_WEIGHT_TYPE = ''
    EDGE_WEIGHT_FORMAT = ''
    DIMENSION = 0
    GRAPH_MATRIX = None
    ECONOMIES_TUPLES = None
    SOLUTIONS = []


def parseFile(path):
    global EDGE_WEIGHT_TYPE, EDGE_WEIGHT_FORMAT, GRAPH_MATRIX, DIMENSION
    tmp_array = ''
    with open(path) as f:
        for idx, line in enumerate(f.readlines()):
            if "EOF" in line:
                pass
            elif idx == 0:
                print('\n====== ', line.replace('\n', '').split(
                    ':')[1].strip(), ' ======')
            elif idx == 1:
                print('Type: ', line.replace('\n', '').split(':')[1].strip())
            elif idx == 3:
                DIMENSION = int(line.replace('\n', '').split(':')[1].strip())
                print('Dimension: ', DIMENSION)
            elif idx == 4:
                EDGE_WEIGHT_TYPE = line.replace('\n', '').split(':')[1].strip()
            elif idx == 5:
                EDGE_WEIGHT_FORMAT = line.replace(
                    '\n', '').split(':')[1].strip()
            elif idx > 6:
                tmp_array = tmp_array + line
    if(EDGE_WEIGHT_TYPE == "EXPLICIT"):
        if(EDGE_WEIGHT_FORMAT == "FULL_MATRIX"):
            GRAPH_MATRIX = np.fromstring(
                tmp_array, dtype=int, sep=' ').reshape((DIMENSION, DIMENSION))


def buildInitialSolution():
    global CLARKE_SOLUTION, GRAPH_MATRIX
    CLARKE_SOLUTION = np.full(GRAPH_MATRIX.shape, np.inf)
    for i in range(len(CLARKE_SOLUTION)):
        if i != 0:
            CLARKE_SOLUTION[0][i] = GRAPH_MATRIX[0][i]
            CLARKE_SOLUTION[i][0] = GRAPH_MATRIX[i][0]


def calculateEconomies():
    global GRAPH_MATRIX, ECONOMIES_TUPLES, DIMENSION
    ECONOMIES_TUPLES = []
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if i == j or i == 0 or j == 0:
                continue

            s = GRAPH_MATRIX[0][i] + \
                GRAPH_MATRIX[0][j] - GRAPH_MATRIX[i][j]
            ECONOMIES_TUPLES.append(((i, j), s))
    ECONOMIES_TUPLES = sorted(
        ECONOMIES_TUPLES, key=lambda x: x[1], reverse=True)


def calculatePathSize(path):
    global GRAPH_MATRIX
    pathSize = 0
    for edge in path:
        pathSize += GRAPH_MATRIX[edge[0]][edge[1]]
    return pathSize


def getPath(solucao, origem, caminho, soma):
    for destino in range(len(solucao[origem])):
        if solucao[origem][destino] != np.inf:
            caminho.insert(len(caminho), (origem, destino))
            soma = soma + solucao[origem][destino]
            solucao[origem][destino] = np.inf
            return getPath(solucao, destino, caminho, soma)
    return caminho, soma


def verifyCycle(new_edge):
    path, cost = getPath(CLARKE_SOLUTION.copy(), 0, [], 0)
    verifier = [False, False]
    for edge in path:
        if edge[0] == 0:
            verifier = [False, False]
        if edge[1] == new_edge[0]:
            verifier[0] = True
        if edge[1] == new_edge[1]:
            verifier[1] = True
        if verifier == [True, True]:
            return True
    return False


def insertEconomies():
    global ECONOMIES_TUPLES, GRAPH_MATRIX, CLARKE_SOLUTION
    a = 0
    for economy in ECONOMIES_TUPLES:
        (i, j), s = economy
        if(CLARKE_SOLUTION[i][0] != np.inf and CLARKE_SOLUTION[0][j] != np.inf) and (not verifyCycle((i, j))):
            a = a + 1
            CLARKE_SOLUTION[i][0] = np.inf
            CLARKE_SOLUTION[0][j] = np.inf
            CLARKE_SOLUTION[i][j] = GRAPH_MATRIX[i][j]


def insertSolution():
    global CLARKE_SOLUTION, SOLUTIONS
    SOLUTIONS.append(getPath(CLARKE_SOLUTION.copy(), 0, [], 0))

def clarkeWright():
    buildInitialSolution()
    calculateEconomies()
    insertEconomies()
    insertSolution()


def _2opt():
    global SOLUTIONS, GRAPH_MATRIX
    reference_solution = SOLUTIONS[0][0]
    n = 0
    while n < len(reference_solution):
        for i in range(n+2, len(reference_solution)-1 if n == 0 else (len(reference_solution))):
            edge_one = reference_solution[n]
            edge_two = reference_solution[i]
            new_solution = reference_solution.copy()
            for j in range(n+1, i):
                new_solution[j] = (new_solution[j][1], new_solution[j][0])
            new_solution[n] = (reference_solution[n][0],
                               reference_solution[i][0])
            new_solution[i] = (reference_solution[n][1],
                               reference_solution[i][1])
            SOLUTIONS.append((new_solution, calculatePathSize(new_solution)))
        n += 1


def plotGraph(graph, file, label, matrix):
    global DIMENSION, GRAPH_MATRIX
    edges = []
    if(matrix):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if(graph[i][j] != np.inf and graph[i][j] != 9999):
                    edges.append((i,j))
    else :
        edges = graph

    G = nx.DiGraph()
    for edge in edges:
        G.add_edges_from([edge], weight=GRAPH_MATRIX[edge[0]][edge[1]])
    edge_labels = dict([((u, v,), d['weight'])
                        for u, v, d in G.edges(data=True)])
    red_edges = []
    edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]
    pos=nx.circular_layout(G)
    nx.draw_networkx_labels(G, pos)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw(G, pos, node_size=300, edge_color=edge_colors, edge_cmap=plt.cm.Reds)
    # plt.savefig('graph_images/%s-%s.png' % (file, label))
    plt.show()

def main():
    global FOLDER, PROBLEMS
    PROBLEMS.truncate(0)
    for r, d, f in os.walk(FOLDER):
        if(r != FOLDER and 'atsp' in r):
            for file in f:
                if r.split('/')[1] in file:
                    try:
                        initGlobalVariables()
                        parseFile(r+'/'+file)
                        # parseFile('grafos/atsp/br17.atsp')
                        # plotGraph(GRAPH_MATRIX.copy(), file, 'Complete', True)
                        clarkeWright()
                        print("CLARKE_WRIGHT:",SOLUTIONS[0][1])
                        plotGraph(CLARKE_SOLUTION.copy(), file, 'ClarkeWright', True)
                        _2opt()
                        _2opt_answer = sorted(SOLUTIONS, key=lambda x: x[1])[0]
                        print("2-OPT:", _2opt_answer[1])
                        plotGraph(_2opt_answer[0].copy(), file, '2Opt', False)
                    except Exception as e:
                        print(e)
                        PROBLEMS.writelines(file + '\n')
                    # break
    PROBLEMS.close()


if __name__ == "__main__":
    main()
