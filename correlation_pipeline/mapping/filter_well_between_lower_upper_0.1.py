




# Filters between a range, gives x and y pixel value for each
# peak position, that way we can focus on certain areas for correlations



import fluxfm
import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import glob
import pathlib 
import h5py
import hdf5plugin
import csv
from matplotlib.colors import LinearSegmentedColormap


def h5info(total_length, individual_lengths):
    result = []
    h5start = 1
    for i in individual_lengths:
        for j in range(i):
            if len(result)<total_length:
                result.append(h5start)
            else:
                break
        h5start +=1
        if len(result) >=total_length:
            break
    return result      

def h5frame(individual_lengths):
    frame = []
    for frame_number,length in enumerate(individual_lengths, start = 0):
        for frame_position in range(1,length+1):
            frame.append(frame_position)
    return frame

def final_plot(ignore_ia3d,hinit,binit,red_well,bool_list,well_list,xpix,ypix): 
    xpix = np.array(xpix, dtype = 'int')
    ypix = np.array(ypix, dtype = 'int')
    xmin = min(xpix)
    ymin = min(ypix)
    xmax = max(xpix)
    ymax = max(ypix)

    #check if x, y and data is the same length
    xlen = int(len(xpix))
    well_list  = well_list[:xlen]
    bool_list = bool_list[:xlen]

    if len(ypix)==len(xpix)==len(well_list):
        #im = np.zeros((260,135))
        im = np.zeros((xmax-xmin+1,ymax-ymin+1))
        for x,y,d in zip(xpix,ypix,well_list):
            im[x-xmin,y-ymin] = d
 
    if len(ypix)==len(xpix)==len(bool_list):
        #im = np.zeros((260,135))
        imr = np.zeros((xmax-xmin+1,ymax-ymin+1))
        for x,y,e in zip(xpix,ypix,bool_list):
            imr[x-xmin,y-ymin] = e  


    
    else:
        print("lengths aren't the same for x, y and data")
        print("y is ", len(ypix))
        print("x is ", len(xpix))
        print("data is ", len(d_list))
        exit() 
        
        
    colors = [(0,0,0),(0,0.5,0)]
    color_map = LinearSegmentedColormap.from_list('black_to_green',colors)
    if ignore_ia3d== True:
        fig,ax = plt.subplots(1,2,figsize = (10,5))
        b = ax[0].imshow(imr, origin = 'lower',aspect = 125/250, clim = [0,1], cmap = color_map)
        ax[0].set_title('filtered '+str(run)+" "+analysis[:-4])
        hfull,bfull = np.histogram(im,bins = 34000,range = (lower,upper)) 
        ax[1].plot(bfull[:-1],hfull, color = colors[0], label = 'full')
        hred,bred = np.histogram(red_well,bins = 34000,range = (lower,upper))
        ax[1].plot(bred[:-1],hred, color = colors[1], label = 'filtered to exclude '+str(res1)+' ' +str(res2))
        ax[1].legend(loc = 'upper left')
        count = np.count_nonzero(imr == 1)
        perc = (count/imr.size)*100
        print(str(perc)+' % of well has first radial peak outside '+str(res1)+' '+str(res2)+' q range')
        plt.show()
    if ignore_ia3d!=True:
        fig,ax = plt.subplots(1,2,figsize = (10,5))
        b = ax[0].imshow(imr, origin = 'lower',aspect = 125/250, clim = [0,1], cmap = color_map)
        ax[0].set_title('filtered '+str(run)+" "+analysis[:-4])
        ax[1].plot(binit[:-1],hinit, color = colors[0], label = 'full')
        hred,bred = np.histogram(red_well,bins = 34000,range = (lower,upper))
        ax[1].plot(bred[:-1],hred, color = colors[1], label = 'filtered to '+str(lower)+'-'+str(upper))
        plt.legend(loc = 'upper left')
        count = np.count_nonzero(imr == 1)
        perc = (count/imr.size)*100
        print(str(perc)+' % of well has first radial peak in '+str(lower)+'-'+str(upper)+' q range')
        plt.show()

def init_plot(well_list,xpix,ypix): 
    xpix = np.array(xpix, dtype = 'int')
    ypix = np.array(ypix, dtype = 'int')
    xmin = min(xpix)
    ymin = min(ypix)
    xmax = max(xpix)
    ymax = max(ypix)

    #check if x, y and data is the same length
    xlen = int(len(xpix))
    well_list  = well_list[:xlen]

    if len(ypix)==len(xpix)==len(well_list):
        #im = np.zeros((260,135))
        initim = np.zeros((xmax-xmin+1,ymax-ymin+1))
        for x,y,d in zip(xpix,ypix,well_list):
            initim[x-xmin,y-ymin] = d
        fig,ax = plt.subplots(1,2,figsize = (10,5))
        a = ax[0].imshow(initim, origin = 'lower',aspect = 125/250,clim = [lower,upper])
        plt.colorbar(a,ax = ax[0])
        hinit,binit= np.histogram(initim,bins = 34000,range = (lower,upper)) 
        ax[1].plot(binit[:-1],hinit)
        plt.show()
        
    
    else:
        print("lengths aren't the same for x, y and data")
        print("y is ", len(ypix))
        print("x is ", len(xpix))
        print("data is ", len(d_list))
        exit() 
    return hinit,binit



