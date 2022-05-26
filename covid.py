import pandas as pd
import numpy as np

data = pd.read_excel("data/shuju1.xlsx", header=None)


data = np.array(data)


# print(data)
# exit(0)


e12 = 300
e3 = 150
I = 1050
Q = 330240

t = len(data)
# print(t)

x = range(0, t)

rmin = 0.05
rmax = 4
pmin = 0.05
pmax = 0.6


n = 10

rt = (rmax - rmin) / n
pt = (pmax - pmin) / n


rpchu = np.zeros((n  +  1, 2))

echu = np.zeros((t + 1, 4 * ((n + 1)**2))) #  #储存r，p变化时计算得到的每一天的e12，e3，I，Q
mchu = np.zeros((t + 1,(n + 1)**2)) # %储存误差的和
m1chu = np.zeros((t + 1,(n + 1)**2)) # %储存PI和真实值的误差
m2chu = np.zeros((t + 1,(n + 1)**2)) # %储存Q和真实值的误差
qiuhe = 0



for i in range(0, n + 1):
    rpchu[i,:] = rmin + rt*i,pmin + pt*i  # %构造r和p的矩阵

# print(rpchu)


for i in range(1, t + 1): # %t*4(n + 1)**2
    for j in range(n + 1): #关于r循环
        for k in range(n + 1): #关于p循环

            echu[0,4*(n + 1)*j + 4*k]= e12
            echu[0,4*(n + 1)*j + 4*k + 1]= e3
            echu[0,4*(n + 1)*j + 4*k + 2]= I
            echu[0,4*(n + 1)*j + 4*k + 3]= Q
            
            # print(echu.shape)
            # print(echu)


            qiuhe = np.sum(echu[0:i,:],0) #第1到t天求得的四种值分别求和           

            echu[i,4*(n + 1) * j + 4 * k] = 0.125 * rpchu[j,0] * (echu[i-1,4 * (n + 1) * j + 4 * k + 1] + echu[i - 1, 4 * (n + 1) * j + 4 * k + 2]) + 0.5 * echu[i - 1, 4 * (n + 1) * j + 4 * k]
            echu[i,4*(n + 1) * j + 4 * k + 1] = 0.5 * echu[i - 1, 4 * (n + 1) * j + 4 * k]
            echu[i,4*(n + 1) * j + 4 * k + 2] = echu[i - 1, 4 * (n + 1) * j + 4 * k + 1] + (6/7) * echu[i - 1, 4 * (n + 1) * j + 4 * k + 2] - 0.001 * echu[i-1, 4 * (n + 1) * j + 4 * k + 2] - rpchu[k, 1] * echu[i - 1, 4 * (n + 1) * j + 4 * k + 2]
            echu[i,4*(n + 1) * j + 4 * k + 3] = rpchu[k,1] * qiuhe[4*(n + 1)*j + 4*k + 2] + Q #模型求得的Q值

            # print(echu[:4, :4])
            # exit(0)

            m1chu[i, j * (n + 1) + k] = abs(rpchu[k, 1] * echu[i, 4*(n + 1)*j + 4*k + 2] - data[i-1,0]) #r,p不同时的所有误差M1(新增)
            m2chu[i, j * (n + 1) + k] = abs(echu[i, 4 * (n + 1) * j + 4 * k + 3] - data[i - 1, 1]) #r,p不同时的所有误差M2(总和)
            mchu[i, j * (n + 1) + k] = m1chu[i,j * (n + 1) + k] + m2chu[i,j * (n + 1) + k] #M1，M2之和

            # print(m1chu)
            # print(m2chu)
            # print(mchu)

            # exit(0)


agg = np.zeros((t,(n + 1)**2)) #构造存放误差的矩阵
for i in range(0, t):
    agg[i,:]=mchu[i + 1,:] #去掉第一行，剩下t天所有的值


tt = np.zeros((1,t), dtype=np.uint16) #存放大矩阵中rp的值，用于确定位置
tt1 = np.zeros((1,t), dtype=np.uint16) #存放每一天的最小值（可以不用）
tt2 = np.zeros((2,t)) #第一行为最小值所取的r，第二行为最小值所取的p
tt3 = np.zeros((2,t), dtype=np.uint16) #rp位置(第几个r,第几个p)
tt4 = np.zeros((2,t)) #第一行为pI的最小值，第二行为总和的最小值

for i in range(0, t):
    d=1000000

    for j in range(0, (n + 1)**2):
        
        if agg[i,j] < d:
            d = agg[i,j] #寻找每一行的最小值，并记录rp的位置
            tt[0,i] = j



for i in range(0, t):
    tt3[0, i] = np.ceil( (tt[0,i] + 1) / (n + 1)) #第几个r满足要求（向上取整）
    tt3[1, i] = (tt[0,i] + 1) % (n + 1) #第几个p满足要求（取余）
    if (tt[0,i] + 1) % (n + 1) == 0: #此时p取最后个值
        tt3[1,i] = (n + 1)


    # print(tt3)
    # exit(0)
    
    tt2[0, i] = (tt3[0, i] - 1) * rt + rmin #满足要求的r值
    tt2[1, i] = (tt3[1, i] - 1) * pt + pmin #满足要求的p值


    b = 4 * (n + 1) * (tt3[0,i] - 1) + 4 * (tt3[1,i] - 1) + 2
    # print(b)
    
    a = echu[i + 1, b] #满足要求的pI值

    # print(a)
    tt4[0, i] = tt2[1, i] * a
    tt4[1, i] = np.sum(tt4[0,0:i + 1]) + Q #模型求得的Q



print(tt2)


import matplotlib.pyplot as plt


plt.figure(0)

plt.plot(x, tt4[0, :])
plt.plot(x, data[:, 0])
plt.show()
#  #disp(tt)
# disp(tt2) #输出满足要求的r，p
# xlswrite('rp.xlsx',tt2)



# figure(1)
# plot(x,tt4(1,:),'r') #计算的pI值图像
# hold on
# plot(x,num(:,1)','b')
# legend('模拟的PI值','真实值')


# figure(2)
# plot(x,tt4(2,:),'r') #计算的Q值图像
# hold on
# plot(x,num(:,2)','b')
# legend('模拟的Q值','真实Q')



# figure(3)
# plot(x,tt2(1,:),'r')
# legend('Rt值')



# figure(4)
# plot(x,tt2(2,:),'b')
# legend('p值')
# end