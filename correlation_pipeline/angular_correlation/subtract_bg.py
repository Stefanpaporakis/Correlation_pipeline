import numpy as np
import matplotlib.pyplot as plt



group = '75MO_W_P4_2H'
tag = '138392_383'
an = 'radpeakpos'
red = '1.35_1.45'
reduced = True




if reduced == True:
	aset = np.load(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/{an}/{red}/reduced{tag}_nstart400_a_correlation_sum.npy")
	bset = np.load(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/{an}/{red}/reduced{tag}_nstart400_b_correlation_sum.npy")

else:
	aset = np.load(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/{tag}_nstart400_a_correlation_sum.npy")
	bset = np.load(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/{tag}_nstart400_b_correlation_sum.npy")

full = aset+bset
bggroup = 'calibration'
bgtag = '138017_8'
bg = np.load(f"/data/xfm/20027/analysis/eiger/{bggroup}/{bgtag}/corr/{bgtag}_a_correlation_sum.npy")
bg =bg+ (np.load(f"/data/xfm/20027/analysis/eiger/{bggroup}/{bgtag}/corr/{bgtag}_b_correlation_sum.npy"))


q_q = True
if q_q == True:
	for i, j in enumerate(np.arange(full.shape[0])):
		norm = np.sum(full[i,j])/np.sum(bg[i,j])
		full[i,j,:] = full[i,j,:]-bg[i,j,:]*norm

	if reduced==True:
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/{an}/{red}/reduced_bgsub_{tag}_nstart400_correlation_sum.npy",full)
	else:
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/bgsub_{tag}_nstart400_correlation_sum.npy",full)

q_q = False

if q_q == False:
	for i in np.arange(full.shape[0]):
			for j in np.arange(full.shape[0]):
				norm = np.sum(full[i,j])/np.sum(bg[i,j])
				full[i,j,:] = full[i,j,:]-bg[i,j,:]*norm
	if reduced ==True:
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/{an}/{red}/reduced_3D_bgsub_{tag}_nstart400_correlation_sum.npy",full)
	else:
		np.save(f"/data/xfm/20027/analysis/eiger/{group}/{tag}/corr_nps1/3D_bgsub_{tag}_nstart400_correlation_sum.npy",full)

