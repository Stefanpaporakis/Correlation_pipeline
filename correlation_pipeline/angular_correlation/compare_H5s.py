
#This script compares summed H5 chunks BETWEEN H5 files, you set the size of the chunk,
#then you can check if the correlations are the same between H5 files within the 
#same sample. E.g. If H1 chunk 10 looks the same as H2 chunk 10







import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 


maia_start = 138009

group = '75MO_W_P4_2H'
run = 381
qslice = 32
chunksize = 1 # set chunksize to 1 for full correlation just about
w=0
angle_blur = 0
seperation = 0.1
nstart = 1
##THESE ARE WHERE YOU SELECT THE FILES TO COMPARE###
select_h5_first = [1,2,3] 
select_h5_second = [4,5,6]

maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)

choice = input("compare all or selected h5s? (all/select)")
if choice=="all":
    path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/"
    files = sorted(glob.glob(path+"*nstart"+str(nstart)+"*h5file*.npy"))  
    #print(files)

if choice=="select":
    path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps{chunksize}/"
    files = sorted(glob.glob(path + "*nstart"+str(nstart)+f"*h5file{select_h5_first[0]}""*.npy",))
    files = files+sorted(glob.glob(path + "*nstart"+str(nstart)+f"*h5file{select_h5_first[1]}""*.npy"))
    files = files+sorted(glob.glob(path + "*nstart"+str(nstart)+f"*h5file{select_h5_first[2]}""*.npy"))
    files1 = sorted(glob.glob(path + "*nstart"+str(nstart)+f"*h5file{select_h5_second[0]}""*.npy",))
    files1 = files1+sorted(glob.glob(path + "*nstart"+str(nstart)+f"*h5file{select_h5_second[1]}""*.npy",))
    files1 = files1+sorted(glob.glob(path + "*nstart"+str(nstart)+f"*h5file{select_h5_second[2]}""*.npy",))


slist = []
for i, filename in enumerate(files):
    fname= filename.split('/')[-1]
    runnumf = fname.split('nstart'+str(nstart)+'_')[1]
    legendnum = runnumf.split('_correlation')[-2]
    profile = np.load(filename)
    slist.append(profile)
    integrated_slice = np.sum(np.sum(profile[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
    tmp = integrated_slice*0.0
    for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
    integrated_slice = tmp
    plt.plot(np.arange(0,360,2), integrated_slice+i*seperation, label = legendnum)

if choice == "all":
    plt.title(group+", "+str(run)+", chunksize = "+str(chunksize)+", width = "+str(w)+", angle blur = "+str(angle_blur)+", h5 files")
    plt.legend(loc = 'upper right')
   # plt.yscale("log")
    plt.show()
       

tlist = []
if choice=="select":
    for i, filename in enumerate(files1):
        fname= filename.split('/')[-1]
        runnumf = fname.split('nstart'+str(nstart)+'_')[1]
        legendnum = runnumf.split('_correlation')[-2]
        profile = np.load(filename)
        tlist.append(profile)
        integrated_slice1 = np.sum(np.sum(profile[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
        tmp = integrated_slice*0.0
        for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice1,shift)
        integrated_slice1 = tmp
        plt.plot(np.arange(0,360,2), integrated_slice1+i*2, label = legendnum)
    plt.title(group+", "+str(run)+", chunksize = "+str(chunksize)+", selected h5 files")
    plt.legend(loc = 'upper right')
    plt.show()


if choice == "select":
    first = sum(slist)
    second = sum(tlist)
    plt.plot(np.arange(0,360,2), first[qslice,qslice,:],label = select_h5_first) 
    plt.plot(np.arange(0,360,2), second[qslice,qslice,:], label = select_h5_second)
    plt.legend(loc = 'upper right') 
    plt.title(group+", "+str(run)+", chunksize = "+str(chunksize)+", selected")

if choice=="all":
    plist = []
    fullcorrlist = []
    fullcorra = sorted(glob.glob(path+"*"+str(nstart)+"_a_correlation_sum.npy"))
    fullcorrb = sorted(glob.glob(path+"*"+str(nstart)+"_b_correlation_sum.npy"))
    for a in fullcorra:
        profile = np.load(a)
        plist.append(profile)
    for b in fullcorrb:
        profile = np.load(b)
        plist.append(profile)
    fullcorrlist = sum(plist)
    integrated_slice = np.sum(np.sum(fullcorrlist[qslice-w:qslice+w+1,qslice-w:qslice+w+1,:],0),0)
    tmp = integrated_slice*0.0
    for shift in range(-angle_blur,angle_blur+1): tmp += np.roll(integrated_slice,shift)
    integrated_slice = tmp
    np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+f"corr_nps{chunksize}_fullcorr_sum.npy",fullcorrlist)
    plt.plot(np.arange(0,360,2), integrated_slice)#[qslice,qslice,:]) 
    #plt.yscale("log")
    plt.title(group+", "+str(run)+", chunksize = "+str(chunksize)+", width = "+str(w)+", angle blur = "+str(angle_blur)+", full correlation ")
plt.show()   

