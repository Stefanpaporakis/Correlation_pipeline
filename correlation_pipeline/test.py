import numpy as np
import matplotlib.pyplot as plt

sample = "CTAB"
maia_num = "86409_202"

path = f"/data/xfm/17635/analysis/eiger/SAXS/{sample}/{maia_num}/"
tag = f"{maia_num}_sum_reduced_s"

data  = np.load(path+tag+".npy")

plt.plot(data[:,0],data[:,1])
plt.show()

