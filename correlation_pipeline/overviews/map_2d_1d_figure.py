
import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct




def process(init_path,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
	rwell = []
	
	#full data
	reduced_corr = False
	fdl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	fwell = fdl.load_radial_peak_position(init_path)
	fcorr = fdl.load_correlation_data(init_path,qslice,width,angle_blur)
	full_2D_data,full_1D_data = fdl.load_saxs_data(init_path)


	#reduced  data
	reduced_corr = True
	rdl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	for i in fwell:
		rwell_data = np.where((i >=lower)and(i<=upper),i,0)
		rwell.append(rwell_data)
	rcorr = rdl.load_correlation_data(init_path,qslice,width,angle_blur)
	red_2D_data,red_1D_data = rdl.load_saxs_data(init_path)

	plt.figure(figsize = (6,6))
	plt.plot(full_1D_data[:,0],full_1D_data[:,1], label ='full',color = 'black')
	plt.plot(red_1D_data[:,0],red_1D_data[:,1], label = 'filtered '+str(lower)+" "+str(upper),color = 'green')
	plt.legend()
	plt.xlabel("q (nm${-1}$)")
	plt.xlim(1,4)
	plt.ylabel("Intensity (A.U)")	
#plt.show()
	
	fig,ax = plt.subplots(2,2)#figsize = (6,6)
	a = ax[0,0].imshow(pd.rad_pos_plot(fwell),origin = 'lower',aspect = aspect, clim = [1.3,1.7])
	#plt.colorbar(a,ax = ax[0,0])
	ax[0,0].set_title('full')
	b = ax[0,1].imshow(pd.rad_pos_plot(rwell),vmin = 1.3, vmax = 1.7,origin = 'lower',aspect = aspect)#, clim = [1.3,1.7])
	#plt.colorbar(b,ax = ax[0,1])
	ax[0,1].set_title('filtered '+str(lower)+" "+str(upper))
	#ax[0,2].plot(np.arange(0,360,2),fcorr, label = 'full')
	#ax[0,2].plot(np.arange(0,360,2),rcorr, label =str(lower)+" "+str(upper)+ ' filtered')
	#ax[0,2].legend()
	ax[1,0].imshow(full_2D_data,clim = [0,2000])
	ax[1,0].set_title('full')
	ax[1,1].imshow(red_2D_data,clim = [0,2000])
	ax[1,1].set_title('filtered '+str(lower)+" "+str(upper))
	#ax[1,2].plot(full_1D_data[:,0],full_1D_data[:,1], label ='full')
	#ax[1,2].plot(red_1D_data[:,0],red_1D_data[:,1], label = 'filtered '+str(lower)+" "+str(upper))
	#ax[1,2].legend()
	#plt.suptitle("run "+str(run)+", "+str(temp)+chr(176)+' rad peak pos ',fontsize = 20)
	plt.show()
	





###Config stuf from correlation toolkit
maia_start = 138009
group = '75MO_W_P4_2H'
run = [383]#, 385, 387]#,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
temp = [35]#,48.3,55.9]#, 37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = '_' #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [35]#,33,34]#,35,33,33]
angle_blur = 0
width = 0
lower = [0.25]#,1.38,1.4]
upper = [2]#1.5,1.53]
analysis = 'radial_peak_position.npy'

#Script specific
aspect = 125/250

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

for qslice,lower,upper,run,temp in zip(qslice,lower,upper,run,temp):
	tag,maia_num = fl.file_finder(group,run)
	qslice = int(qslice)
	pd = ct.plot_data(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur,init_path)
	process(init_path,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

