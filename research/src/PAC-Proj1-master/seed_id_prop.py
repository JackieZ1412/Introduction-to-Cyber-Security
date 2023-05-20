try:
    import networkx as nx
    import matplotlib.pyplot as plt
except ImportError:
    print ('Fail to import networkx! Programing terminates')
    print ('Please install by: pip install networkx')
    sys.exit()

import copy
import codecs
import os


def __find_k_cliques(G, k):
    rcl = nx.find_cliques_recursive(G)
    k_cliques_list = []
    while True:
        edge_list = []
        try:
            clique_list = next(rcl)
            if len(clique_list) != k:
                continue

            else:
                for i in range(len(clique_list)):
                    for j in range(i+1, len(clique_list)):
                        edge_list.append(G.has_edge(clique_list[i], clique_list[j]))
                        edge_list.append(G.has_edge(clique_list[j], clique_list[i]))

                if all( has_edge is True for has_edge in edge_list):
                    k_cliques_list.append(clique_list)

        except StopIteration:
            break

    if len(k_cliques_list) == 0:
        return None

    else:
        #print "k_cliques_list: ", k_cliques_list
        return k_cliques_list


def __calc_node_cnc(G_undirected, target_node, k_clique):
    sum_cnc = 0

    for node in k_clique:
        if target_node != node:
           sum_cnc += len(sorted(nx.common_neighbors(G_undirected, target_node, node))) #- len(k_clique) + 2
           #print "sum_cnc: ", sum_cnc
    return float(sum_cnc)



def find_k_clique_seed(lgraph, rgraph, k, e):

    """Compute the k-clique seed selection
    This function is implemented based on NetworkX, please install it first!!!
    Args:
        lgraph is the left graph generated using NetworkX
        rgraph is the right graph generated using NetworkX
        k is the number of k-clique
        e is the threshold (epsilon)
    Returns:
        The list of mappings of seeds
    """

    lgraph_k_clqs = __find_k_cliques(lgraph, k)
    rgraph_k_clqs = __find_k_cliques(rgraph, k)

    lgraph_undirected = lgraph.to_undirected()
    rgraph_undirected = rgraph.to_undirected()

    ## mapping from lgraph to rgraph
    seed_mapping = dict()
    seed_mappings = []

    if lgraph_k_clqs is not None and rgraph_k_clqs is not None:
        for lgraph_k_clq in lgraph_k_clqs:
            for rgraph_k_clq in rgraph_k_clqs:
                for lnode in lgraph_k_clq:
                    for rnode in rgraph_k_clq:
                        lnode_cnc = __calc_node_cnc(lgraph_undirected, lnode, lgraph_k_clq)
                        rnode_cnc = __calc_node_cnc(rgraph_undirected, rnode, rgraph_k_clq)
                        lnode_degree = float(lgraph.degree(lnode))
                        rnode_degree = float(rgraph.degree(rnode))
                        #print "lnode, rnode ", lnode_cnc, rnode_cnc


                        if (1-e <= (lnode_cnc/rnode_cnc) <= 1+e) and \
                            (1-e <= (lnode_degree/rnode_degree) <= 1+e):
                            seed_mapping[lnode] = rnode

                if len(seed_mapping) == k:
                    seed_mappings.append(copy.copy(seed_mapping))
                    "seed_mapping.clear()"
                    rgraph_k_clqs.remove(rgraph_k_clq)
                    lgraph_k_clqs.remove(lgraph_k_clq)
                    break

        return seed_mapping

    else:
        print ('No k-cliques have been found')


def PropagationStep(Gl, Gr, mapping):
    lgraph = Gl
    rgraph = Gr
    theta = 0.1
    b = nx.nodes(lgraph)
    b.append([0])
    scores = [0 for lnode in b]

    for lnode in nx.nodes(lgraph):
        if lnode in mapping: continue
        scores[lnode] = matchScores(lgraph, rgraph, mapping, lnode)
        print ("scores[",lnode,"]", scores[lnode])

        if eccentricity(scores[lnode]) < theta : continue
        #print"-----------------------"
        rnode = max(scores[lnode], key=scores[lnode].get)

        scores[rnode] = matchScores(lgraph, rgraph, invert_mapping(mapping), rnode)
        print ("scores[",rnode,"]", scores[rnode])
        #print eccentricity(scores[rnode])
        if eccentricity(scores[rnode]) < theta : continue
        #print"-+++++++++++++++++++++++++---"

        for node in nx.nodes(lgraph):

            if scores[rnode][node] == max(scores[lnode]):
                reverse_match = node

                if reverse_match !=lnode: continue
        mapping[lnode] = rnode
        #print mapping
    return mapping


