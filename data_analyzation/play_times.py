import matplotlib.pyplot as plt
import numpy as np
import json

def get(l):
    le = len(l)
    if l[le - 1] == "万":
        l = l[:-1]
        l = float(l)
        l = l * 10000
        return l
    return int(l)
    

with open("data.json",'r', encoding = 'utf-8') as load_f:
    load_dict = json.load(load_f)
list = []
sum= 0
for x in load_dict:
    list.append(get(load_dict[x]["view_cnt"]))
    sum += get(load_dict[x]["view_cnt"])
list.sort()
ypoints = []
xpoints = []
all = 0
for i in range(0, len(list)):
    xpoints.append(i / len(list))
    ypoints.append(list[i])
    all += list[i]
plt.plot(xpoints, ypoints)
plt.show()

sum = 0
for i in range(int(len(list) * 0.892), len(list)):
    sum += list[i]
print("前10.8%的up主拥有" + str(round(sum * 100 / all, 3)) + "%的播放量")