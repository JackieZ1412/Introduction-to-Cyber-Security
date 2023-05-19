#pragma once

#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <vector>
#include <set>
#include <unordered_map>
#include <cassert>
#include <algorithm>
#include <sys/time.h>
/*
#include <time.h>
#include <windows.h>
int gettimeofday(struct timeval *tp, void *tzp)
{
    time_t clock;
    struct tm tm;
    SYSTEMTIME wtm;
    GetLocalTime(&wtm);
    tm.tm_year = wtm.wYear - 1900;
    tm.tm_mon = wtm.wMonth - 1;
    tm.tm_mday = wtm.wDay;
    tm.tm_hour = wtm.wHour;
    tm.tm_min = wtm.wMinute;
    tm.tm_sec = wtm.wSecond;
    tm.tm_isdst = -1;
    clock = mktime(&tm);
    tp->tv_sec = clock;
    tp->tv_usec = wtm.wMilliseconds * 1000;
    return (0);
}
*/

#define ITER_NUM 5
#define BETA 0.15
#define ALPHA 0.85
#define MAX_THREAD 16
#define THETA 0.85
using namespace std;

enum algo_iter {
  VOID_ITER,            // 0
  BASELINE_ITER,        // 1
  ROLESIM,              // 2 Undirected
  ROLESIM_PLUS,         // 3 Extend RoleSim to directed graph
  ALPHA_ROLESIM,        // 4 Threshold sieved RoleSim++
  ALPHA_ROLESIM_SEED,   // 5 RoleSim++ with seed
};

enum algo_match {
  VOID_MATCH,     // 0
  BASELINE_MATCH, // 1
  FEEDBACK,       // 2 Increase neighbours
  FEEDBACK_ALPHA, // 3 Increase neighbours
  FEEDBACK_SEED,  // 4
  PERCOLATE,      // 5 Graph percolation
  COMPARE_TWO     // 6 Compare NeighborMatch && BaselineMatch
};

class node_pair {
 public:
  int id1, id2;
  node_pair(int x, int y) {
    id1 = x;
    id2 = y;
  }
  bool operator < (const node_pair &a) const {
    return (id1 < a.id1 || (id1 == a.id1 && id2 < a.id2));
  }
  bool operator == (const node_pair &a) const {
    return (id1 == a.id1 && id2 == a.id2);
  }
};

class timer{
  long int time_start, time_end;
public:
  double delta;
  timer(){
  }
  void start(){
      struct timeval tval;
    gettimeofday(&tval, NULL);
    time_start = tval.tv_sec * 1000 + tval.tv_usec / 1000;
  }
  void end(){
      struct timeval tval;
    gettimeofday(&tval, NULL);
    time_end = tval.tv_sec * 1000 + tval.tv_usec / 1000;
      delta = (double)(time_end - time_start) / 1000;
  }

};

// G1: crawled; G2: anonymized
typedef vector< vector<int> > Graph;
extern Graph G1, G2;
// Reversed graph
extern Graph RG1, RG2;

extern vector<int> seed_set;

// Similarity matrix
typedef vector< double > Vec;
typedef vector< Vec > SimMat;
extern SimMat sim_score[2];

// Threshold sieved similarity scores
typedef unordered_map<int, double> SVec;
typedef vector< SVec > SSimMat;

extern SSimMat ssim_score[2];

// Number of nodes
extern int n1, n2;

// Graph preprocess: read graph and add neighbors to the vector
extern void PreprocessGraph(algo_iter ai, algo_match am);

// Calculate similarity matrix
extern void CalcSimilarity(algo_iter ai);

// Analyze intermediate result
void EvalSimilarity(algo_iter ai, int overlap);

// Match two graphs based on similarity score
extern void MatchGraph(algo_match am, int overlap);

void PrintMatrix(const SimMat &sim_score);
void OutputMatrix(const SSimMat &sim_score);