def matchScores (lgraph, rgraph, mapping, lnode):
    c = nx.nodes(rgraph)
    c.append([0])
    scores = [0 for rnode in c]

    a = lnode

    for (lnbr, lnode_) in nx.edges(lgraph):

        if lnode_ == a:

            if lnbr not in mapping: continue
            rnbr = mapping[lnbr]
            b = rnbr
            for (rnbr_, rnode) in nx.edges(rgraph):
                if rnbr_ == b:
                    if rnode in mapping: continue
                    scores[rnode] += 1 / rgraph.in_degree(rnode) ** 0.5

    for (lnode_, lnbr) in nx.edges(lgraph):

        if lnode_ == a:

            if lnbr not in mapping: continue
            rnbr = mapping[lnbr]

            b = rnbr
            for (rnode,rnbr_) in nx.edges(rgraph):
                if rnbr_ == b:
                    if rnode in mapping: continue
                    scores[rnode] += 1 / rgraph.out_degree(rnode) ** 0.5

    return scores

def eccentricity(items):
    import numpy
    if all(v == 0 for v in items):
        return 0
    else:
        return (max(items) - max_sec(items)) / numpy.std(items)



def max_sec(numbers):
    a = sorted(numbers)
    ma = max(numbers)
    countdown = len(numbers)
    for num in numbers:
        countdown -= 1
        if a[countdown] != ma: break
    return a[countdown]

def invert_mapping(d):
    return dict([(v, k) for k, v in d.items()])





def never_seen_before (node_to_add, user_id, user_name):
    global nodeIndex
    global seen_attributes
    if user_id not in seen_attributes:
        Gaux.add_node(node_to_add, userID = user_id)
        Gaux.node[node_to_add]['userName']=user_name
        nodeIndex=nodeIndex+1
        seen_attributes.add(user_id)
        return True
    return False


if __name__ == '__main__':
    #path = 'C:\Users\JonyC\Documents\GitHub\PAC-Proj1\NodeLists'
    path = '/home/zya1412/PAC-Proj1-master/PAC-Proj1-master/NodeLists'
    os.chdir(path)
    seen_attributes = set()
    Gsan = nx.DiGraph()
    Gaux = nx.DiGraph()

    nodeIndex=1
    fileIndex=1
    for filename in os.listdir(path):
        ''' file Name processing'''
        #print(filename)
        userID = filename[:filename.find('.txt')]
        userName = ''
        # userID = filename[:filename.find(' ')].encode('utf-8')
        # userName = filename[filename.find(' ')+1:filename.find('.txt')].encode('utf-8')

        never_seen = never_seen_before(nodeIndex,userID,userName)

        if never_seen == True:
            fileIndex=nodeIndex-1
        if never_seen == False:
            for i in range(len(seen_attributes)):
                if Gaux.node[i+1]['userID'] == userID:
                    fileIndex=i+1
                    #print "userName: ", Gaux.node[i]['userName']
                    #print "seen_attributes: ", seen_attributes

        data = codecs.open(filename,'r','utf-8')
        line = data.readline()
        while line:
            #print "nodeIndex: ", nodeIndex
            userID = line[:line.find(' ')].encode('utf-8')
            userName = line[line.find(' ')+1:].encode('utf-8')
            never_seen = never_seen_before(nodeIndex,userID,userName)
            if never_seen == False:
                for i in range(len(seen_attributes)):
                    if Gaux.node[i+1]['userID'] == userID:
                        Gaux.add_edge(fileIndex,i+1)
                        #print "fileIndex, nodeIndex i",fileIndex, i+1
            if never_seen ==True:
                Gaux.add_edge(fileIndex,nodeIndex-1)
                #print "fileIndex, nodeIndex", fileIndex, nodeIndex-1

            line = data.readline()
        data.close
    print ("name ", Gaux.node[5]['userName'])
    ''' Gsan Generation'''
    Gsan=Gaux
    for i in range(nx.number_of_nodes(Gsan)):
        Gsan.node[i+1]['userName']=''

    a = find_k_clique_seed(lgraph=Gaux, rgraph=Gsan, k=3, e=0.1)
    print (a)
    nx.draw(Gsan)
    plt.hold(True)
    plt.savefig("path.png")
    ps = PropagationStep(Gaux, Gsan, a)
    print (ps)

    #print "",Gaux.node[0]['userID'], Gaux.node[0]['userName']
    #plt.show()

    Denominator =0.0
    Numerator=0.0
    for node in ps:
        if Gaux.node[node]['userID'] == Gsan.node[ps[node]]['userID']:
            Numerator = Numerator+ Gaux.degree(node)
        Denominator = Denominator + Gaux.degree(node)
    succ_rate = (Numerator/Denominator)*100

    print ("success rate:", succ_rate, "%")
    err_rate = 100-succ_rate
    print ("error rate:",err_rate,"%")
