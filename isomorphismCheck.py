from basicpermutationgroup import order
from graph import *
from graph_io import *
from permv2 import permutation


def isoMorphismCount(G: "Graph", H: "Graph"):
    """
    Set up
    """
    for v in G.vertices:
        v.initialGraph = True
    for v in H.vertices:
        v.initialGraph = False
    U = G + H
    for v in U.vertices:
        v.label = 0
        v.newLabel = 0
    return recIsoMorphismCount(U)


def recIsoMorphismCount(U: "Graph"):
    """
    Recursive function that counts the isomorphism
    """
    balanced = True
    bijection = True
    partitions = U.partitionRefinements()

    # Check if the bijection and balance of the graph
    for p in partitions:
        count = 0
        for v in p:
            if v.initialGraph :
                count += 1
        if len(p) != 2 or count != 1:
            bijection = False
        if count * 2 != len(p):
            balanced = False
            break

    # Apply the condition from the lecture
    if bijection:
        return 1
    elif not balanced:
        return 0
    else:
        # The approach is to choose the partition with smallest size >=4, still not sure if it really boosts the speed
        chosenIndex = 0
        x = None
        countIsomorphism = 0

        # List used to revert the map to initial state after a iteration
        labelList = [0] * len(U.vertices)
        for i in range(len(U.vertices)):
            labelList[i] = U.vertices[i].label
        # Choose x
        for v in partitions[chosenIndex]:
            if v.initialGraph :
                x = v
                break
        # Looping through y from graph H
        for y in partitions[chosenIndex]:
            if y.initialGraph:
                continue
            for i in range(len(partitions)):
                for v in partitions[i]:
                    v.label = v.newLabel = i
            # Set new color
            x.label = x.newLabel = len(partitions)
            y.label = y.newLabel = len(partitions)
            countIsomorphism += recIsoMorphismCount(U)

            # Revert to initial values
            for i in range(len(U.vertices)):
                U.vertices[i].label = labelList[i]
        return countIsomorphism


def isoCount(G, H, counting):
    """
    Set up
    """
    if G.isTree():
        print("This is a tree")
        return treeIso(G, H)
    for v in G.vertices:
        v.initialGraph = True
    for v in H.vertices:
        v.initialGraph = False
    U = G + H
    for v in U.vertices:
        v.label = 0
        v.newLabel = 0
        v.group = v
        v.nr = -1
        v.groupSize = -1
        v.twinType = 0
    copyU = U
    product = 1
    product = H.formTwinGroup()
    G.formTwinGroup()
    # if product > 1:
    #     print(product)
    copyU = Graph(False)
    for v in U.vertices:
        if v.group == v:
            v._graph = copyU
            copyU.add_vertex(v)
            v._incidence = {}

    for e in U.edges:
        tail = e.tail
        head = e.head

        if head.group == head and tail.group == tail:
            head._add_incidence(e)
            tail._add_incidence(e)
            copyU.add_edge(e)

    if not counting:
        return recIsoMorphismCheck(copyU)

    generator = []
    ans = generatingSet(copyU, False, generator)

    # print(len(generator))
    # print(len(Reduce(generator)))
    if ans:
        return product * order(generator)
    else:
        return 0


def recIsoMorphismCheck(U: "Graph"):
    """
    Recursive function that counts the isomorphism
    """
    balanced = True
    bijection = True
    partitions = U.fastPr()
    # Check if the bijection and balance of the graph
    for p in partitions:
        count = 0

        gGroupSizeCount = {}
        gTwinCount = {}

        hGroupSizeCount = {}
        hTwinCount = {}
        for v in p:
            if v.initialGraph:
                count += 1
                gTwinCount[v.twinType] = gTwinCount.get(v.twinType, 0) + 1
                gGroupSizeCount[v.groupSize] = gGroupSizeCount.get(v.groupSize, 0) + 1
            else:
                hTwinCount[v.twinType] = hTwinCount.get(v.twinType, 0) + 1
                hGroupSizeCount[v.groupSize] = hGroupSizeCount.get(v.groupSize, 0) + 1
        for groupSize in gGroupSizeCount:
            gGroupCount = gGroupSizeCount[groupSize]
            if gGroupCount != hGroupSizeCount.get(groupSize, -5):
                balanced = False
                bijection = False
                break
        for twinCount in gTwinCount:
            if not balanced:
                break
            gTCount = gTwinCount[twinCount]
            if gTCount != hTwinCount.get(twinCount, -5):
                balanced = False
                bijection = False
                break
        bijection = bijection and len(p) == 2
        if not balanced:
            break

    # Apply the condition from the lecture
    if bijection:
        return True
    elif not balanced:
        return False
    else:
        # The approach is to choose the partition with smallest size >=4, still not sure if it really boosts the speed
        chosenIndex = -1
        minLen = 0
        for i in range(len(partitions)):
            lenP = len(partitions[i])
            if 4 <= lenP and lenP > minLen:
                chosenIndex = i
                minLen = lenP
        x = None

        ans = False
        # List used to revert the map to initial state after a iteration
        labelList = [0] * len(U.vertices)
        for i in range(len(U.vertices)):
            labelList[i] = U.vertices[i].label
        # Choose x
        for v in partitions[chosenIndex]:
            if v.initialGraph :
                x = v
                break

        # Looping through y from graph H
        for y in partitions[chosenIndex]:
            if y.initialGraph :
                continue

            if y.groupSize != x.groupSize or y.twinType != x.twinType:
                continue

            for i in range(len(partitions)):
                for v in partitions[i]:
                    v.label = v.newLabel = i
            # Set new color
            x.label = x.newLabel = len(partitions)
            y.label = y.newLabel = len(partitions)
            ans = recIsoMorphismCheck(U)
            if ans:
                return True
            # Revert to initial values
            for i in range(len(U.vertices)):
                U.vertices[i].label = labelList[i]
        return False


