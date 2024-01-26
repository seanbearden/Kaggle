from ast import literal_eval
import time


def init_reverse_moves(moves):
    new_moves = {}

    for m in moves.keys():
        new_moves[m] = moves[m]
        xform = moves[m]
        m_inv = '-' + m
        xform_inv = len(xform) * [0]
        for i in range(len(xform)):
            xform_inv[xform[i]] = i
        new_moves[m_inv] = xform_inv

    return new_moves


def apply_move(move, state):
    m = move
    s = state.split(';')

    move_list = moves[m]
    new_state = []
    for i in move_list:
        new_state.append(s[i])
    s = new_state

    return ';'.join(s)


def reverse_move(move, state):
    m = move[1:] if move[0] == '-' else '-' + move
    return apply_move(m, state)


def expand(paths, reverse=False):
    states = list(paths.keys())
    for s in states:
        for m in moves:
            if reverse:
                next_s = reverse_move(m, s)
                if not next_s in paths:
                    paths[next_s] = paths[s] + [m]
            else:
                next_s = apply_move(m, s)
                if not next_s in paths:
                    paths[next_s] = paths[s] + [m]


def solve(num_wildcards, allowed_moves, initial_state, solution_state, debug=False):
    global moves, source_paths, dest_paths

    RUN_TIME = 60 * 60 * 24 * 7
    START_TIME = time.time()
    TIMEOUT = RUN_TIME

    moves = literal_eval(allowed_moves)

    moves = init_reverse_moves(moves)

    if num_wildcards < 2:
        source_paths = {
            initial_state: []
        }

        dest_paths = {
            solution_state: []
        }

        start_time = time.time()
        solution = None
        count = 0
        while time.time() - START_TIME < RUN_TIME and time.time() - start_time < TIMEOUT:
            count += 1
            print(count)
            if count % 2:
                expand(source_paths)
            else:
                expand(dest_paths, reverse=True)

            # overlap = list(set(source_paths.keys()).intersection(set(dest_paths.keys())))

            # Assuming source_paths and dest_paths are dictionaries with lists as keys
            source_paths_str = {k for k in source_paths.keys()}
            dest_paths_str = {k for k in dest_paths.keys()}

            # Compute the intersection
            overlap_str = source_paths_str.intersection(dest_paths_str)

            if len(overlap_str) > 0:
                # Convert the string representation back to lists if needed
                # overlap = [s.split(';') for s in overlap_str]
                overlap = list(overlap_str)
                mnsc = 10000000
                mnsl = None
                for oi in range(len(overlap)):
                    ol = overlap[oi]
                    sl = '.'.join(source_paths[ol] + list(reversed(dest_paths[ol])))
                    sz = len(sl.split('.'))
                    if sz < mnsc:
                        mnsc = sz
                        mnsl = sl
                solution = mnsl
                break
    else:
        ssl = solution_state.split(';')
        mn_score = 10000000
        mn_sol = None
        for i in range(len(ssl)):
            for j in range(len(ssl)):
                if j <= i:
                    continue

                sol = None

                ssln = ssl.copy()
                t = ssln[i]
                ssln[i] = ssln[j]
                ssln[j] = t
                ss = ';'.join(ssln)

                source_paths = {
                    initial_state: []
                }

                dest_paths = {
                    ss: []
                }

                start_time = time.time()
                # solution = None
                count = 0
                while time.time() - START_TIME < RUN_TIME and time.time() - start_time < TIMEOUT:
                    count += 1
                    print(count)

                    if count % 2:
                        expand(source_paths)
                    else:
                        expand(dest_paths, reverse=True)

                    # overlap = list(set(source_paths.keys()).intersection(set(dest_paths.keys())))

                    # Assuming source_paths and dest_paths are dictionaries with lists as keys
                    source_paths_str = {k for k in source_paths.keys()}
                    dest_paths_str = {k for k in dest_paths.keys()}

                    # Compute the intersection
                    overlap_str = source_paths_str.intersection(dest_paths_str)


                    if len(overlap_str) > 0:
                        # Convert the string representation back to lists if needed
                        overlap = list(overlap_str)
                        mnsc = 10000000
                        mnsl = None
                        for oi in range(len(overlap)):
                            ol = overlap[oi]
                            sl = '.'.join(source_paths[ol] + list(reversed(dest_paths[ol])))
                            sz = len(sl.split('.'))
                            if sz < mnsc:
                                mnsc = sz
                                mnsl = sl
                                if debug:
                                    print('=> [A] ' + str(sz) + ' : ' + sl)
                        sol = mnsl
                        break

                if sol is not None:
                    sz = len(sol.split('.'))
                    if sz < mn_score:
                        mn_score = sz
                        mn_sol = sol

                        if debug:
                            print('=> {' + str(sz) + '} ' + str(sol))

        solution = mn_sol

    return solution
