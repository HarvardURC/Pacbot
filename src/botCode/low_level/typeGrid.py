from legends import *

grid = [[I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I], # 0
        [I,c,s,s,c,I,I,c,s,s,c,I,e,e,e,e,e,e,e,e,e,I,c,s,j,l,j,s,s,c,I],
        [I,s,I,I,j,I,I,s,I,I,s,I,e,e,e,e,e,e,e,e,e,I,s,I,I,k,I,I,I,s,I],
        [I,s,I,I,l,k,s,c,I,I,s,I,e,e,e,e,e,e,e,e,e,I,s,I,I,s,I,e,I,s,I],
        [I,s,I,I,j,I,I,I,I,I,s,I,e,e,e,e,e,e,e,e,e,I,s,I,I,s,I,e,I,s,I],
        [I,s,I,I,s,I,I,I,I,I,s,I,I,I,I,I,I,I,I,I,I,I,k,I,I,s,I,I,I,j,I], # 5
        [I,s,I,I,c,s,j,l,j,s,r,s,s,s,s,j,l,j,s,s,s,j,l,j,s,r,s,s,k,l,I],
        [I,s,I,I,I,I,I,k,I,I,s,I,I,I,I,I,k,I,I,I,I,I,I,I,I,s,I,I,I,j,I],
        [I,s,I,I,I,I,I,j,I,I,j,I,I,I,I,I,k,I,I,I,I,I,I,I,I,j,I,e,I,s,I],
        [I,s,I,I,c,s,k,l,I,I,l,k,j,l,j,j,l,j,s,c,I,I,c,s,k,l,I,e,I,s,I],
        [I,s,I,I,s,I,I,j,I,I,j,I,I,k,I,I,I,I,I,s,I,I,s,I,I,j,I,e,I,s,I], # 10
        [I,j,I,I,s,I,I,j,I,I,s,I,I,s,I,n,n,n,I,j,I,I,s,I,I,j,I,I,I,s,I],
        [I,l,k,s,c,I,I,l,k,s,c,I,I,s,I,n,n,n,I,l,k,s,c,I,I,l,k,s,s,c,I],
        [I,j,I,I,I,I,I,j,I,I,I,I,I,s,I,n,n,n,n,j,I,I,I,I,I,j,I,I,I,I,I],
        [I,j,I,I,I,I,I,j,I,I,I,I,I,s,I,n,n,n,n,j,I,I,I,I,I,j,I,I,I,I,I],
        [I,l,k,s,c,I,I,l,k,s,c,I,I,s,I,n,n,n,I,l,k,s,c,I,I,l,k,s,s,c,I], # 15
        [I,j,I,I,s,I,I,j,I,I,s,I,I,s,I,n,n,n,I,j,I,I,s,I,I,j,I,I,I,s,I],
        [I,s,I,I,s,I,I,j,I,I,j,I,I,k,I,I,I,I,I,s,I,I,s,I,I,j,I,e,I,s,I],
        [I,s,I,I,c,s,k,l,I,I,l,k,j,l,j,j,l,j,s,c,I,I,c,s,k,l,I,e,I,s,I],
        [I,s,I,I,I,I,I,j,I,I,j,I,I,I,I,I,k,I,I,I,I,I,I,I,I,j,I,e,I,s,I],
        [I,s,I,I,I,I,I,k,I,I,s,I,I,I,I,I,k,I,I,I,I,I,I,I,I,s,I,I,I,j,I], # 20
        [I,s,I,I,c,s,j,l,j,s,r,s,s,s,s,j,l,j,s,s,s,j,l,j,s,r,s,s,k,l,I],
        [I,s,I,I,s,I,I,I,I,I,s,I,I,I,I,I,I,I,I,I,I,I,k,I,I,s,I,I,I,j,I],
        [I,s,I,I,j,I,I,I,I,I,s,I,e,e,e,e,e,e,e,e,e,I,s,I,I,s,I,e,I,s,I],
        [I,s,I,I,l,k,s,c,I,I,s,I,e,e,e,e,e,e,e,e,e,I,s,I,I,s,I,e,I,s,I],
        [I,s,I,I,j,I,I,s,I,I,s,I,e,e,e,e,e,e,e,e,e,I,s,I,I,k,I,I,I,s,I], # 25
        [I,c,s,s,c,I,I,c,s,s,c,I,e,e,e,e,e,e,e,e,e,I,c,s,j,l,j,s,s,c,I],
        [I,I,I,I,I,I,I,I,I,I,I,I,e,e,e,e,e,e,e,e,e,I,I,I,I,I,I,I,I,I,I]]
#        |         |         |         |         |         |         |
#        0         5        10        15       20         25       30
