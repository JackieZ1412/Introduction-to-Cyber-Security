import random

def propagationStep(lgraph, rgraph, mapping, theta):
    scores = {}
    for lnode in lgraph.nodes:
        scores[lnode] = matchScores(lgraph, rgraph, mapping, lnode)
        if eccentricity(list(scores[lnode].values())) < theta:
            continue
        rnode = max(scores[lnode], key=scores[lnode].get)
        scores[rnode] = matchScores(rgraph, lgraph, invert(mapping), rnode)
        if eccentricity(list(scores[rnode].values())) == max(list(scores[rnode].values())):
            reverse_match = max(scores[rnode], key=scores[rnode].get)
            if reverse_match == lnode:
                mapping[lnode] = rnode

def matchScores(lgraph, rgraph, mapping, lnode):
    scores = {}
    for rnode in rgraph.nodes:
        if rnode not in mapping.values():
            mapping[lnode] = rnode
            scores[rnode] = calculateScore(lgraph, rgraph, mapping)
            del mapping[lnode]
    return scores

def eccentricity(items):
    items = list(items.values())
    return ((max(items)-max2(items))/std_dev(items))

# until convergence do:
#     propagationStep(lgraph, rgraph, seed_mapping)