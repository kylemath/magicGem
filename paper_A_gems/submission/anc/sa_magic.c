// Simulated annealing on F = sum over 2n+2 lines (line sum - M)^2 ; stops at first F==0 (magic square).
// usage: sa_magic n nsquares seed steps T0 T1 maxattempts_per_square [semi]  -> prints squares (row-major) one per line
// optional 8th argument semi = 1: rows and columns only (semi-magic squares); default 0: all 2n+2 lines (magic squares)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
static uint64_t s[2];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t nxt(void){uint64_t s0=s[0],s1=s[1],r=s0+s1;s1^=s0;s[0]=rotl(s0,55)^s1^(s1<<14);s[1]=rotl(s1,36);return r;}
static inline double ur(void){return (nxt()>>11)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
  int n=atoi(argv[1]); long nsq=atol(argv[2]); uint64_t seed=strtoull(argv[3],0,10);
  long steps=atol(argv[4]); double T0=atof(argv[5]),T1=atof(argv[6]); long maxatt=atol(argv[7]); int semi=argc>8?atoi(argv[8]):0;
  s[0]=seed*0x9E3779B97F4A7C15ULL+1; s[1]=seed^0xD1B54A32D192ED03ULL; for(int i=0;i<20;i++)nxt();
  int N=n*n, M=n*(N+1)/2, NL=semi?2*n:2*n+2;
  int lines[64][4], nl[64];
  for(int c=0;c<N;c++){int i=c/n,j=c%n;int k=0;lines[c][k++]=i;lines[c][k++]=n+j;if(!semi&&i==j)lines[c][k++]=2*n;if(!semi&&i+j==n-1)lines[c][k++]=2*n+1;nl[c]=k;}
  int v[64]; int ls[64]; long found=0, att=0, totalatt=0;
  double alpha=pow(T1/T0,1.0/steps);
  while(found<nsq && att<maxatt*nsq){
    att++; totalatt++;
    for(int i=0;i<N;i++)v[i]=i+1;
    for(int i=N-1;i>0;i--){int j=nxt()%(i+1);int t=v[i];v[i]=v[j];v[j]=t;}
    for(int l=0;l<NL;l++)ls[l]=-M;
    for(int c=0;c<N;c++)for(int k=0;k<nl[c];k++)ls[lines[c][k]]+=v[c];
    long F=0;for(int l=0;l<NL;l++)F+=(long)ls[l]*ls[l];
    double T=T0;
    for(long st=0;st<steps && F>0;st++,T*=alpha){
      int a=nxt()%N,b=nxt()%N; if(a==b)continue;
      int d=v[b]-v[a]; // cell a gains d, cell b loses d
      int tl[16],td[16],nt=0;
      for(int k=0;k<nl[a];k++){tl[nt]=lines[a][k];td[nt]=d;nt++;}
      for(int k=0;k<nl[b];k++){int l=lines[b][k];int f=0;for(int q=0;q<nt;q++)if(tl[q]==l){td[q]-=d;f=1;break;}if(!f){tl[nt]=l;td[nt]=-d;nt++;}}
      long dF=0;for(int q=0;q<nt;q++){int x=ls[tl[q]];dF+=(long)(x+td[q])*(x+td[q])-(long)x*x;}
      if(dF<=0 || ur()<exp(-dF/T)){
        for(int q=0;q<nt;q++)ls[tl[q]]+=td[q];
        int t=v[a];v[a]=v[b];v[b]=t;F+=dF;
      }
    }
    if(F==0){found++;for(int i=0;i<N;i++)printf("%d%c",v[i],i==N-1?'\n':' ');}
  }
  fprintf(stderr,"n=%d found=%ld attempts=%ld\n",n,found,totalatt);
  return 0;}
