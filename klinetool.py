#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-28 16:28:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import json
from magetool import urltool
from magetool import timetool
import numpy as np
import time   

BaseKlinePth = 'data/kline.txt'

def read5MimKline():
    f = open(BaseKlinePth,'r')
    lines = f.readlines()
    f.close()
    kdats = []
    for l in lines:
        tmpl = l.replace('\n','').replace('\r','')
        tmpdat = json.loads(tmpl)
        kdats.append(tmpdat)

    # print len(kdats),len(kdats[0])
    return kdats
    #[1510590900000, 64.535, 64.564, 64.38, 64.518, 9022.0, 1399.350184200521]
    ##时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
def get1minKline():
    turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1min&contract_type=quarter&size=300'
    data = urltool.getUrl(turl)
    ddic = json.loads(data)
    print len(ddic)
    return ddic

def getAverageData(datas,pAver = 3,didx = 4):
    #[1517536380000,142.443,142.443,142,142,3486,244.8654307]
    ##时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
    outs = []
    for n in range(len(datas)):
        d = datas[n]
        tmps = [d[0]]
        if n < pAver -1:
            dtmp = datas[0:n+1]
            vtmp = [x[didx] for x in dtmp]
            mean = np.mean(vtmp)
            tmps.append(mean)
        else:
            dtmp = datas[n - pAver+1:n+1]
            vtmp = [x[didx] for x in dtmp]
            mean = np.mean(vtmp)
            tmps.append(mean)
        outs.append(tmps)
    return outs

def subList(lis1,lis2):
    v1 = list(lis1)
    v2 = list(lis2)
    v = list(map(lambda x: x[0]-x[1], zip(v1, v2)))
    return v


def get_EMA(df,N,idx = 4):  
    emas = []
    for i in range(len(df)):  
        if i==0:  
            emas = [df[i][idx]]
        if i>0:  
            emastmp = (emas[-1] * (N-1.0) + df[i][idx] * 2.0)/(N+1.0)
            emas.append(emastmp)
    return emas  



def get_MACD(df,dshort = 12,dlong = 26,M = 9):
    a=get_EMA(df,dshort)  
    b=get_EMA(df,dlong)  
    DIF=subList(a, b) 

    DEA = []
    #print(df['diff'])  
    for i in range(len(df)):  
        if i==0:  
            # df.ix[i,'dea']=df.ix[i,'diff'] 
            DEA = [DIF[i]] 

        if i>0:  
            DEAtmp = (2 * DIF[i] + (M - 1) * DEA[i-1])/(M+1)
            DEA.append(DEAtmp)

    MACD = list(map(lambda x: (x[0]-x[1])*2, zip(DIF, DEA)))

    return DIF,DEA,MACD
    

basemoney = [100]
basecount = 10
savepth = 'data/simulation.txt'

#price,count
longprice = []
shortprice = []


def getDepth():
    turl = 'https://www.okex.com/api/v1/future_depth.do?symbol=ltc_usd&contract_type=quarter&size=20'
    data = urltool.getUrl(turl)
    ddic = json.loads(data)
    buys = ddic['bids']
    sells = ddic['asks']
    return buys,sells

def openLong(count = basecount):
    bs,ss = getDepth()
    print bs
    print ss
    price = 0.0

    counttmp = 0

    n = 0
    while True:
        n -= 1
        counttmp += ss[n][1]
        if counttmp >= count:
            price = ss[-n][0]
            break
        if n < -5:
            price = bs[-5][0]
            break
    strtime = str(timetool.getNowDate())
    oustr = 'openLong_%.4f_%d,%s\n'%(price,count,strtime)
    print oustr
    f = open(savepth,'a')
    f.write(oustr)
    f.close()
    cmd = 'say 开多操作'
    os.system(cmd)

    
def openShort(count = basecount):
    bs,ss = getDepth()
    price = 0.0
    counttmp = 0

    n = 0
    while True:
        n -= 1
        counttmp += bs[n][1]
        if counttmp >= count:
            price = bs[-n][0]
            break
        if n < -5:
            price = bs[-5][0]
            break
    strtime = str(timetool.getNowDate())
    oustr = 'openShort_%.4f_%d,%s\n'%(price,count,strtime)
    print oustr
    f = open(savepth,'a')
    f.write(oustr)
    f.close()
    cmd = 'say 开空操作'
    os.system(cmd)


def closeLongTrade(msg):
    bs,ss = getDepth()
    price = 0.0
    counttmp = 0

    n = 0
    while True:
        n -= 1
        counttmp += bs[n][1]
        if counttmp >= count:
            price = bs[-n][0]
            break
        if n < -5:
            price = bs[-5][0]
            break
    strtime = str(timetool.getNowDate())
    oustr = 'closeLong_%.4f_%d,%s,%s\n'%(price,count,strtime,msg)
    print oustr
    f = open(savepth,'a')
    f.write(oustr)
    f.close()
    cmd = 'say 平多操作'
    os.system(cmd)