def generatingSet(U: "Graph", pruned: bool, generator):
    """
    Recursive function that counts the isomorphism
    """
    balanced = True
    bijection = True
    partitions = U.fastPr()

    # Check if the bijection and balance of the graph
    for p in partitions:
        count = 0
        gGroupSizeCount = {}
        gTwinCount = {}

        hGroupSizeCount = {}
        hTwinCount = {}
        for v in p:

            if v.initialGraph:
                count += 1
                gTwinCount[v.twinType] = gTwinCount.get(v.twinType, 0) + 1
                gGroupSizeCount[v.groupSize] = gGroupSizeCount.get(v.groupSize, 0) + 1
            else:
                hTwinCount[v.twinType] = hTwinCount.get(v.twinType, 0) + 1
                hGroupSizeCount[v.groupSize] = hGroupSizeCount.get(v.groupSize, 0) + 1
        for groupSize in gGroupSizeCount:

            gGroupCount = gGroupSizeCount[groupSize]
            if gGroupCount != hGroupSizeCount.get(groupSize, -5):
                balanced = False
                bijection = False
                break

        for twinCount in gTwinCount:
            if not balanced:
                break
            gTCount = gTwinCount[twinCount]
            if gTCount != hTwinCount.get(twinCount, -5):
                balanced = False
                bijection = False
                break
        bijection = bijection and len(p) == 2
        if not balanced:
            break

    # Apply the condition from the lecture
    if bijection:
        if not pruned:
            for v in U.vertices:
                v.nr = v.label
            return True
        n = len(partitions)
        mapping = [0] * n
        x = y = 0
        for p in partitions:
            for v in p:
                if v.initialGraph :
                    x = v.nr
                else:
                    y = v.nr
            mapping[x] = y
        perm = permutation(n, mapping=mapping)
        generator.append(perm)
        # if not isInGenerator(perm, generator):
        #     generator.append(perm)
        return True

    elif balanced:
        # The approach is to choose the partition with smallest size >=4, still not sure if it really boosts the speed
        chosenIndex = -1
        minLen = 0
        for i in range(len(partitions)):
            lenP = len(partitions[i])
            if 4 <= lenP and lenP > minLen:
                chosenIndex = i
                minLen = lenP
        x = None

        # List used to revert the map to initial state after a iteration
        labelList = [0] * len(U.vertices)
        for i in range(len(U.vertices)):
            labelList[i] = U.vertices[i].label
        # Choose x
        for v in partitions[chosenIndex]:
            if v.initialGraph:
                x = v
                break

        # Looping through y from graph H
        found = False
        for y in partitions[chosenIndex]:
            if y.initialGraph :
                continue

            if y.groupSize != x.groupSize or y.twinType != x.twinType:
                continue

            # Set new color
            x.label = x.newLabel = len(partitions)
            y.label = y.newLabel = len(partitions)
            if x.nr == -1 or y.nr == x.nr:
                found = generatingSet(U, pruned, generator) or found
            else:
                found = generatingSet(U, True, generator) or found
            # Revert to initial values
            for i in range(len(U.vertices)):
                U.vertices[i].label = labelList[i]
            if pruned and found:
                break
        return found


def productOfString(encode):
    if len(encode) < 5:
        return 1
    subTrees = {}
    openBrackets = 1
    start = 1
    i = 2
    while i < len(encode) - 1:
        if encode[i] == ')':
            openBrackets -= 1
        else:
            openBrackets += 1
        i += 1
        if openBrackets == 0:
            subTree = encode[start:i]
            subTrees[subTree] = subTrees.get(subTree, 0) + 1
            start = i
    product = 1
    for k in subTrees.items():
        product *= math.factorial(k[1])
        product *= (productOfString(k[0]) ** k[1])
    return product


def treeIso(G, H):
    gCenter = G.treeCenter()[0]
    hCenters = H.treeCenter()
    count = 0
    gEncode = G.encode(gCenter)
    for hCenter in hCenters:
        if H.encode(hCenter) == gEncode:
            count += 1
    if count > 0:
        return count * productOfString(gEncode)
    return 0
