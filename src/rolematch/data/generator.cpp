#include <fstream>
#include <random>
#include <iostream>
#include <cassert>
#include <cstdlib>
using namespace std;
/*
    G1、G2为二维数组，```G1[idx][i]```中的值```idy```表示idx到idy有一条边

    输入文件格式
    第一行两个数字n和y，其中y没用，n是seed图中最大的下标
    下面每行idx、idy表示idx到idy有一条边
*/


//从seed文件生成crawled和anonymized，它们之间有1/overlap的重合
void generator(int upper, int overlap)
{
    FILE *fp_r = nullptr;
    FILE *fp_w1 = nullptr;
    FILE *fp_w2 = nullptr;
    int idx, idy, r;
    int count=0;

    fp_r = fopen("./seed.txt", "r");
    fp_w1 = fopen("./crawled.txt", "w");
    fp_w2 = fopen("./anonymized.txt", "w");
    //写crawled第一行
    fprintf(fp_w1, "%d %d\n", upper, 0);
    //写anonymized第一行
    fprintf(fp_w2, "%d %d\n", upper, 0);
    //不读seed第一行
    fscanf(fp_r, "%d %d", &idx, &idy);
    //crawled并anonymized等于seed，所以一半一半
    while (fscanf(fp_r, "%d %d", &idx, &idy) != EOF) {
        if(count%2)
        {
            fprintf(fp_w1, "%d %d\n", idx, idy);
        }
        else
        {
            fprintf(fp_w2, "%d %d\n", idx, idy);
        }
        count++;
    }
    fclose(fp_r);
    fclose(fp_w1);
    fclose(fp_w2);

    //从crawled里面抽1/overlap复制到anonymized里面
    fp_r = fopen("./crawled.txt", "r");
    fp_w2 = fopen("./anonymized.txt", "a");
    count=1;
    while (fscanf(fp_r, "%d %d", &idx, &idy) != EOF) {
        if(count%overlap==0) 
        {
            fprintf(fp_w2, "%d %d\n", idx, idy);
        }
        count++;
    }
    fclose(fp_r);
    fclose(fp_w2);
    
}

//Email-Enron的
void generator_seed(int lower, int upper)
{
    FILE *fp_r = nullptr;
    FILE *fp_w = nullptr;
    int idx, idy;
    fp_r = fopen("./Email-Enron.txt", "r");
    fp_w = fopen("./seed.txt", "w");
    assert(fp_r != nullptr);
    //写第一行
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

int main()
{
    int lower = 1;
    int upper = 100;
    srand(114);
    generator_seed(lower,upper);
    generator(upper, 5);
    return 0;
}