#include <fstream>
#include <random>
#include <iostream>
#include <string>
#include <cassert>
#include <cstdlib>
using namespace std;

#define Max_n 36700
/*
    G1、G2为二维数组，```G1[idx][i]```中的值```idy```表示idx到idy有一条边

    输入文件格式
    第一行两个数字n和y，其中y没用，n是seed图中最大的下标
    下面每行idx、idy表示idx到idy有一条边
*/


//从seed文件生成crawled和anonymized，它们的大小相近
//它们之间有overlap比率的重合
void generator(int lower, int upper, float overlap)
{
    FILE *fp_r = nullptr;
    FILE *fp_w1 = nullptr;
    FILE *fp_w2 = nullptr;
    int idx, idy, r;

    fp_r = fopen("./data/seed.txt", "r");
    fp_w1 = fopen("./data/crawled.txt", "w");
    fp_w2 = fopen("./data/anonymized.txt", "w");
    //写crawled第一行
    fprintf(fp_w1, "%d %d\n", upper, 0);
    //写anonymized第一行
    fprintf(fp_w2, "%d %d\n", upper, 0);
    //不读seed第一行
    fscanf(fp_r, "%d %d", &idx, &idy);
    //确定overlap的节点名单
    bool overlap_v[Max_n];
    int sum = upper - lower + 1;
    for(int i=lower; i<=upper; i++)
    {
        if((rand()%sum) < (sum*overlap))
            overlap_v[i] = true;
        else
            overlap_v[i] = false;
    }
    //确定crawled和anonymized中包含的节点，留存包含overlap_v中节点在内的边，随机分配其余的边
    while (fscanf(fp_r, "%d %d", &idx, &idy) != EOF) {
        if(overlap_v[idx] && overlap_v[idy])
        {
            fprintf(fp_w1, "%d %d\n", idx, idy);
            fprintf(fp_w2, "%d %d\n", idx, idy);
        }
        else
        {
            if(rand()%2)
            {
                fprintf(fp_w1, "%d %d\n", idx, idy);
            }
            else
            {
                fprintf(fp_w2, "%d %d\n", idx, idy);
            }
        }
    }
    fclose(fp_r);
    fclose(fp_w1);
    fclose(fp_w2);
}

// 生成Email-Enron的Gs，其中包含节点标号lower到upper的所有节点
void generator_seed(int lower, int upper)
{
    FILE *fp_r = nullptr;
    FILE *fp_w = nullptr;
    int idx, idy;
    fp_r = fopen("./data/Email-Enron.txt", "r");
    fp_w = fopen("./data/seed.txt", "w");
    assert(fp_r != nullptr);
    // 写第一行
    fprintf(fp_w, "%d %d\n", upper, 0);
    while (fscanf(fp_r, "%d %d", &idx, &idy) != EOF) {
        if(idx < lower)
            continue;
        if(idx > upper)
            break;
        if(idy >= lower && idy <= upper) 
        {
            fprintf(fp_w, "%d %d\n", idx, idy);
        }
    }
    fclose(fp_r);
    fclose(fp_w);
}

// 输入：
// 参数1：图节点标号下界
// 参数2：图节点标号上界
// 参数3：crawled_graph和anonymized_graph重合率
// 参数4：匿名网络的匿名化方法
int main(int argc, char *argv[])
{
    int lower = stoi(argv[1]);
    int upper = stoi(argv[2]);
    float overlap = stof(argv[3]);
    string anonymization = argv[4];
    cout <<"vertices index range from: " << lower << " to " << upper << endl;
    cout <<"overlap rate between crawled_graph and anonymized_graph: " << overlap << endl;
    generator_seed(lower,upper);
    generator(lower, upper, overlap);
    return 0;
}
