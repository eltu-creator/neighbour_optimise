# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:00:35 2016

@author: ppzfrp
"""
# set up random 3-d positions
#
import numpy as np
import time
import errno
N=np.int(input('N = '))
seed=np.int(input('Random number seed = '))
np.random.seed(seed)
pos=np.random.random((3,N))
start_time=time.time()
# deliberately slow code to find nearest neighbours within periodic unit cube
#
#  You may only change the code in this cell (i.e. between here and "toc")
#
s=np.zeros(shape=(N,N))
#array to store nearest neighbour
match=np.zeros(N)
#find distance between x coordinates
for a in range(N):
    for b in range(N):
        s[a,b]=0.
        offx=0.
        #checks x(a) <= 0.25
        if (pos[0,a]<=0.25):
            #checks x(b) >= 0.75
            if (pos[0,b]>=0.75):
                #means doesn't loop around
                offx=1
        if (pos[0,a]>=0.75):
            if (pos[0,b]<=0.25):
                #means loop around
                offx=-1
        #distance between points add x
        s[a,b]=s[a,b]+(pos[0,a]-pos[0,b]+offx)**2
#
#find distance between y coordinates
for a in range(N):
    for b in range(N):
        offy=0.
        #loops around
        if (pos[1,a]<=0.25):
            if (pos[1,b]>=0.75):
                offy=1
        #doesn't loop around
        if (pos[1,a]>=0.75):
            if (pos[1,b]<=0.25):
                offy=-1
        #distance between points add y
        s[a,b]=s[a,b]+(pos[1,a]-pos[1,b]+offy)**2
#
#find distance between z coordinates
for a in range(N):
    for b in range(N):
        offz=0.
        #loops around
        if (pos[2,a]<=0.25):
            if (pos[2,b]>=0.75):
                offz=1
        #doesn't loop around
        if (pos[2,a]>=0.75):
            if (pos[2,b]<=0.25):
                offz=-1
        #distance between points add z
        s[a,b]=s[a,b]+(pos[2,a]-pos[2,b]+offz)**2
        s[a,b]=np.sqrt(s[a,b])
#
#find the smallest distance
for a in range(N):
    mindist=1e10 #initial big value to compare
    match[a]=0
    for c in range(N):
        if (a!=c):
            #compares min value so far and distance for particular point
            mindist=np.minimum(s[a,c],mindist)
            #assign new min distance if needed
            if (mindist==s[a,c]):
                match[a]=c

end_time=time.time() #toc
print('Elapsed time = ',repr(end_time-start_time))

# generate filename from N and seed
filename='pyneigh'+str(N)+'_'+str(seed)
# if a file with this name already exists read in the nearest neighbour
# list found before and compare this to the current list of neighbours,
# else save the neighbour list to disk for future reference
try:
    fid=open(filename,'rb')
    matchold=np.loadtxt(fid)
    fid.close()
    if (matchold==match).all():
        print('Checked match')
    else:
        print('Failed match')
except OSError as e:
    if e.errno == errno.ENOENT:
        print('Saving neighbour list to disk')
        fid=open(filename,'wb')
        np.savetxt(fid,match,fmt="%8i")
        fid.close()
    else:
        raise
#
