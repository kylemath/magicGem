// Simulated annealing: find arrangement of 1..n^2 with all row sums M and column sums M+gamma_j.
// usage: anneal n seed iters T0 < (start square n*n ints) (gamma n ints)   -> prints square or FAIL
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static unsigned long long st;
static inline unsigned long long rnd(){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static inline double urand(){return (rnd()>>11)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
  int n=atoi(argv[1]); st=strtoull(argv[2],0,10)*2654435761ULL+88172645463325252ULL;
  long long iters=atoll(argv[3]); double T0=atof(argv[4]);
  int N=n*n; int *s=malloc(sizeof(int)*N); long long *e=malloc(sizeof(long long)*n); long long *tg=malloc(sizeof(long long)*n);
  for(int i=0;i<N;i++) if(scanf("%d",&s[i])!=1) return 1;
  long long M=(long long)n*(N+1)/2;
  for(int j=0;j<n;j++){ if(scanf("%lld",&tg[j])!=1) return 1; tg[j]+=M; }
  for(int j=0;j<n;j++){ long long c=0; for(int i=0;i<n;i++) c+=s[i*n+j]; e[j]=c-tg[j]; }
  long long E=0; for(int j=0;j<n;j++) E+=e[j]*e[j]; long long best=E;
  for(long long it=0; it<iters && E>0; it++){
    double T=T0*(1.0-(double)it/iters)+1e-9;
    int i=rnd()%n, j=rnd()%n, k=rnd()%n; if(j==k) continue;
    long long d=s[i*n+k]-s[i*n+j];
    long long dE=2*d*(e[j]-e[k])+2*d*d;
    if(dE<=0 || urand()<exp(-dE/T)){
      int t=s[i*n+j]; s[i*n+j]=s[i*n+k]; s[i*n+k]=t; e[j]+=d; e[k]-=d; E+=dE; if(E<best)best=E;
    }
  }
  if(E!=0){ printf("FAIL %lld best %lld\n",E,best); return 0; }
  for(int i=0;i<N;i++) printf("%d ",s[i]); printf("\n"); return 0;
}
