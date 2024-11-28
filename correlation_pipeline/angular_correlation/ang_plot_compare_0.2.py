from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import matplotlib.cm as cm
import correlation_toolkit as ct
import matplotlib.pyplot as plt

def ia3d_model():
	a = []
	b= []
	vecl = []
	vec2l = []
	anglel = []
	red_angle = []
	ang_occur = []
	alpha = 0.0
	a.append([2-2*alpha,1,1])
	a.append([1-alpha,2,1])
	a.append([1-alpha,1,2])
	a.append([2,1,1])
	a.append([-2,1,1])
	a.append([2,-1,1])
	
	for vec in a:
		for m in [-1,1]:
			for n in [-1,1]:
				for p in [-1,1]:
					b.append(np.array([vec[0]*m, vec[1]*n, vec[2]*p]))
	for vec in a:
		for m in [-1,1]:
			b.append(np.array([vec[0]*m, vec[1]*m, vec[2]*m]))

	for vec in b:
		for vec2 in b:
			diff = vec2-vec
			diffnorm = np.sqrt(np.sum(diff**2))
			angle = 2*np.arcsin(diffnorm/(2*np.sqrt(6)))*180.0/np.pi
			
			vecl.append(str(vec))
			vec2l.append(str(vec2))
			anglel.append(int(angle))
	#print(vecl)
	#print(vec2l)
	#print(anglel)
	occurences = {}
	for i in anglel:
		if i in occurences:
			occurences[i]+=1
		else:
			occurences[i] = 1
			red_angle.append(i)
	for i in red_angle:
		ang_occur.append(occurences[i])
	return red_angle,ang_occur

def twinning():
	angles = [180,112,123,127,96,160,136,102,43,67,77,19,52]
	return angles



##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
group = '60MO_EtAF_9H'
#group = '75MO_W_P4_2H'
run = [150,158,165,172]
#run = [381]
temp = [30,32.5,35,37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = True #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice =[31,33,35,37] #MO PILs
#qslice = [32] #MO water
angle_blur =1
width = 1
lower = [1.26,1.33,1.4,1.53]
upper = [1.38,1.44,1.54,1.68]
analysis = 'radial_peak_position.npy'

#script specific params
strt=0
nruns=4

model_ia3d=True
twin = False
c_vals = np.linspace(0,0.3,len(run))
colors = cm.PuOr(c_vals)[::-1]
plist = []
dlistC = []
labels = run

fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
model_angle,occurance = ia3d_model()
twin_peaks = twinning()

if reduced_corr == False:
	for run,j in zip(run,qslice):
		tag = fl.file_finder(group,run)[0]
		maia_num = fl.file_finder(group,run)[1]
		qslice = int(j)
		dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		#load corr data#
		corr = dl.load_correlation_data(init_path,qslice,width,angle_blur)
		dlistC.append(corr)
		
if reduced_corr == True:
	for run,j,k,l,m in zip(run,qslice,temp,lower,upper):
		tag = fl.file_finder(group,run)[0]
		maia_num = fl.file_finder(group,run)[1]
		qslice = int(j)
		lower = l
		upper = m
		#print(tag,qslice,l,m)
		dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		#load corr data#
		corr = dl.load_correlation_data(init_path,qslice,width,angle_blur)
		dlistC.append(corr)

		
for i, data in enumerate(dlistC[strt:strt+nruns]):
	p, = plt.plot(np.arange(0,360,2),data)#,color=colors[i])
	plist.append(p)

if model_ia3d ==True:
	for i,j in zip(model_angle,occurance):
		x =plt.axvline(i, linestyle = '--', color='red',label = 'model')
	#plist.append(x)
if twin==True:
	for i in twin_peaks:
		y = plt.axvline(i,linestyle = '--',color = 'green', label = 'twinning')
	#plist.append(y)
	    	    #print('model angle '+str(i)+' occured '+str(j)+' times')
plt.ylabel("Correlation intensity (arb units)", fontsize=10)
plt.xlabel(r'theta (degrees)',fontsize=10)

plt.yscale('log')
plt.legend((150,158,165,172),loc = 'upper right')
plt.draw()
plt.show()    
