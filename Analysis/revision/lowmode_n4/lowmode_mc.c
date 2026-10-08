/*
 * lowmode_mc.c -- Monte Carlo estimate of the probability that a uniformly
 * random arrangement of {1..n^2} satisfies the low-mode conditions.
 * Counts hits for  XY (T1=T2=target), DIAG (both diagonals = M), and L (all four).
 *
 * Build: cc -O3 -march=native -o lowmode_mc lowmode_mc.c
 * Run:   ./lowmode_mc n nsamples seed      (prints one JSON line)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static uint64_t s[4];
static inline uint64_t rotl(uint64_t x,int k){return (x<<k)|(x>>(64-k));}
static inline uint64_t next(void){ /* xoshiro256** */
    uint64_t r=rotl(s[1]*5,7)*9, t=s[1]<<17;
    s[2]^=s[0]; s[3]^=s[1]; s[1]^=s[2]; s[0]^=s[3]; s[2]^=t; s[3]=rotl(s[3],45); return r; }
static uint64_t splitmix(uint64_t *x){ uint64_t z=(*x+=0x9E3779B97F4A7C15ULL);
    z=(z^(z>>30))*0xBF58476D1CE4E5B9ULL; z=(z^(z>>27))*0x94D049BB133111EBULL; return z^(z>>31); }

int main(int argc,char**argv){
    int n=atoi(argv[1]); long long ns=atoll(argv[2]); uint64_t seed=strtoull(argv[3],0,10), st=seed;
    for(int i=0;i<4;i++) s[i]=splitmix(&st);
    int N=n*n; int a[64]; for(int i=0;i<N;i++) a[i]=i+1;
    long T12=(long)(n-1)*N*(N+1)/4, M=(long)n*(N+1)/2;
    long long hxy=0,hd=0,hl=0;
    for(long long t=0;t<ns;t++){
        for(int i=N-1;i>0;i--){ int j=(int)(next()%(uint64_t)(i+1)); int tmp=a[i];a[i]=a[j];a[j]=tmp; }
        long T1=0,T2=0,D1=0,D2=0;
        for(int i=0;i<n;i++){ long rs=0; for(int j=0;j<n;j++){ rs+=a[i*n+j]; T1+=(long)j*a[i*n+j]; }
            T2+=(long)i*rs; D1+=a[i*n+i]; D2+=a[i*n+n-1-i]; }
        int xy=(T1==T12&&T2==T12), d=(D1==M&&D2==M);
        hxy+=xy; hd+=d; hl+=(xy&&d);
    }
    printf("{\"n\": %d, \"samples\": %lld, \"seed\": %llu, \"hits_XY\": %lld, \"hits_DIAG\": %lld, \"hits_L\": %lld}\n",
           n,ns,(unsigned long long)seed,hxy,hd,hl);
    return 0;
}
