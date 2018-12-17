import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
import re

def opendata(path, tag):
    stepmap = {}
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if "stepstocompletion" in name:
                p = os.path.join(root, name)
                parts = root.split('/')
                str_regex = re.compile(tag + '[0-9]+')
                num_regex = re.compile('[0-9]+')
                str_str_matc = str_regex.match(parts[2])
                if str_str_matc is not None:
                    num = int(num_regex.findall(str_str_matc.group())[0])
                    with open(p, 'r') as f:
                        l = int(f.read())
                        stepmap[num] = l

    return stepmap



def map2array(stepmap):
    res = []
    for key, value in stepmap.items():
        res.append(np.array([int(key), int(value)]))

    npres = np.array(res)
    result = np.sort(npres.view('i8,i8'), order=['f0'], axis=0).view(np.int)

    return result


def normalize_incomplete_data(a):
    for x in range(0, len(a)):
        print(a[x])
        a[x][0] = x

    return a

def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]

os.chdir('./newrun-range')
highrangedata = opendata("./logs", "highrange")
lowrangedata = opendata("./logs/", "lowrange")

highrangearray = map2array(highrangedata)
lowrangearray = map2array(lowrangedata)

highrangekeys = highrangearray[:,0]
highrangevals = highrangearray[:,1]

lowrangekeys = lowrangearray[:,0]
lowrangevals = lowrangearray[:,1]

lowrangevals_nooutliers = reject_outliers(lowrangevals, 30)
lowrangevals_x = np.arange(len(lowrangevals_nooutliers))

highrangevals_nooutliers = reject_outliers(highrangevals, 30)
highrangevals_x = np.arange(len(highrangevals_nooutliers))
plt.plot(lowrangevals_x, lowrangevals_nooutliers, label="Lowrange Run")
plt.plot(highrangevals_x, highrangevals_nooutliers,  label="Highrange Run")
plt.legend(["Range = 4", "Range = 8"])
plt.xlabel("simulation run")
plt.ylabel("timesteps")
plt.show()
os.chdir("../")
