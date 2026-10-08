/*
 * lowmode_enum.c -- exact meet-in-the-middle enumeration of n x n arrangements
 * of {1,...,N}, N = n^2, satisfying a set of LINEAR statistics
 *     T_m(S) = sum_{cells c} w_m[c] * s_c  ==  target_m .
 *
 * The cells are split into A = first k cells (row-major) and B = the remaining
 * N-k cells.  For every k-subset V of values and every bijection V -> A we pack
 * the partial statistics into a 64-bit key; for the complementary value set and
 * every bijection V^c -> B we compute (target - partial) and look it up.  Keys
 * are matched by sorting both key lists and merging.  Subsets are distributed
 * over pthreads.
 *
 * Modes (second argument):
 *   L         T1 = sum j*s_ij, T2 = sum i*s_ij, T3 = main diag, T4 = anti diag
 *             (the low-mode balanced class: Cov(X,Z)=Cov(Y,Z)=Cov(Dmain,Z)=Cov(Danti,Z)=0).
 *             Members are enumerated explicitly: breakdown by (#rows = M, #cols = M)
 *             is printed, and with a third argument the members are written to a
 *             binary file (N bytes per arrangement, row-major, values 1..N).
 *   XY        T1, T2 only (first-moment balance, no diagonals) -- count only.
 *   DIAG      T3, T4 only -- count only.
 *   MAGIC     all row sums, all column sums, both diagonals = M -- count only.
 *   SEMI      all row sums and column sums = M (semi-magic) -- count only.
 *   ROWSL     L plus all row sums = M  -- count only (cross-check of breakdown).
 *   COLSL     L plus all column sums = M -- count only.
 *
 * Build:  cc -O3 -march=native -o lowmode_enum lowmode_enum.c -lpthread
 * Run:    ./lowmode_enum 4 L members_n4.bin
 *
 * Author: Kyle Elliott Mathewson.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include <time.h>

#define MAXN 5
#define MAXCELLS (MAXN*MAXN)
#define MAXSTATS 10
#define MAXK 13          /* largest half we ever permute (n=5: 12/13) */

static int n, N, K, KB;          /* K = |A|, KB = |B| = N-K */
static int nstats;
static int w[MAXSTATS][MAXCELLS];
static long target[MAXSTATS];
static int shift_[MAXSTATS], bits_[MAXSTATS];
static long maxA_[MAXSTATS];
static long Mtarget;

static int nthreads = 16;
static int save_members = 0;
static int enum_mode = 0;   /* 1 for mode L: enumerate members explicitly */
static const char *outname = NULL;

/* permutations */
static uint8_t *permA, *permB;     /* [nA][K], [nB][KB] */
static long nA, nB;

/* subsets */
static uint32_t *subsets; static long nsub;

typedef struct { uint64_t key; uint32_t idx; } KI;

static long factorial(int m){ long f=1; for(int i=2;i<=m;i++) f*=i; return f; }

static uint8_t *gen_perms(int m, long *count){
    long cnt = factorial(m); *count = cnt;
    uint8_t *P = malloc((size_t)cnt*m);
    int a[MAXK]; for(int i=0;i<m;i++) a[i]=i;
    for(long p=0;p<cnt;p++){
        for(int i=0;i<m;i++) P[p*m+i]=(uint8_t)a[i];
        /* next_permutation */
        int i=m-2; while(i>=0 && a[i]>=a[i+1]) i--;
        if(i<0) break;
        int j=m-1; while(a[j]<=a[i]) j--;
        int t=a[i];a[i]=a[j];a[j]=t;
        for(int l=i+1,r=m-1;l<r;l++,r--){t=a[l];a[l]=a[r];a[r]=t;}
    }
    return P;
}

static int cmp_ki(const void*a,const void*b){
    uint64_t x=((const KI*)a)->key, y=((const KI*)b)->key;
    return x<y?-1:(x>y?1:0);
}
static int cmp_u64(const void*a,const void*b){
    uint64_t x=*(const uint64_t*)a, y=*(const uint64_t*)b;
    return x<y?-1:(x>y?1:0);
}

/* per-thread results */
typedef struct {
    int tid;
    uint64_t count;            /* number of matching arrangements */
    uint64_t hist[MAXN+1][MAXN+1];   /* [#rows==M][#cols==M] (L mode) */
    uint8_t *members; size_t nmem, capmem;  /* saved members (L mode) */
} TRes;

