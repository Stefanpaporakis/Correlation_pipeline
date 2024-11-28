import numpy as np
import glob
import h5py
import hdf5plugin
import matplotlib.pyplot as plt
import os
import pathlib
import correlation_toolkit as ct
from pyFAI.azimuthalIntegrator import AzimuthalIntegrator
	
def frm_integration(frame, unit="q_nm^-1", npt=2250):
	ai = AzimuthalIntegrator()
	ai.setFit2D(directDist=0.64/1000,
				centerX=517.0902,
				centerY=543.7068,
				pixelX=75e-6,
				pixelY=75e-6)
	ai.wavelength = 0.67018e-10
	integrated_profile = ai.integrate1d(data=frame, npt=npt, unit=unit)
	return np.transpose(np.array(integrated_profile))
		
def process(reduced_1D_2D,raw_path,dlist,all_data):
	for k, h5 in enumerate(sorted(glob.glob(raw_path+"*_data*.h5"))):
		with h5py.File(h5) as f:
			print('looking at ', h5)
			d = np.array(f['entry/data/data'])
			d[d>4.29e9] = 0
			full = d
			print('h5 shape is',d.shape)
			if reduced_1D_2D==True:
				framemask = dlist[dlist[:,0]==k+1,1].astype(np.int)-1
				nd = d.shape[0]
				d = d[framemask[framemask<nd],:,:]
				print("reduced h5 to ", d.shape)
			if all_data is None:
				all_data = np.sum(d,axis = 0)
				full_image = np.sum(full,axis = 0)
			else:
				all_data +=np.sum(d,axis = 0)
				full_image += np.sum(full,axis = 0)
	return full_image, all_data



group = '60MO_EtAF_9H'
run =[150,158,165,172]#[392,393] #[381,383,384,385,386,387,388,389,390,391,392,393]
temp =[3] #[30,35,37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7]
lower = [1.26,1.33,1.4,1.53]#[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
upper = [1.38,1.44,1.54,1.68]#[2,2,2,2,2,2,2,2,2,2,2,2]
maia_num = []
tag = []
chunksize = 1
reduced_corr = True #reduced or full correlation data, 
init_path = f"/data/xfm/20027/analysis/"
qslice = [32,35,33,34,34,34,34,35,35,37,37,37]
angle_blur = 0
width = 0
analysis = '_'


#Set to True for reduced data, 
#need to have run filter_between_lower_pper.py first for True,
#Can run straight away for False
reduced_1D_2D = True



if int(len(run)) == int(len(lower)) ==  int(len(upper)):
	pass
else:
	print('cant run script, check you groups')
	print('run length ',len(run))
	print('lower length ', len(lower))
	print('upper length ', len(upper))
	exit()

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)


if reduced_1D_2D==True:
	for run,lower,upper in zip(run,lower,upper):
		all_data = None
		tag,maia_num = fl.file_finder(group,run)
		dlist = np.loadtxt(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/mapping_stuff/radpeakpos/{str(lower)}_{str(upper)}_xy_peaks.txt", skiprows=1, delimiter = '	')[:,3:]
		raw_path = f"/data/xfm/20027/raw/eiger/{group}/{tag}/"
		outpath = f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/radpeakpos/{str(lower)}_{str(upper)}/"
		full_image, all_data = process(reduced_1D_2D,raw_path,dlist,all_data)
		plt.imshow(full_image)
		plt.savefig(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'summed_diffraction.png')
		plt.close()
		fig,ax = plt.subplots(1,2,figsize = (10,5))
		a = ax[0].imshow(full_image)
		ax[0].set_title('full diffraction image')
		b = ax[1].imshow(all_data)
		ax[1].set_title('reduced ')# + str(lower) + ', '+str(upper) = ' difraction image')
		image = plt.imshow(all_data)
		if os.path.exists(outpath)==False:
			  os.mkdir(outpath)
		np.save(outpath+'reduced_diffraction.npy',all_data)
		saxs1d = frm_integration(all_data)
		np.save(outpath+'reduced_1d_sum.npy',saxs1d)
		fsaxs1d = frm_integration(full_image)
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'summed_diffraction.npy',full_image)
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'1d_sum.npy',fsaxs1d)
		plt.savefig(outpath+'reduced_image.png')
		plt.close()
		
		
if reduced_1D_2D == False:
	for run in run:
		dlist = []
		all_data = None
		tag,maia_num = fl.file_finder(group,run)
		raw_path = f"/data/xfm/20027/raw/eiger/{group}/{tag}/"
		full_image, all_data = process(reduced_1D_2D,raw_path,dlist,all_data)
		plt.imshow(full_image)
		plt.savefig(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'summed_diffraction.png')
		plt.close()
		fsaxs1d = frm_integration(full_image)
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'summed_diffraction.npy',full_image)
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/"+'1d_sum.npy',fsaxs1d)

