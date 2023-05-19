## De-anonymizing Social Networks 分析与复现

### 算法分析

本文是社交网络反匿名化领域的开创性工作，提出了一种通用的匿名社交网络重识别算法。该算法只使用社交网络的结构信息，不对不同网络中成员之间的重叠作出任何先验假设，能够有效地实现匿名社交网络的反匿名化。[1]

具体而言，该算法包括以下几个步骤：

1. 数据预处理：通过少量用户的详细信息以及网络爬虫等方法，获取社交网络中大量的用户和关系数据。

2. 社交网络建模：将社交网络建模为一个包含用户与用户间关系信息的图。同时，构建匿名目标图和攻击者辅助图，为后续节点识别做准备。

   ![An example of social network](../assets/map.png)

3. 节点识别：通过**种子查找算法**，识别出匿名目标图和攻击者辅助图中同时存在的少量种子节点，并将它们相互映射。然后，根据种子节点之间的共同邻居和节点度数等信息，将匿名目标图中的节点映射到攻击者辅助图相应的节点。

4. 社交网络重构：利用节点映射关系，不断找出新的映射关系，并加入到原有的关系中，从而实现匿名社交网络的反匿名化。

在这个方法中，最核心的部分就是**种子查找算法**：

该算法分为两个阶段。首先，攻击者鉴别出一小部分“种子”节点，这些节点既存在于匿名目标图中，也存在于攻击者的辅助图中，并将它们相互映射。主要的传播阶段是一个自我加强的过程，使用网络的拓扑结构将种子映射扩展到新节点，并将新的映射反馈给算法。最终的结果是辅助网络和目标网络的子图之间的一个大映射，重新识别了后者中所有映射过的节点。

种子查找算法的输入包括：（1）目标图，（2）k个辅助图中的种子节点，（3）k个节点度值，（4）k个公共邻居计数对，以及（5）误差参数$\theta$。算法在目标图中搜索一个独特的k个节点的完全图，其节点度和公共邻居计数在$1±\theta$的因子范围内匹配。如果找到，则算法将完全图中的节点映射到辅助图中相应的节点；否则，报告失败。

除此之外，算法还需要目标图和辅助图之间的部分“种子”映射$\mu_S$。它输出一个映射$\mu$。可以考虑概率映射，但我们发现将注意力集中在确定性的一一映射$\mu :V_1→V_2$上更简单。直观地，该算法使用网络的拓扑结构和先前构建的映射的反馈来寻找新的映射。它对轻微的拓扑结构修改具有鲁棒性，例如由数据脱敏引入的修改。在每次迭代中，算法从$V_1$和$V_2$之间的累积映射对列表开始。它选择一个未映射的任意节点$u$在$V_1$中，并为$V_2$中的每个未映射节点$v$计算一个分数，该分数等于已映射到$v$的邻居中与$u$相邻的节点数。如果匹配的强度超过阈值$\theta$，则将u和v之间的映射添加到列表中，下一次迭代开始。

还有一些额外的细节和启发式方法需要阐明：

1. Eccentricity：Eccentricity是一种启发式方法，在去匿名化数据库的上下文中使用。它衡量了集合$X$中的一个项目与其他项目之间的差异程度，其中$max$和$max_2$分别表示最高值和第二高值，$σ$表示标准差。我们的算法测量了映射得分集合的离心率（即$v_1$中的单个节点与$v_2$中每个未映射节点之间的映射分数），并且如果离心率得分低于阈值$\theta$，则拒绝该匹配。
   $$
   Eccentricity = \frac{max(X) - max_2(X)}{\delta(X)}
   $$
   
2. Edge directionality：为了计算节点对u和v之间的映射得分，算法计算了两个得分——第一个得分仅基于u和v的入边，第二个得分仅基于出边。然后将这些得分相加。

3. 节点度数：如上所述的映射得分有利于具有高度度数的节点。为了补偿这种偏差，每个节点的得分都除以其度数的平方根。与余弦相似度的原理相同。

4. 重新访问节点：在算法的早期阶段，需要处理的映射较少，因此算法会产生更多的错误。随着算法的进行，映射节点的数量增加，错误率降低。因此需要重新访问已映射的节点：重新访问节点时计算的映射可能会不同，因为有新的映射可用。

5. 反向匹配：该算法对两个图的语义完全不关心。$G_1$是目标图，$G_2$是辅助图，还是反过来都无所谓。每次节点$u$映射到$v$时，都会使用交换输入图的映射得分进行计算。如果$v$映射回$u$，则保留映射；否则，拒绝映射。

6. 复杂度：忽略重新访问节点和反向匹配，该算法的复杂度为$O(|E_1|d_2)$，其中$d_2$是$V_2$中节点度数的上界。

通过2，3的描述可以看出该算法在计算score时采用的余弦相似度作为度量：
$$
cos(X,Y) = \frac{|X \cap Y|}{\sqrt{|X||Y|}}
$$
下图给出了算法的流程的伪代码：

![process](../assets/process.png)

### 复现关键代码

1. Eccentricity计算：直接按照定义实现

   ```python
   def eccentricity(items):
       if all(v == 0 for v in items):
           return 0
       else:
           return (max(items) - max_sec(items)) / numpy.std(items)
   ```

2. 节点匹配的score计算：直接穷举节点对并根据边集合以及余弦相似度计算matchscore：

   ```python
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
   ```

3. 种子算法迭代得出最终映射的过程：

   ```python
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
   ```

4. 寻找k个节点的完全子图：

   ```python
   def find_k_clique_seed(lgraph, rgraph, k, e):
   	'''
   	notes: __find_k_cliques is a method that compute the k cliques in left/right sub map
   		   __calc_node_cnc is a method that compute the number of common neighbours
   	'''
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
   ```

### 结果 & 总结

![output](../assets/output.png)

将数据集转化成拓扑图如上(由于节点太多导致无法清晰表达出拓扑结构)，结果与论文中得到的结果相同，有30%的正确识别率，但是算法的复杂度仍然过高，运行时间**难以想象地长**，这是因为边数和结点个数都过多，而算法的迭代方法也是朴素的暴力迭代，我们相信算法效率的提高和正确率的提高是拓展算法最重要的两个组成部分