def closeShortTrade(msg):
    bs,ss = getDepth()
    print bs
    print ss
    price = 0.0

    counttmp = 0

    n = 0
    while True:
        n -= 1
        counttmp += ss[n][1]
        if counttmp >= count:
            price = ss[-n][0]
            break
        if n < -5:
            price = bs[-5][0]
            break
    strtime = str(timetool.getNowDate())
    oustr = 'closeShort_%.4f_%d,%s,%s\n'%(price,count,strtime,msg)
    print oustr
    f = open(savepth,'a')
    f.write(oustr)
    f.close()
    cmd = 'say 平空操作'
    os.system(cmd)


    
def test():
    # openLong()
    print timetool.getNowDate()
    #1.buy,0.不操作，-1.sell

isopens = [False,False]
openindex = [0,0]
closeindex = [0,0]  #[buy,sell],均线金叉和死叉位置

def getTreadeType():
    k1d = get1minKline()
    ave3 = getAverageData(k1d,3)
    ave5 = getAverageData(k1d,5)
    ave13 = getAverageData(k1d,13)
    if ave5[-2] > ave13[-2] and ave5[-1] < ave13[-1]: #均线死叉
        closeindex[1] = 0
        closeindex[0] = -1
    elif ave5[-2] < ave13[-2] and ave5[-1] > ave13[-1]:
        closeindex[0] = 0   
        closeindex[1] = -1 
    else:
        if closeindex[0] >= 0:
            closeindex[0] += 1
        if closeindex[1] >= 0:
            closeindex[1] += 1

    dif,dea,macd = get_MACD(k1d)
    outstr = ''
    tp = 0
    s = -2
    e = -1
    if dea[-1] <= 0:  #0轴以下
        if macd[s] >= 0 and macd[e] < 0:
            outstr = '零轴以下死叉'
            tp = -1
        elif macd[s] <= 0 and macd[e] > 0:
            outstr = '零轴以下金叉'
            tp = 0
        else:
            outstr = '零轴以下'
            tp = 0
    elif dea[-1] >= 0: #0轴以上
        if macd[s] >= 0 and macd[e] < 0:
            outstr = '零轴以上死叉'
            tp = 0
        elif macd[s] <= 0 and macd[e] > 0:
            outstr = '零轴以上金叉'
            tp = 1
        else:
            outstr = '零轴以上'
            tp = 0

    if tp != 0:
        cmd = 'say %s,DEA等于%.2f'%(outstr,dea[-1])
        os.system(cmd)
        if tp < 0:
            openShort()
            openindex[1] = 1
        elif tp > 0:
            openLong()
            openindex[0] = 1
    outstr = outstr + '%.4f'%(dea[-1])
    print outstr
    

    if openindex[1] > 0:
        #已作空
        if closeindex[1] > 0 and closeindex[1] <= 2:
            #时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
            if k1d[-1][2] > ave13[-1]:#最高价高于13均线，平空止损
                closeShortTrade('stop_loss')
                openindex[1] = -1
        elif closeindex[1] >= 2:
            if k1d[-1][4] > ave13[-1]:#达到止盈13均线,平空
                closeShortTrade('stop_trader')
                openindex[1] = -1

    if openindex[0] > 0:
        #已作多
        if closeindex[0] > 0 and closeindex[0] <= 2:
            #时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
            if k1d[-1][2] > ave13[-1]:#最高价高于13均线，平空止损
                closeLongTrade('stop_loss')
                openindex[0] = -1
        elif closeindex[0] >= 2:
            if k1d[-1][4] > ave13[-1]:#达到止盈13均线,平空
                closeLongTrade('stop_trader')
                openindex[0] = -1
    return tp


def runloop():
    lastsec = 0
    while True:
        loctim = time.localtime()
        hsec = loctim.tm_sec
        
        if hsec == 0:
            tp = getTreadeType()
            if tp == 0:
                print '-------------不操作'
            elif tp > 0:
                print '-------------可买入'
                cmd = 'say 注意，已买入'
                os.system(cmd)
            elif tp < 0:
                print '-------------可卖出'
                cmd = 'say 注意，已卖出'
                os.system(cmd)
            time.sleep(50)
        else:
            time.sleep(0.5)
            if hsec != lastsec:
                # print hsec
                lastsec = hsec




def main():
    # k5d = read5MimKline()
    runloop()


    

#测试
if __name__ == '__main__':
    main()
    # test()
