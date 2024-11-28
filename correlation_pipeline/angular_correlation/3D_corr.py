import numpy as np
import matplotlib.pyplot as plt
import os
import array
import sys
import correlation_toolkit as ct

def prepare(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
	fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	tag,maia_num = fl.file_finder(group,run)
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	return dl,tag,maia_num

def corr_3D(qq_plot,init_path,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
	dl ,tag,maia_num= prepare(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	data = dl.load_3D_correlation_data(init_path,qslice,width,angle_blur)

	sc, scl = 1, 1
	rmax =  128 #128
	rline = 35 #this is where you set the line to extract and plot separately
	irline = int(data.shape[0]*rline/rmax)

	disp = np.zeros( (data.shape[0], data.shape[2]) )
	dline = np.zeros( data.shape[2] )
	tmp = data*0.
	ith = 1 # this crops from the left
	thmin = (ith/360)*data.shape[2]
	for i in np.arange(data.shape[0]):
		for j in np.arange(data.shape[1]):
			tmp[i,j,:] = data[i,j,:] - 1*np.average(data[i,j,ith:-ith])
	pw = 0
	for i in np.arange(data.shape[0]):
		disp[i,:] = tmp[i,i,:]*(i*i)**pw
		dline[:] = np.sum(np.sum(tmp[irline-width:irline+width+1,irline-width:irline+width+1,:]*(i*i)**pw,0),0)
	ir1 = disp.shape[0]-0
	rmaxnew = rmax*(ir1/data.shape[0])
	ir = 0
	rminnew = rmax*(ir/data.shape[0])
	plt.figure()
	plt.imshow(disp[ir:ir1,ith:disp.shape[1]//1], origin='lower', extent=[thmin,180,rminnew,rmaxnew], aspect=2)
	#plt.clim([np.min(disp[ir:ir1,ith:disp.shape[1]//2])*scl,np.max(disp[ir:ir1,ith:disp.shape[1]//2])*sc])
	plt.clim(0,1)
	plt.title(tag)
	if qq_plot==True:
		plt.show(block=False)
	else:
		plt.show()

def qq_slice(model,flag,init_path,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur):
	if corr_3d_plot==True:
		print("q-q' slice where?")
		qslice = int(input())
	dl ,tag,maia_num= prepare(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	corr = dl.load_correlation_data(init_path,qslice,width,angle_blur)
	positions = models(model)
	plt.figure()
	for i in positions:
		plt.axvline(i,linestyle = '--',color = 'red')
	
	plt.plot(np.arange(0,360,2),corr)
	plt.title(qslice)
	if corr_3d_plot==True:
		plt.pause(0.001)
	else:
		plt.show()
		exit()

def models(model):
	positions = []
	ia3d = [33,48,60,80,70,99,109,131,120,146,180]
	hexagonal = [60,120]
	if model=='ia3d':
		for i in ia3d:
			positions.append(i)
	if model =='hex':
		for i in hexagonal:
			positions.append(i)
	return positions		


##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
group = '60MO_EtAF_9H'
run = 172
lower = 1.53
upper = 1.68
temp = ' '
maia_num = ' '
tag = ' '
chunksize = 1
reduced_corr = True #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = 32
angle_blur =1
width = 2
analysis = 'radial_peak_position.npy'
corr_3d_plot=True
qq_plot = True
model = 'ia3d'

if corr_3d_plot==True:
	plot_3D = corr_3D(qq_plot,init_path,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

if qq_plot==True:
	flag=True
	while flag==True:
		plot_qq_slice = qq_slice(model,flag,init_path,maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		print('try again?[y/n]')
		again = str(input())
		if again!='y':
			exit()
