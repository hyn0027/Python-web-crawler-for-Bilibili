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
creators = {}
num = {}
for x in load_dict:
    if load_dict[x]["uid"] in creators:
        creators[load_dict[x]["uid"]] += 1
        num[load_dict[x]["uid"]] += get(load_dict[x]["view_cnt"])
    else:
        creators[load_dict[x]["uid"]] = 1
        num[load_dict[x]["uid"]] = get(load_dict[x]["view_cnt"])
cnt1 = 0
cnt2 = 0
sum1 = 0
sum2 = 0
for x in creators:
    if creators[x] > 1:
        cnt1 += creators[x];
        sum1 += num[x]
    else:
        cnt2 += 1
        sum2 += num[x]

print("所有up主数: " + str(len(creators)))
print("连续投稿up主数: "+ str(cnt1))
print("连续投稿up主占比: " + str(cnt1/len(creators)))
print("不连续投稿up主的平均单个视频播放量: " + str(sum2/(len(creators) - cnt1)))
print("连续投稿up主的平均单个视频播放量: " + str(sum1/cnt1))
print("平均单个视频播放量之比： " + str( (sum1/cnt1) / (sum2 / (len(creators) - cnt1) )))

my_tim_cnt = []
my_tim_sum = []

for  i in range(0, 100):
    my_tim_cnt.append(0)
    my_tim_sum.append(0)

for x in creators:
    my_tim_cnt[creators[x]] += creators[x]
    my_tim_sum[creators[x]] += num[x]

x = []
y = []

for i in range(0, 100):
    if my_tim_cnt[i] != 0:
        x.append(i)
        y.append(my_tim_sum[i] / my_tim_cnt[i])

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
print(p) 
yvals = p(x)
plot1 = plt.plot(x, y, '*')
plot2 = plt.plot(x, yvals, 'r')
plt.show()