static void push_member(TRes *r, const uint8_t *s){
    if(r->nmem==r->capmem){ r->capmem = r->capmem? r->capmem*2 : 1<<16; r->members = realloc(r->members, r->capmem*(size_t)N); }
    memcpy(r->members + r->nmem*(size_t)N, s, N); r->nmem++;
}

static void *worker(void *arg){
    TRes *r = (TRes*)arg;
    KI  *ka = malloc(sizeof(KI)*nA);
    KI  *kb = malloc(sizeof(KI)*nB);
    int vals[MAXCELLS], comp[MAXCELLS];
    uint8_t sq[MAXCELLS];
    int enumerate = enum_mode;
    for(long si=r->tid; si<nsub; si+=nthreads){
        uint32_t mask = subsets[si];
        int a=0,b=0;
        for(int v=1; v<=N; v++){ if(mask>>(v-1)&1) vals[a++]=v; else comp[b++]=v; }
        /* side A */
        for(long p=0;p<nA;p++){
            const uint8_t *pp = permA + p*K;
            uint64_t key=0;
            for(int m=0;m<nstats;m++){
                long t=0;
                for(int c=0;c<K;c++) t += (long)w[m][c]*vals[pp[c]];
                key |= ((uint64_t)t) << shift_[m];
            }
            ka[p].key=key; ka[p].idx=(uint32_t)p;
        }
        /* side B */
        long nb_valid=0;
        for(long q=0;q<nB;q++){
            const uint8_t *pq = permB + q*KB;
            uint64_t key=0; int ok=1;
            for(int m=0;m<nstats;m++){
                long t=0;
                for(int c=0;c<KB;c++) t += (long)w[m][K+c]*comp[pq[c]];
                long need = target[m]-t;
                if(need<0 || need>maxA_[m]){ ok=0; break; }
                key |= ((uint64_t)need) << shift_[m];
            }
            if(ok){ kb[nb_valid].key=key; kb[nb_valid].idx=(uint32_t)q; nb_valid++; }
        }
        qsort(ka,nA,sizeof(KI),cmp_ki);
        qsort(kb,nb_valid,sizeof(KI),cmp_ki);
        long i=0,j=0;
        while(i<nA && j<nb_valid){
            if(ka[i].key<kb[j].key) i++;
            else if(ka[i].key>kb[j].key) j++;
            else {
                uint64_t k=ka[i].key; long i2=i,j2=j;
                while(i2<nA && ka[i2].key==k) i2++;
                while(j2<nb_valid && kb[j2].key==k) j2++;
                r->count += (uint64_t)(i2-i)*(uint64_t)(j2-j);
                if(enumerate){
                    for(long x=i;x<i2;x++) for(long y=j;y<j2;y++){
                        const uint8_t *pp=permA+ka[x].idx*K, *pq=permB+kb[y].idx*KB;
                        for(int c=0;c<K;c++) sq[c]=(uint8_t)vals[pp[c]];
                        for(int c=0;c<KB;c++) sq[K+c]=(uint8_t)comp[pq[c]];
                        int rk=0,ck=0;
                        for(int rr=0;rr<n;rr++){ long s=0; for(int cc=0;cc<n;cc++) s+=sq[rr*n+cc]; rk += (s==Mtarget); }
                        for(int cc=0;cc<n;cc++){ long s=0; for(int rr=0;rr<n;rr++) s+=sq[rr*n+cc]; ck += (s==Mtarget); }
                        r->hist[rk][ck]++;
                        if(save_members) push_member(r,sq);
                    }
                }
                i=i2;j=j2;
            }
        }
    }
    free(ka); free(kb);
    return NULL;
}

static void add_stat(const int *wc, long tgt){
    memcpy(w[nstats], wc, sizeof(int)*N); target[nstats]=tgt; nstats++;
}

