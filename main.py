import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt
import json
import time

FILES = [
    {'file_name':'br17', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ft53', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ft70', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv33', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv35', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv38', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv44', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv47', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv55', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv64', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv70', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ftv170', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'kro124p', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'p43', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'rbg323', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'rbg358', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'rbg403', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'rbg443', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
    {'file_name':'ry48p', 'clarke_solutions': [], '2opt_solutions': [], 'best_clarke_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}, 'best_2opt_solution': {'origin': None, 'solution': {'path': [], 'size': 99999}}},
]

FOLDER = 'grafos'
EDGE_WEIGHT_TYPE = ''
EDGE_WEIGHT_FORMAT = ''
DIMENSION = 0
GRAPH_MATRIX = None
PROBLEMS = open('problems.txt', 'w')

CLARKE_SOLUTION = None
ECONOMIES_TUPLES = None
SOLUTIONS = []
ORIGIN = None


def initGlobalVariables():
    global  CLARKE_SOLUTION, ECONOMIES_TUPLES, SOLUTIONS, ORIGIN
    ECONOMIES_TUPLES = None
    SOLUTIONS = []
    ORIGIN = None
    CLARKE_SOLUTION = None
    ORIGIN = None


def parseFile(path):
    global EDGE_WEIGHT_TYPE, EDGE_WEIGHT_FORMAT, GRAPH_MATRIX, DIMENSION
    GRAPH_MATRIX = None
    DIMENSION = 0
    EDGE_WEIGHT_TYPE = ''
    EDGE_WEIGHT_FORMAT = ''
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
    CLARKE_SOLUTION = [9999] * (GRAPH_MATRIX.shape[0] * GRAPH_MATRIX.shape[1])
    CLARKE_SOLUTION = np.array(CLARKE_SOLUTION).reshape(GRAPH_MATRIX.shape)
    for i in range(len(CLARKE_SOLUTION)):
        if i != 0:
            CLARKE_SOLUTION[ORIGIN][i] = GRAPH_MATRIX[ORIGIN][i]
            CLARKE_SOLUTION[i][ORIGIN] = GRAPH_MATRIX[i][ORIGIN]


def calculateEconomies():
    global GRAPH_MATRIX, ECONOMIES_TUPLES, DIMENSION
    ECONOMIES_TUPLES = []
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if i != j and i != ORIGIN and j != ORIGIN:
                s = GRAPH_MATRIX[ORIGIN][i] + \
                    GRAPH_MATRIX[ORIGIN][j] - GRAPH_MATRIX[i][j]
                ECONOMIES_TUPLES.append(((i, j), s))
    ECONOMIES_TUPLES = sorted(
        ECONOMIES_TUPLES, key=lambda x: x[1], reverse=True)


def calculatePathSize(path):
    global GRAPH_MATRIX
    pathSize = 0
    for edge in path:
        pathSize += GRAPH_MATRIX[edge[0]][edge[1]]
    return pathSize


def getPath(solution, origin, path, cost):
    for destiny in range(len(solution[origin])):
        if solution[origin][destiny] < 9999:
            path.insert(len(path), (origin, destiny))
            cost += solution[origin][destiny]
            solution[origin][destiny] = 9999
            return getPath(solution, destiny, path, cost)
    return path, cost


def verifyCycle(new_edge):
    path, cost = getPath(CLARKE_SOLUTION.copy(), ORIGIN, [], 0)
    verifier = [False, False]
    for edge in path:
        if edge[0] == ORIGIN:
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
    for economy in ECONOMIES_TUPLES:
        (i, j), s = economy
        if(CLARKE_SOLUTION[i][ORIGIN] < 9999 and CLARKE_SOLUTION[ORIGIN][j] < 9999) and (not verifyCycle((i, j))):
            CLARKE_SOLUTION[i][ORIGIN] = 9999
            CLARKE_SOLUTION[ORIGIN][j] = 9999
            CLARKE_SOLUTION[i][j] = GRAPH_MATRIX[i][j]


def insertSolution():
    global CLARKE_SOLUTION, SOLUTIONS
    SOLUTIONS.append(getPath(CLARKE_SOLUTION.copy(), ORIGIN, [], 0))

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
    if matrix:
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if graph[i][j] < 9999 and graph[i][j] < 9999 :
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
    nx.draw(G, pos, node_size=300, node_color='silver', edge_color=edge_colors, edge_cmap=plt.cm.Reds)
    # plt.savefig('graph_images/%s-%s.png' % (file, label))
    plt.show()

def executeToFolder():
    global FOLDER, PROBLEMS, ORIGIN
    for r, d, f in os.walk(FOLDER):
        if(r != FOLDER and 'atsp' in r):
            for file in f:
                if r.split('/')[1] in file:
                    try:
                        initGlobalVariables()
                        ORIGIN = 0
                        parseFile(r+'/'+file)
                        # parseFile('grafos/atsp/br17.atsp')
                        # plotGraph(GRAPH_MATRIX.copy(), file, 'Complete', True)
                        clarkeWright()
                        print("CLARKE_WRIGHT:", SOLUTIONS[0][1])
                        # plotGraph(CLARKE_SOLUTION.copy(), file, 'ClarkeWright', True)
                        _2opt()
                        _2opt_answer = sorted(SOLUTIONS, key=lambda x: x[1])[0]
                        print("2-OPT:", _2opt_answer[1])
                        # plotGraph(_2opt_answer[0].copy(), file, '2Opt', False)
                    except Exception as e:
                        print(file + ':' + e )
                        PROBLEMS.writelines(file + ':' + e + '\n')
                    # break

def executeToArray():
    global FILES, PROBLEMS, ORIGIN, SOLUTIONS
    for i in range(len(FILES)):
        try:
            parseFile('grafos/atsp/%s.atsp' % (FILES[i]['file_name']))
            for j in range(DIMENSION):
                initGlobalVariables()
                SOLUTIONS = []
                ORIGIN = j
                # print("Testing origin %s" % j)
                start = time.time()
                clarkeWright()
                end = time.time()
                cw_solution = {'origin': ORIGIN, 'elapsed_time': end-start, 'solution': {'path': SOLUTIONS[0][0], 'size': int(SOLUTIONS[0][1])}}
                FILES[i]['clarke_solutions'].append(cw_solution.copy())
                if(cw_solution['solution']['size'] < FILES[i]['best_clarke_solution']['solution']['size']):
                    FILES[i]['best_clarke_solution'] = cw_solution.copy()
                start = time.time()
                _2opt()
                end = time.time()
                _2opt_answer = sorted(SOLUTIONS, key=lambda x: x[1])[0]
                _2opt_solution = {'origin': ORIGIN, 'elapsed_time': end-start, 'solution': {'path': _2opt_answer[0], 'size': int(_2opt_answer[1])}}
                FILES[i]['2opt_solutions'].append(_2opt_solution.copy())
                if(_2opt_solution['solution']['size'] < FILES[i]['best_2opt_solution']['solution']['size']):
                    FILES[i]['best_2opt_solution'] = _2opt_solution.copy()
            print("Best Clarke Solution %d using origin %d" % ( FILES[i]['best_clarke_solution']['solution']['size'], FILES[i]['best_clarke_solution']['origin'],))
            print("Best 2-OPT Solution %d using origin %d" % ( FILES[i]['best_2opt_solution']['solution']['size'], FILES[i]['best_2opt_solution']['origin'],))
        except Exception as e:
            print(FILES[i] + ':' + e )
            PROBLEMS.writelines(FILES[i] + ':' + e + '\n')
        with open('results-' + FILES[i]['file_name'] + '.json', 'w') as results_file:
            json.dump(FILES[i], results_file, indent=4)




def main():
    global PROBLEMS
    PROBLEMS.truncate(0)
    # executeToFolder()
    executeToArray()
    PROBLEMS.close()


if __name__ == "__main__":
    main()

