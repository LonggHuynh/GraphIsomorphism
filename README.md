The main file is Main-Long.py

To solve the GI problems, uncomment lines 3-38, and comment line 22(# autCount = isoCount(G, H, True)). If you want to solve GIAut, you dont need to comment line 22.
For the Aut problems, uncomment lines 40-60.

There is a function called isoMorphismCount() which does not include twins/trees/generating set/fast minimization

You can change the path and/or file name to run it on the lines:
with open('<path>') as f:
    L = load_graph(f, read_list=True)

Note that for the selection of file, you need to write the path 2 times.

The following guide will show how to turn on/off some functionality.
Tree:
Go to isomorphismCheck.py, comment line 90-92(if G.isTree():....).

Fast partition refinement, isomorphismCheck.py change all function fastPr() to partitionRefinements().

The generating set and twins implementations are quite integrated, the way to change it is complicated, so it wouldnt be mentioned here


