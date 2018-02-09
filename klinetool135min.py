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
def get3minKline():
    try:
        turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=3min&contract_type=quarter&size=300'
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        print len(ddic)
        return ddic
    except Exception as e:
        print '未请求到数据'
        return None

def get5minKline():
    try:
        turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=5min&contract_type=quarter&size=300'
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

def getMACDXieLv(macddats):
    xl = macddats[-1] - macddats[-2]
    return xl


def getTreadeType(klinedata):
    k1d = klinedata
    # isUP = isClose(k1d)
    if not k1d:
        return None

    dif,dea,macd = get_MACD(k1d)

    macdchange = getMACDXieLv(macd)

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

            return macd[-1],-1,macdchange
        elif macd[s] <= 0 and macd[e] > 0:
            outstr = '零轴以下金叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            print outstr
            return macd[-1],1,macdchange
        else:
            outstr = '零轴以下'
            print outstr
            return macd[-1],0,macdchange
    elif dea[-1] >= 0: #0轴以上
        if macd[s] >= 0 and macd[e] < 0:
            outstr = '零轴以上死叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            print outstr
            return macd[-1],-1,macdchange
        elif macd[s] <= 0 and macd[e] > 0:
            outstr = '零轴以上金叉'
            # cmd  = 'say %s'%(outstr)
            # os.system(cmd)
            # tradetool.isOpenLong = True
            print outstr
            return macd[-1],1,macdchange
        else:
            outstr = '零轴以上'
            print outstr
            return macd[-1],0,macdchange
    #         openShort()

    # outstr = outstr + '%.4f'%(dea[-1])
    # print outstr
    # print timetool.getNowDate(k1d[-1][0]/1000) 
class TradeType(object):
    """docstring for ClassName"""
    def __init__(self,spth):
        self.isOpenLong = False
        self.isOpenShort = False
        self.savepth = spth
        self.watchcount = 3
        self.isMacdSXs = []
        self.isMacdJXs = []

        for i in range(self.watchcount):
            self.isMacdSXs.append(False)
            self.isMacdJXs.append(False)

    def openShort(self,count = basecount):
    

        bs,ss = getDepth()
        price = 0.0
        counttmp = 0
        ss = ss[::-1]
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
        f = open(self.savepth,'a')
        f.write(oustr)
        f.close()
        # tradetool.isOpenShort = True
        self.isOpenShort = True #openshort

        # cmd = 'say 开空操作'
        # os.system(cmd)

    def closeShort(self,msg,count = basecount):
        
        bs,ss = getDepth()
        ss = ss[::-1]
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
        f = open(self.savepth,'a')
        f.write(oustr)
        f.close()
        self.isOpenShort = False #closlong

        # cmd = 'say 平空操作'
        # os.system(cmd)

    def openLong(self,count = basecount):
        
        bs,ss = getDepth()
        ss = ss[::-1]
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
        f = open(self.savepth,'a')
        f.write(oustr)
        f.close()
        self.isOpenLong = True #openlong
        # cmd = 'say 开多操作'
        # os.system(cmd)

    def closeLong(self,msg,count = basecount):
        
        bs,ss = getDepth()
        ss = ss[::-1]
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
        f = open(self.savepth,'a')
        f.write(oustr)
        f.close()
        self.isOpenLong = False #closlong

        # cmd = 'say 平多操作'
        # os.system(cmd)

if not os.path.exists('data/trade'):
    os.mkdir('data/trade')

trademacdtool = TradeType('data/trade/t135m.txt')

def testIsStateWithMacdChange(dat1,dat3,dat5):

    macdv1,macd1type,macdchange1 = dat1
    macdv3,macd3type,macdchange3 = dat3
    macdv5,macd5type,macdchange5 = dat5



    if trademacdtool.isOpenLong:
        # if (macdchange1 < 0 and macdchange3 < 0):
        #     trademacdtool.closeLong('1')
        # elif (macdchange1 < 0 and macdchange5 < 0):
        #     trademacdtool.closeLong('2')
        if macdchange3 < 0 and macdchange5 < 0:
            trademacdtool.closeLong('3')
    else:
        if macdchange1 > 0 and macdchange3 > 0 and macdchange5 > 0:
            trademacdtool.openLong()

    if trademacdtool.isOpenShort:
        # if (macdchange1 > 0 and macdchange3 > 0):
        #     trademacdtool.closeShort('1')
        # elif (macdchange1 > 0 and macdchange5 > 0):
        #     trademacdtool.closeShort('2')
        # el
        if macdchange3 > 0 and macdchange5 > 0:
            trademacdtool.closeShort('3')
    else:
        if macdchange1 < 0 and macdchange3 < 0 and macdchange5 < 0:
            trademacdtool.openShort()

def runloop():
    lastsec = 0
    print 'start run'
    while True:
        loctim = time.localtime()
        hsec = loctim.tm_sec
        
        if hsec == 0:
            # tinksound = 'afplay /System/Library/Sounds/Tink.aiff'
            # os.system(tinksound)
            k1mindata = get1minKline()
            dat1 = getTreadeType(k1mindata)
            time.sleep(1)
            k3mindata = get3minKline()
            dat3 = getTreadeType(k3mindata)
            time.sleep(1)
            k5mindata = get5minKline()
            dat5 = getTreadeType(k5mindata)
            # ordertype = testIsState(dat1,dat3,dat5)
            ordertype = testIsStateWithMacdChange(dat1, dat3, dat5)

            time.sleep(290) #比5分钟少10秒,取数据在这一分马上结束时获取
        else:
            time.sleep(0.4)
            if hsec != lastsec:
                lastsec = hsec


def main():
    # k5d = read5MimKline()
    runloop()


    

#测试
if __name__ == '__main__':
    main()
    # test()
