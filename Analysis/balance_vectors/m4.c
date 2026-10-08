#include <stdio.h>
int a[16],used[17];
void rec(int p){
  if(p==16){ if(a[0]+a[5]+a[10]+a[15]==34&&a[3]+a[6]+a[9]+a[12]==34){for(int i=0;i<16;i++)printf("%d ",a[i]);printf("\n");}return;}
  int r=p/4,c=p%4;
  for(int v=1;v<=16;v++){ if(used[v])continue;
    if(c==3&&a[p-1]+a[p-2]+a[p-3]+v!=34)continue;
    if(r==3){int s=v;for(int k=0;k<3;k++)s+=a[c+4*k]; if(s!=34)continue;}
    used[v]=1;a[p]=v;rec(p+1);used[v]=0;}
}
int main(){rec(0);}
