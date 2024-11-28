import numpy as np
import matplotlib.pyplot as plt
import correlation_toolkit as ct




###Config stuf from correlation toolkit
maia_start = 138009
group = '75MO_W_P4_2H'#'75MO_W_P4_2H'
run = [381,385,388,392]
temp = [1,2,3,4]
maia_num = []
tag = []
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [35]#,33,34]#,35,33,33]
angle_blur = 0
width = 0
analysis = '_'
lower = '_'
upper = '_'

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)

image = []
for run,temp in zip(run,temp):
	tag,maia_num = fl.file_finder(group,run)
	dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
	full_2D_data = np.load(dl.load_saxs_path(init_path)+'summed_diffraction.npy')
	image.append(full_2D_data)

low,up = 330,700
ylow,yup = 380,700


fig,ax = plt.subplots(1,4)
ax[0].imshow(image[0])
ax[0].set_xlim(low,up)
ax[0].set_ylim(ylow,yup)
ax[0].axis("off")
ax[1].imshow(image[1])
ax[1].set_xlim(low,up)
ax[1].set_ylim(ylow,yup)
ax[1].axis("off")
ax[2].imshow(image[2])
ax[2].set_xlim(low,up)
ax[2].set_ylim(ylow,yup)
ax[2].axis("off")
ax[3].imshow(image[3])
ax[3].set_xlim(low,up)
ax[3].set_ylim(ylow,yup)
ax[3].axis("off")
plt.show()
