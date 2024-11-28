import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct
import sys

def ifs(lower,upper,run):
	if len(lower)!=len(upper):
		print('params arent equal')
		print('upper: ',len(upper))
		print('lower: ', len(lower))
		print('run: ',len(run))
		sys.exit()
	if len(lower)!=len(run):
		print('params arent equal')
		print('upper: ',len(upper))
		print('lower: ', len(lower))
		print('run: ',len(run))
		sys.exit()
	if len(run)!=len(upper):
		print('params arent equal')
		print('upper: ',len(upper))
		print('lower: ', len(lower))
		print('run: ',len(run))
		sys.exit()


###Config stuf from correlation toolkit
maia_start = 138009
group = '75MO_W_P4_2H'
run =[381,381,383,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
temp = [30]#,64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [35]#,33,34]#,35,33,33]
angle_blur = 0
width = 0

#For ia3d:
lower = [1.31,1.31,1.35,1.36,1.38,1.37,1.4,1.39,1.41,1.4,1.43,1.47,1.51]#,1.38,1.4]
upper = [1.43,1.43,1.45,1.48,1.5,1.52,1.53,1.52,1.51,1.56,1.58,1.66,1.64]

#For non-ia3d:
#lower =[0.45,0.43,0.41,0.4] #[0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]#,1.38,1.4]
#upper = [0.9,0.92,0.99,1.09]#[2,2,2,2,2,2,2,2,2,2,2,2,2]

analysis = 'radial_peak_position.npy'
seperation = 0


fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
ifs(lower,upper,run)


for lower,upper,run,temp in zip(lower,upper,run,temp):
	tag,maia_num = fl.file_finder(group,run)
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	_,data = dl.load_saxs_data(init_path)
	plt.plot(data[:,0],data[:,1]-seperation, label = temp)
	seperation = seperation+0

plt.legend()
plt.xlim(1,4)
plt.xlabel("q (nm$^{-1}$)")
plt.ylabel("Intensity (A.U)")
#plt.yscale('log')
plt.show()




