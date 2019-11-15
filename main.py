import numpy as np
import os
import scipy.sparse as ssp

FOLDER = 'grafos'
EDGE_WEIGHT_TYPE = ''
EDGE_WEIGHT_FORMAT = ''
DIMENSION = 0
GRAPH_MATRIX = None
SHORTEST_PATHS = None
ECONOMIES_DICTS = None
VISITED = []

PROBLEMS = open('problems.txt', 'w')


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


def calculateMinPathsOneToAll():
    global GRAPH_MATRIX, SHORTEST_PATHS
    SHORTEST_PATHS = ssp.csgraph.bellman_ford(GRAPH_MATRIX, directed=True, return_predecessors=False)
    print(SHORTEST_PATHS)


def calculateEconomies():
    global SHORTEST_PATHS, ECONOMIES_DICTS, DIMENSION
    ECONOMIES_DICTS = {}
    for i in range(DIMENSION):
        ECONOMIES_DICTS[i] = {}
        for j in range(DIMENSION):
            if i != j:
                s = SHORTEST_PATHS[0][i] + SHORTEST_PATHS[0][j] - SHORTEST_PATHS[i][j]
                ECONOMIES_DICTS[i][j] = s
    for key in ECONOMIES_DICTS.keys():
        ECONOMIES_DICTS[key] = dict(sorted(
            ECONOMIES_DICTS[key].items(), key=lambda x : x[1], reverse=True))
    print("########################################")
    print(ECONOMIES_DICTS)
    print("########################################")


def removeOriginsDestinies(origin, destiny):
    global ECONOMIES_DICTS
    if origin in ECONOMIES_DICTS.keys():
        ECONOMIES_DICTS.pop(origin)
    for key in ECONOMIES_DICTS.keys():
        if destiny in ECONOMIES_DICTS[key].keys():
            ECONOMIES_DICTS[key].pop(destiny)


def atsp():
    global ECONOMIES_DICTS, VISITED, DIMENSION
    VISITED = []
    while len(VISITED) != DIMENSION:
        pass


def main():
    global FOLDER, PROBLEMS
    PROBLEMS.truncate(0)
    for r, d, f in os.walk(FOLDER):
        if(r != FOLDER and 'atsp' in r):
            for file in f:
                if r.split('/')[1] in file:
                    try:
                        # parseFile(r+'/'+file)
                        parseFile('grafos/atsp/br17.atsp')
                        calculateMinPathsOneToAll()
                        calculateEconomies()
                        removeOriginsDestinies(0,1)
                        print(ECONOMIES_DICTS)
                    except Exception as e:
                        print(e)
                        PROBLEMS.writelines(file + '\n')
                    break


if __name__ == "__main__":
    main()

