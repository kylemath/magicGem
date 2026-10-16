// semimagic4_count.c -- independent depth-first count of the semi-magic squares of order 4 (prints 549504; about 20 s).
// cc -O2 semimagic4_count.c -o semimagic4_count && ./semimagic4_count   (the number asserted in magic_vs_random.py)
#include <stdio.h>
int n=4,N=16,M=34,a[16],used[17],rs[4],cs[4],rc[4],cc[4]; long cnt=0;
void dfs(int c){ if(c==N){cnt++;return;} int i=c/n,j=c%n;
 for(int v=1;v<=N;v++){ if(used[v])continue; int r=rs[i]+v,s=cs[j]+v;
  if(j==n-1 && r!=M) continue; if(i==n-1 && s!=M) continue; if(r>M||s>M) continue;
  used[v]=1; rs[i]=r; cs[j]=s; dfs(c+1); used[v]=0; rs[i]-=v; cs[j]-=v; } }
int main(){dfs(0); printf("%ld\n",cnt);}
