import numpy as np
import os
import pandas as pd
import zipfile

from permutation_group_modified.schreiersims import *




with zipfile.ZipFile('../../../res/data/santa-2023.zip', 'r') as z:
    with z.open('puzzle_info.csv') as f:
        puzzle_info = pd.read_csv(f, index_col='puzzle_type')

    with z.open('puzzles.csv') as f:
        puzzles = pd.read_csv(f, index_col='id')

    with z.open('sample_submission.csv') as f:
        submission = pd.read_csv(f)

N = 3
center_cubelet_faces = list(range(((N-1)//2)*(N+1), 6*N**2, N**2))
# allowed moves
move_dict = eval(puzzle_info.loc[f'cube_{N}/{N}/{N}', 'allowed_moves'])


# apply deep tree to get group order
grp = Group(Config(monte_carlo=False, schreier_tree='deep'))
add_rubiks_gens(grp, list(move_dict.values()))
print_all_stats(grp)
known_group_order = grp.order()

traces = grp.trace_generators()
for sgs, trace in traces.items():
    p_test = list(range(54))
    for g, inv in trace:
        if inv == 1:
            p_test = [g[i] for i in p_test]
        elif inv == 2:
            for i, j in enumerate(g):
                p_test[j] = i
        else:
            p_test = [p_test[i] for i in g]
        # print(p_test)
    print(list(sgs)==p_test)
    if list(sgs) != p_test and trace:
        print(p_test)
        print(sgs)

# known_group_order = 1038048078587756544000

# # supply start to base for cube faces
# grp = Group(base=center_cubelet_faces)
# print(f'  base perfix = {grp.base()}')
# add_rubiks_gens(grp, list(move_dict.values()))
grp.build(known_group_order)
grp.verify()
print_sgs_stats(grp)