maia_start = 138009
group = '75MO_W_P4_2H'
run = 383
xyfile = 138009+int(run)
lower= 0.25 #Need to set these for ia3d ignore
upper = 2
ignore_ia3d = True
h5number = 4 #How many h5 files are there, very important parameter


analysis = 'radial_peak_position.npy'
maia_num = maia_start + run
tag = str(maia_num)+"_"+str(run)
analysis_path = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/"

#Load well and append all data to list, and tell you what the most common number is
well_list = []
well = np.load(analysis_path+analysis, allow_pickle=True)
#print(len(well))
well[well == None] = 0
unique,counts = np.unique(well,return_counts = True)
most_common = unique[np.argmax(counts)]
print("most common "+analysis[:-4]+" for entire well is",most_common)
for i in well:
    well_list.append(i)


    #load x and y points from csv file
xpix = []
ypix = []
xy_path = f"/data/xfm/20027/analysis/xy/{xyfile}/"
with open (xy_path+str(xyfile)+"-et-marker-stage-cv.csv", newline ='') as xy:
    xyreader = csv.reader(xy,delimiter = ',')
    for row in xyreader:
        xpix.append(row[5])
        ypix.append(row[6])
hinit,binit = init_plot(well_list,xpix,ypix)


retry = True
while retry:
    bool_list  = []

    if ignore_ia3d == True:
        print('ignore between? (lower,upper)')
        res1,res2 = input().split()
        res1 = float(res1)
        res2 = float(res2)
        boolwell = (well>lower)*(well<upper)
        boolwell = (well<res1)+(well>res2)
        red_well = [num for num in well if lower<=num<=upper]
        red_well = [num for num in red_well if num <res1 or num>res2]
    if ignore_ia3d ==False:
        print('filter between? (lower,upper)')
        lower,upper = input().split()
        lower = float(lower)
        upper = float(upper)
        boolwell = (well>lower)*(well<upper)
        red_well = [num for num in well if lower<=num<=upper]
    for i in boolwell:
        bool_list.append(i)

    
#Merge lists to only contain values where boolwell is true, and the most common value in the reduced dataset
    filtered_list = []
    filtered_well = [value for i, value in enumerate(well) if boolwell[i]]
    unique,counts = np.unique(filtered_well,return_counts = True)
    most_common = unique[np.argmax(counts)]
    print("most common " +analysis[:-4]+" for filtered well is",most_common)
    for i in filtered_well:
        filtered_list.append(i)


# save xy values to list if boolean is true
    x_list = []
    y_list = []
    x_data = [value for i, value in enumerate(xpix) if boolwell[i]]
    for i in x_data:
        x_list.append(i)
    y_data = [value for i, value in enumerate(ypix) if boolwell[i]]
    for i in y_data:
        y_list.append(i)


#make a list of vlaues that correspond to the h5 file size the crop for the 
#boolean values to get what h5 file each frame cam from
    h5_list = []
    frame_list = []
    total_length = int(len(well)) #run 381
    print("total frames is ", total_length)
    print("reduced number of frames to ", len(filtered_list))
    #individual_lengths = [9999,9999,9999,total_length-30000]#run 381
    individual_lengths = [9999]*(h5number - 1)
    x = sum(individual_lengths)
    individual_lengths.append(total_length-x)
    h5data = h5info(total_length,individual_lengths)
    frame_data = h5frame(individual_lengths)
    h5data = [value for i, value in enumerate(h5data) if boolwell[i]]
    for i in h5data:
        h5_list.append(i)
    frame_data = [value for i, value in enumerate(frame_data) if boolwell[i]]
    for i in frame_data:
        frame_list.append(i)


#make everything the same length
    xlen = int(len(x_list))
    filtered_list  = filtered_list[:xlen]
    h5_list = h5_list[:xlen]
    frame_list = frame_list[:xlen]
#print(len(h5_list))
#print (len(filtered_list))
#print(len(x_list))
#print(len(y_list))

    plot = final_plot(ignore_ia3d,hinit,binit,red_well,bool_list,well_list,xpix,ypix)
    response = input('try again? [y/n]')
    if response !='y':
        retry = False
#save to a file (.txt in this case)
        if analysis =='summed_intensity.npy':
            analysis_path = analysis_path+'/intpeaks/'
        if analysis == 'max_value.npy':
            analysis_path = analysis_path+'/maxpeaks/'
        if analysis =='radial_peak_position.npy':
            analysis_path = analysis_path+'/radpeakpos/'
        if analysis =='radial_peak_height.npy':
            analysis_path = analysis_path+'/radpeakheight/'
        if os.path.exists(analysis_path)==False:
              os.mkdir(analysis_path)
        with open(analysis_path+str(lower)+'_'+str(upper)+'_xy_peaks.txt', 'w') as f:
            f.write('peak\tx\ty\th5\tframe\n')
            for i in range(0,len(filtered_list)):
                f.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(str(filtered_list[i]),str(x_list[i]),str(y_list[i]),str(h5_list[i]),str(frame_list[i])))
        print('saved x and y peaks to ', analysis_path+str(lower)+'_'+str(upper))

