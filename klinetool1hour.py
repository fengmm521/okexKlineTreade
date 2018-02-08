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
from magetool import listtool
import numpy as np
import time   


if not os.path.exists('data'):
    os.mkdir('data')


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
    try:
        turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1min&contract_type=quarter&size=300'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        print len(ddic)
        return ddic
    except Exception as e:
        print '未请求到数据'
        return None

def get15minKline():
    try:
        turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=15min&contract_type=quarter&size=300'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        print len(ddic)
        return ddic
    except Exception as e:
        print '未请求到数据'
        return None

def get30minKline():
    try:
        turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=30min&contract_type=quarter&size=300'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        print len(ddic)
        return ddic
    except Exception as e:
        print '未请求到数据'
        return None

def get1hourKline():
    try:
        turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1hour&contract_type=quarter&size=300'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        print len(ddic)
        return ddic
    except Exception as e:
        print '未请求到数据'
        return None

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
    

basecount = 1
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

    
def test():
    # openLong()
    print timetool.getNowDate()
    #1.buy,0.不操作，-1.sell




def isClose(k1d):
    ave3 = getAverageData(k1d,3)
    ave5 = getAverageData(k1d,5)
    ave13 = getAverageData(k1d,13)

def getTreadeType(klinedata):
    k1d = klinedata
    # isUP = isClose(k1d)
    if not k1d:
        return None

    dif,dea,macd = get_MACD(k1d)
    outstr = ''
    tp = 0
    s = -2
    e = -1
    if dea[-1] <= 0:  #0轴以下
        if macd[s] >= 0 and macd[e] < 0:
            outstr = '零轴以下死叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            print outstr
            return -1,-1
        elif macd[s] <= 0 and macd[e] > 0:
            outstr = '零轴以下金叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            print outstr
            return -1,1
        else:
            outstr = '零轴以下'
            print outstr
            return -1,0
    elif dea[-1] >= 0: #0轴以上
        if macd[s] >= 0 and macd[e] < 0:
            outstr = '零轴以上死叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            print outstr
            return 1,-1
        elif macd[s] <= 0 and macd[e] > 0:
            outstr = '零轴以上金叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            # tradetool.isOpenLong = True
            print outstr
            return 1,1
        else:
            outstr = '零轴以上'
            print outstr
            return 1,0
    #         openShort()

    # outstr = outstr + '%.4f'%(dea[-1])
    # print outstr
    # print timetool.getNowDate(k1d[-1][0]/1000) 
class TradeType(object):
    """docstring for ClassName"""
    def __init__(self):
        self.isOpenLong = False
        self.isOpenShort = False
        self.isMacd15SX = False
        self.isMacd15JX = False
        self.isMacd30SX = False
        self.isMacd30JX = False

tradetool = TradeType()

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
    # tradetool.isOpenShort = True
    tradetool.isOpenShort = True #openshort

    # cmd = 'say 开空操作'
    # os.system(cmd)

def closeShort(msg,count = basecount):
    
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
    tradetool.isOpenShort = False #closlong

    # cmd = 'say 平空操作'
    # os.system(cmd)

def openLong(count = basecount):
    
    bs,ss = getDepth()

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
    tradetool.isOpenLong = True #openlong
    # cmd = 'say 开多操作'
    # os.system(cmd)

def closeLong(msg,count = basecount):
    
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
    tradetool.isOpenLong = False #closlong

    # cmd = 'say 平多操作'
    # os.system(cmd)



def testIsState(dea15type,macd15type,dae30type,macd30type):

    if macd30type == 1:
        tradetool.isMacd30JX = True
        tradetool.isMacd30SX = False
    elif macd30type == -1:
        tradetool.isMacd30JX = False
        tradetool.isMacd30SX = True

    if macd15type == 1:
        tradetool.isMacd15JX = True
        tradetool.isMacd15SX = False
    elif macd15type == -1:
        tradetool.isMacd15JX = False
        tradetool.isMacd15SX = True

    if tradetool.isMacd15JX and tradetool.isMacd30JX:
        if not tradetool.isOpenLong: #openlong
            openLong()
        if tradetool.isOpenShort:
            closeShort()
    elif tradetool.isMacd15SX and tradetool.isMacd30SX:
        if not tradetool.isOpenShort:
            openShort()
        if tradetool.isOpenLong:
            closeLong()
    elif tradetool.isOpenLong and tradetool.isMacd15SX:
        closeLong()
    elif tradetool.isOpenShort and tradetool.isMacd15JX:
        closeShort()


def runloop():
    lastsec = 0
    print 'start run'
    while True:
        loctim = time.localtime()
        hsec = loctim.tm_sec
        
        if hsec == 0:
            # tinksound = 'afplay /System/Library/Sounds/Tink.aiff'
            # os.system(tinksound)
            k15mindata = get15minKline()
            deatype15,macdtype15 = getTreadeType(k15mindata)
            time.sleep(1)
            k30mindata = get30minKline()
            deatype30,macdtype30 = getTreadeType(k30mindata)
            ordertype = testIsState(deatype15,macdtype15,deatype30,macdtype30)

            time.sleep(900) #15分钟
        else:
            time.sleep(0.5)
            if hsec != lastsec:
                lastsec = hsec


def main():
    # k5d = read5MimKline()
    runloop()


    

#测试
if __name__ == '__main__':
    main()
    # test()
