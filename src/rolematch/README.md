# De-anonymization

### 生成数据

> 给定一个大型网络 G，我们首先从 G 中随机提取一个子网络作为种子网络，表示为Gs=(Vs,Es)，并使用 中的节点Gs生成已爬网网络G1=(V1,E1)和匿名网络G2=(V2,E2)

这里的G选择Enron数据集，Gs、G1、G2使用[generator.cpp](./data/generator.cpp)在G的基础上生成

G的点集下标范围0~36691 ```generator_seed(lower, upper)```生成所有下标在[lower, upper]之间的点的导出子图Gs
而```generator(lower, upper, overlap)```生成Gs的子图G1、G2，它们有$overlap*(upper-lower)$大小的点集重叠

### 运行代码

代码运行在linux上

运行脚本```./generate_data.sh```可以生成数据集，其中可以自行修改脚本中的参数：
```sh
# config:
lowest_vertice_index=1
highest_vertice_index=2000     #less than 36691
overlap_rate=0.8
anonymization_method="no"
```

运行脚本```./run_code.sh```可以运行代码，其中可以自行修改参数：
```sh
# config:
ai=1
am=1    
do_interm=1
overlap=1600    # = overlap_rate * (highest_vertice_index - lowest_vertice_index + 1)
```

四个参数如下：
* 参数1：ai
  ```
  enum algo_iter {
  VOID_ITER,            // 0
  BASELINE_ITER,        // 1
  ROLESIM,              // 2 Undirected
  ROLESIM_PLUS,         // 3 Extend RoleSim to directed graph
  ALPHA_ROLESIM,        // 4 Threshold sieved RoleSim++
  ALPHA_ROLESIM_SEED,   // 5 RoleSim++ with seed
  };
  ```
* 参数2：am
  ```
  enum algo_match {
  VOID_MATCH,     // 0
  BASELINE_MATCH, // 1
  FEEDBACK,       // 2 Increase neighbours
  FEEDBACK_ALPHA, // 3 Increase neighbours
  FEEDBACK_SEED,  // 4
  PERCOLATE,      // 5 Graph percolation
  COMPARE_TWO     // 6 Compare NeighborMatch && BaselineMatch
  };
  ```
* 参数3：do_interm
  是否计算EvalSimilarity
  取值0、1
* 参数4：指定overlap
  取值整数，含义不详

我使用```./Rolematch 2 2 1 100```
