import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct

 

 



maia_start = 138009
group = '75MO_W_P4_2H'
run = 383
temp = []
maia_num = []
tag = []
chunksize = 1
reduced_corr =True
init_path = f'/data/xfm/20027/analysis/'
qslice = '_'
angle_blur = '_'
width = '_'
lower = 1.48
upper= 1.66
analysis = 'radial_peak_position.npy'


fl = ct.path_maker(maia_num,group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
tag,maia_num = fl.file_finder(group,run)
full = np.load(f'{init_path}/eiger/{group}/{tag}/1d_sum.npy')
rdl = ct.data_loader(maia_num,group,tag,analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
red = np.load(f'{rdl.load_saxs_path(init_path)}'+'reduced_1d_sum.npy')


plt.plot(full[:,0],full[:,1], label = 'full')
plt.plot(red[:,0],red[:,1], label = 'ignoring ia3d first raial peak position')
plt.axvline(1.51, color = 'r', linestyle = '--', label = 'shouldering peak location')
plt.legend()
plt.show()

 