int main(int argc, char **argv){
    if(argc<3){ fprintf(stderr,"usage: %s n MODE [members.bin] [threads]\n",argv[0]); return 1; }
    n=atoi(argv[1]); N=n*n; const char *mode=argv[2];
    if(argc>=4 && strcmp(argv[3],"-")!=0){ save_members=1; outname=argv[3]; }
    if(argc>=5) nthreads=atoi(argv[4]);
    K = N/2; KB = N-K;           /* n=3: 4/5, n=4: 8/8, n=5: 12/13 */
    Mtarget = (long)n*(N+1)/2;
    long T12 = (long)(n-1)*N*(N+1)/4;   /* ((n-1)/2) * N(N+1)/2 */

    int wc[MAXCELLS];
    nstats=0;
#define CELLW(expr) for(int c=0;c<N;c++){ int i=c/n, j=c%n; (void)i;(void)j; wc[c]=(expr); }
    int useL = !strcmp(mode,"L") || !strcmp(mode,"ROWSL") || !strcmp(mode,"COLSL");
    if(useL || !strcmp(mode,"XY")){
        CELLW(j); add_stat(wc,T12);
        CELLW(i); add_stat(wc,T12);
    }
    if(useL || !strcmp(mode,"DIAG") || !strcmp(mode,"MAGIC")){
        CELLW(i==j); add_stat(wc,Mtarget);
        CELLW(i+j==n-1); add_stat(wc,Mtarget);
    }
    if(!strcmp(mode,"MAGIC")||!strcmp(mode,"SEMI")||!strcmp(mode,"ROWSL")){
        for(int r=0;r<n-1;r++){ CELLW(i==r); add_stat(wc,Mtarget); }
    }
    if(!strcmp(mode,"MAGIC")||!strcmp(mode,"SEMI")||!strcmp(mode,"COLSL")){
        for(int col=0;col<n-1;col++){ CELLW(j==col); add_stat(wc,Mtarget); }
    }
    if(nstats==0){ fprintf(stderr,"unknown mode %s\n",mode); return 1; }
    if(strcmp(mode,"L")) save_members=0; else enum_mode=1;

    /* key layout: bound on A-side partial = sum over A cells of w*N */
    int sh=0;
    for(int m=0;m<nstats;m++){
        long mx=0; for(int c=0;c<K;c++) mx += (long)w[m][c]*N;
        maxA_[m]=mx; int b=1; while((1L<<b) <= mx) b++;
        bits_[m]=b; shift_[m]=sh; sh+=b;
    }
    if(sh>64){ fprintf(stderr,"key too wide (%d bits)\n",sh); return 1; }

    permA = gen_perms(K,&nA); permB = gen_perms(KB,&nB);
    /* subsets of size K of {1..N} as bitmasks (Gosper) */
    nsub=0; { long cap=1<<20; subsets=malloc(sizeof(uint32_t)*cap);
      uint32_t x=(1u<<K)-1, lim=1u<<N;
      while(x<lim){ subsets[nsub++]=x; uint32_t u=x&-x, v=u+x; x = v + (((v^x)/u)>>2); }
    }
    fprintf(stderr,"n=%d N=%d K=%d mode=%s stats=%d keybits=%d subsets=%ld permsA=%ld permsB=%ld threads=%d\n",
            n,N,K,mode,nstats,sh,nsub,nA,nB,nthreads);

    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    pthread_t th[64]; TRes res[64]; memset(res,0,sizeof(res));
    for(int t=0;t<nthreads;t++){ res[t].tid=t; pthread_create(&th[t],NULL,worker,&res[t]); }
    uint64_t total=0, hist[MAXN+1][MAXN+1]; memset(hist,0,sizeof(hist)); size_t nmem=0;
    for(int t=0;t<nthreads;t++){ pthread_join(th[t],NULL); total+=res[t].count; nmem+=res[t].nmem;
        for(int a=0;a<=n;a++)for(int b=0;b<=n;b++) hist[a][b]+=res[t].hist[a][b]; }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double secs=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);

    printf("{\"n\": %d, \"mode\": \"%s\", \"count\": %llu, \"seconds\": %.2f, \"threads\": %d",
           n,mode,(unsigned long long)total,secs,nthreads);
    if(!strcmp(mode,"L")){
        printf(", \"hist_rows_cols_equal_M\": {");
        int first=1;
        for(int a=0;a<=n;a++)for(int b=0;b<=n;b++) if(hist[a][b]){
            printf("%s\"%d,%d\": %llu",first?"":", ",a,b,(unsigned long long)hist[a][b]); first=0; }
        printf("}");
    }
    printf("}\n");
    if(save_members){
        FILE *f=fopen(outname,"wb");
        for(int t=0;t<nthreads;t++) if(res[t].nmem) fwrite(res[t].members,N,res[t].nmem,f);
        fclose(f);
        fprintf(stderr,"wrote %zu members to %s\n",nmem,outname);
    }
    return 0;
}
