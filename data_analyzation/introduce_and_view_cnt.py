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
cnt = 0
sum1 = sum2 = 0
xx = []
yy = []
my_cnt = []
my_sum = []
for i in range(0, 300):
    my_cnt.append(0)
    my_sum.append(0)
for x in load_dict:
    my_cnt[len(load_dict[x]["creator_introduce"])] += 1
    my_sum[len(load_dict[x]["creator_introduce"])] += get(load_dict[x]["view_cnt"])
    if len(load_dict[x]["creator_introduce"]) > 10:
        cnt += 1
        sum1 += get(load_dict[x]["view_cnt"])
    else:
        sum2 += get(load_dict[x]["view_cnt"])
for i in range(0, 300):
    if my_cnt[i] != 0:
        xx.append(i)
        yy.append(my_sum[i] / my_cnt[i])
print("个人简介长度大于10的视频数: " + str(cnt))
print("个人简介长度小于等于10的视频数: " + str(len(load_dict) - cnt))
print("个人简介长度大于10的up主的平均单个视频播放量: " + str(sum1 / cnt))
print("个人简介长度小于等于10的up主的平均单个视频播放量: " + str(sum2 / (len(load_dict) - cnt)))
print("相差倍数: " + str((sum1 / cnt) / (sum2 / (len(load_dict) - cnt))))

z = np.polyfit(xx, yy, 1)
p = np.poly1d(z)
print(p) 
yvals = p(xx)
plot1 = plt.plot(xx, yy, '*')
plot2 = plt.plot(xx, yvals, 'r')
plt.show()