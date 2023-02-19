import time

from isomorphismCheck import *

dir = sys.argv[1]


try:
    with open(dir) as f:
        L = load_graph(f, read_list=True)
    with open(dir) as f:
        L1 = load_graph(f, read_list=True)
    print('Isomorphic classes')
    visited = [False] * len(L[0])
    start = time.time()
    eClasses = []
    for i in range(len(L[0])):
        if visited[i]:
            continue
        eClass = [i]
        visited[i] = True
        G = L[0][i]
        for j in range(i + 1, len(L[0])):
            if visited[j]:
                continue
            G1 = L[0][j]
            count = isoCount(G, G1, False)
            if count:
                visited[j] = True
                eClass.append(j)
        eClasses.append(eClass)
    end = time.time()

    for i in range(len(eClasses)):
        print(eClasses[i])

    print(end - start)

except:
    print (f"Cannot open {dir}, Usage main.py [file_path]")
