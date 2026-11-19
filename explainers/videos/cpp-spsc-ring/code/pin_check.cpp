#include <pthread.h>
#include <sched.h>
#include <cstdio>
int main(){ for(int c=0;c<4;c++){cpu_set_t s;CPU_ZERO(&s);CPU_SET(c,&s);int r=pthread_setaffinity_np(pthread_self(),sizeof s,&s);printf("cpu %d -> %d now on %d\n",c,r,sched_getcpu());}}
