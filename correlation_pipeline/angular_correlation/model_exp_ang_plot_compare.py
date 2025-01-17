
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
	print(vecl)
	print(vec2l)
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

			
					
	
	
	
	



##Config stuff (required for every script that uses the toolkit)##
maia_start = 138009
group = '75MO_W_P4_2H'
run = [381,383,384,385,386,387,388,389,390,391,392,393]#,384,385,386]
temp = [30,35,37.3, 48.3, 52.3, 55.9, 59.2, 62.1, 64.7, 67, 68.9, 74.5]#,79.6]
maia_num = []
tag = []
chunksize = 1
reduced_corr = False #reduced or full correlation data
init_path = f"/data/xfm/20027/analysis/"
qslice = [32,35,33,34,34,34,34,35,35,37,37,37]
angle_blur = 0
width = 0
lower = [1.31,1.35,1.36,1.38,1.37,1.4,1.39,1.41,1.4,1.43,1.47,1.51]
upper = [1.43,1.45,1.48,1.5,1.52,1.53,1.52,1.51,1.56,1.58,1.66,1.64]
analysis = 'radial_peak_position.npy'

#script specific params
strt=0
nruns=1
c_vals = np.linspace(0,0.3,len(run))
colors = cm.PuOr(c_vals)[::-1]
plist = []
dlistC = []
labels = run


fl = ct.path_maker(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
model_angle,occurance = ia3d_model()


if reduced_corr == False:
	for run,j in zip(run,qslice):
		tag = fl.file_finder(group,run)[0]
		maia_num = fl.file_finder(group,run)[1]
		qslice = int(j)
		#print(tag)
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
		print(tag,qslice,l,m)
		dl = ct.data_loader(maia_num,group,tag, analysis,chunksize,reduced_corr,lower,upper,qslice,width,angle_blur)
		#load corr data#
		corr = dl.load_correlation_data(init_path,qslice,width,angle_blur)
		dlistC.append(corr)
	
	
for i, data in enumerate(dlistC[strt:strt+nruns]):
    p, = plt.plot(np.arange(0,360,2),data,color=colors[i])
    plist.append(p)
for i,j in zip(model_angle,occurance):
	plt.axvline(i, linestyle = '--')
	print('model angle '+str(i)+' occured '+str(j)+' times')


plt.ylabel("Correlation intensity (arb units)", fontsize=10)
plt.xlabel(r'theta (degrees)',fontsize=10)
plt.legend(plist, labels[strt:strt+nruns], loc = 'upper right') 
plt.draw()
plt.show()    
