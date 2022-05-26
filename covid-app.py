from flask import Flask, render_template, request

import pandas as pd
import numpy as np

app = Flask(__name__)


@app.route('/model_api/', methods=['GET', 'POST'])
def api1():

    requestData = eval(request.data)

    province = requestData["province"]
    day_to_predict = requestData["day_to_predict"]

    province_file_dict = {
        "北京": "data/beijing-true.xlsx",
        "香港": "data/hongkong-true.xlsx",
        "深圳": "data/shenzhen.xlsx",
        "上海": "data/shanghai.xlsx",
    }

    data = pd.read_excel(province_file_dict[province], header=None)


    data = np.array(data)

    print(data)

    e12 = requestData["e12"]
    e3 = requestData["e3"]
    I = requestData["I"]
    Q = requestData["Q"]
    

    t = len(data)
    # print(t)

    x = range(0, t)

    rmin = 0.05
    rmax = 4
    pmin = 0.05
    pmax = 0.8


    n = 20

    rt = (rmax - rmin) / n
    pt = (pmax - pmin) / n


    # day_to_predict = 30

    predict_t = t + day_to_predict # 预测天数

    rpchu = np.zeros((n  +  1, 2))

    echu = np.zeros((t + 1, 4 * ((n + 1)**2))) #  #储存r，p变化时计算得到的每一天的e12，e3，I，Q
    mchu = np.zeros((t + 1,(n + 1)**2)) # %储存误差的和
    m1chu = np.zeros((t + 1,(n + 1)**2)) # %储存PI和真实值的误差
    m2chu = np.zeros((t + 1,(n + 1)**2)) # %储存Q和真实值的误差
    qiuhe = 0



    for i in range(0, n + 1):
        rpchu[i,:] = rmin + rt*i,pmin + pt*i  # %构造r和p的矩阵




    sum_dict = {}


    for i in range(1, t + 1): # %t*4(n + 1)**2
        for j in range(n + 1): #关于r循环
            for k in range(n + 1): #关于p循环

                echu[0,4*(n + 1)*j + 4*k]= e12
                echu[0,4*(n + 1)*j + 4*k + 1]= e3
                echu[0,4*(n + 1)*j + 4*k + 2]= I
                echu[0,4*(n + 1)*j + 4*k + 3]= Q
                
                qiuhe = np.sum(echu[0:i,:],0) #第1到t天求得的四种值分别求和           

                sum_dict[i] = qiuhe

                echu[i,4*(n + 1) * j + 4 * k] = 0.125 * rpchu[j,0] * (echu[i-1,4 * (n + 1) * j + 4 * k + 1] + echu[i - 1, 4 * (n + 1) * j + 4 * k + 2]) + 0.5 * echu[i - 1, 4 * (n + 1) * j + 4 * k]
                echu[i,4*(n + 1) * j + 4 * k + 1] = 0.5 * echu[i - 1, 4 * (n + 1) * j + 4 * k]
                echu[i,4*(n + 1) * j + 4 * k + 2] = echu[i - 1, 4 * (n + 1) * j + 4 * k + 1] + (6/7) * echu[i - 1, 4 * (n + 1) * j + 4 * k + 2] - 0.001 * echu[i-1, 4 * (n + 1) * j + 4 * k + 2] - rpchu[k, 1] * echu[i - 1, 4 * (n + 1) * j + 4 * k + 2]
                echu[i,4*(n + 1) * j + 4 * k + 3] = rpchu[k,1] * qiuhe[4*(n + 1)*j + 4*k + 2] + Q #模型求得的Q值




                m1chu[i, j * (n + 1) + k] = abs(rpchu[k, 1] * echu[i, 4*(n + 1)*j + 4*k + 2] - data[i - 1,0 ]) #r,p不同时的所有误差M1(新增)
                m2chu[i, j * (n + 1) + k] = abs(echu[i, 4 * (n + 1) * j + 4 * k + 3] - data[i - 1, 1]) #r,p不同时的所有误差M2(总和)
                mchu[i, j * (n + 1) + k] = m1chu[i,j * (n + 1) + k] + m2chu[i,j * (n + 1) + k] #M1，M2之和



    agg = np.zeros((t,(n + 1)**2)) #构造存放误差的矩阵
    for i in range(0, t):
        agg[i,:]=mchu[i + 1,:] #去掉第一行，剩下t天所有的值


    tt = np.zeros((1,t), dtype=np.uint16) #存放大矩阵中rp的值，用于确定位置
    tt1 = np.zeros((1,t), dtype=np.uint16) #存放每一天的最小值（可以不用）
    tt2 = np.zeros((2,t)) #第一行为最小值所取的r，第二行为最小值所取的p # r和p所在的位置
    tt3 = np.zeros((2,t), dtype=np.uint16) #rp位置(第几个r,第几个p)
    tt4 = np.zeros((2,t)) #第一行为pI的最小值，第二行为总和的最小值

    for i in range(0, t):
        d=10000000

        for j in range(agg.shape[1]):
            
            if agg[i,j] < d:
                d = agg[i,j] #寻找每一行的最小值，并记录rp的位置
                tt[0,i] = j



    for i in range(0, t):
        tt3[0, i] = np.ceil( (tt[0,i] + 1) / (n + 1)) #第几个r满足要求（向上取整）
        tt3[1, i] = (tt[0,i] + 1) % (n + 1) #第几个p满足要求（取余）
        if (tt[0,i] + 1) % (n + 1) == 0: #此时p取最后个值
            tt3[1,i] = (n + 1)


        
        tt2[0, i] = (tt3[0, i] - 1) * rt + rmin #满足要求的r值
        tt2[1, i] = (tt3[1, i] - 1) * pt + pmin #满足要求的p值


        b = 4 * (n + 1) * (tt3[0,i] - 1) + 4 * (tt3[1,i] - 1) + 2
        # print(b)


        
        
        a = echu[i + 1, b] #满足要求的pI值

        # print(a)
        tt4[0, i] = tt2[1, i] * a
        tt4[1, i] = np.sum(tt4[0,0:i + 1]) + Q #模型求得的Q


    index = 4 * (n + 1) * (tt3[0, -1] - 1) + 4 * (tt3[1, -1] - 1) # 这个index有点问题

    last_e12 = echu[t - 1, index]
    last_e3 = echu[t - 1, index + 1]
    last_I = echu[t - 1, index + 2]
    last_Q = echu[t - 1, index + 3]

    r = tt2[0, -1]
    p = tt2[1, -1]

    predict_e12 = np.zeros((day_to_predict + 1))
    predict_e3 = np.zeros((day_to_predict + 1))
    predict_I = np.zeros((day_to_predict + 1))
    predict_Q = np.zeros((day_to_predict + 1))
    
    predict_e12[0] = last_e12
    predict_e3[0] = last_e3
    predict_I[0] = last_I
    predict_Q[0] = last_Q


    for i in range(0, day_to_predict):
        predict_e12[i + 1] = 0.125 * r * (predict_e3[i] + predict_I[i]) + 0.5 * predict_e12[i]
        predict_e3[i + 1] = 0.5 * predict_e12[i]
        predict_I[i + 1] = predict_e3[i] + 6 / 7 * predict_I[i] - 0.001 * predict_I[i] - p * predict_I[i]
        predict_Q[i + 1] = p * sum(predict_I[0: i]) + predict_Q[0]


    for i in range(1, day_to_predict + 1):
        predict_I[i] *= p



    return {
        "x": list(x),
        "simpI": tt4[0, :].tolist(),
        "truepI": data[:, 0].tolist(),
        "predictpI": predict_I.tolist()[1:],


        "simQ": tt4[1, :].tolist(),
        "trueQ": data[:, 1].tolist(),
        "predictQ": predict_Q.tolist()[1:],

        "rt": tt2[0, :].tolist(),
        "p": tt2[1, :].tolist(),

    }


if __name__ == '__main__':
    app.run(debug=True, port=4060, host='0.0.0.0')
