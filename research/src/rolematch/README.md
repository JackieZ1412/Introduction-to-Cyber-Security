# De-anonymization

### 生成数据

> 给定一个大型网络 G，我们首先从 G 中随机提取一个子网络作为种子网络，表示为Gs=(Vs,Es)，并使用 中的节点Gs生成已爬网网络G1=(V1,E1)和匿名网络G2=(V2,E2)

这里的G选择Enron数据集，Gs、G1、G2使用[generator.cpp](./data/generator.cpp)在G的基础上生成

G的点集下标范围0~36691 ```generator_seed(lower, upper)```生成所有下标在[lower, upper]之间的点的导出子图
而```generator(int upper, int overlap)```生成G1、G2，它们之间大小几乎相等，只是有1/overlap的重叠

### 运行代码

代码运行在linux上

在```./build```文件夹中执行
```
cmake ..
make
```
完成编译

然后将```./data```文件夹复制到```./build```里面，就可以运行代码

```./Rolematch ai am do_interm overlap```

其中四个命令行参数如下：
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
