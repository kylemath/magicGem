// Simulated annealing with arbitrary two-cell swaps; energy = sum_j ecol_j^2 + sum_i erow_i^2,
// targets: row sums M + rho_i, column sums M + gamma_j.
// usage: anneal2 n seed iters T0 < start(n*n) gamma(n) rho(n)
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static unsigned long long st;
static inline unsigned long long rnd(){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static inline double urand(){return (rnd()>>11)*(1.0/9007199254740992.0);}
int main(int argc,char**argv){
  int n=atoi(argv[1]); st=strtoull(argv[2],0,10)*2654435761ULL+88172645463325252ULL;
  long long iters=atoll(argv[3]); double T0=atof(argv[4]);
  int N=n*n; int *s=malloc(sizeof(int)*N);
  long long *ec=malloc(8*n),*er=malloc(8*n),*tc=malloc(8*n),*tr=malloc(8*n);
  for(int i=0;i<N;i++) if(scanf("%d",&s[i])!=1) return 1;
  long long M=(long long)n*(N+1)/2;
  for(int j=0;j<n;j++){ if(scanf("%lld",&tc[j])!=1) return 1; tc[j]+=M; }
  for(int j=0;j<n;j++){ if(scanf("%lld",&tr[j])!=1) return 1; tr[j]+=M; }
  for(int j=0;j<n;j++){ long long c=0; for(int i=0;i<n;i++) c+=s[i*n+j]; ec[j]=c-tc[j]; }
  for(int i=0;i<n;i++){ long long c=0; for(int j=0;j<n;j++) c+=s[i*n+j]; er[i]=c-tr[i]; }
  long long E=0; for(int j=0;j<n;j++) E+=ec[j]*ec[j]+er[j]*er[j]; long long best=E;
  for(long long it=0; it<iters && E>0; it++){
    double T=T0*(1.0-(double)it/iters)+1e-9;
    int a=rnd()%N, b=rnd()%N; if(a==b) continue;
    int i1=a/n,j1=a%n,i2=b/n,j2=b%n;
    long long d=s[b]-s[a];   // cell a gets +d, cell b gets -d
    long long dE=0;
    if(j1!=j2) dE+=2*d*(ec[j1]-ec[j2])+2*d*d;
    if(i1!=i2) dE+=2*d*(er[i1]-er[i2])+2*d*d;
    if(dE<=0 || urand()<exp(-dE/T)){
      int t=s[a]; s[a]=s[b]; s[b]=t;
      if(j1!=j2){ ec[j1]+=d; ec[j2]-=d; }
      if(i1!=i2){ er[i1]+=d; er[i2]-=d; }
      E+=dE; if(E<best)best=E;
    }
  }
  if(E!=0){ printf("FAIL %lld best %lld\n",E,best); return 0; }
  for(int i=0;i<N;i++) printf("%d ",s[i]); printf("\n"); return 0;
}
