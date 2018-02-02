#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-12-28 16:28:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import json
import urllib2
import chardet
import hashlib

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

def conventNewKline(dats):
    tmps = [0]*6
    tmps[0] = dats[-1][0]  #时间取收盘时间
    tmps[1] = dats[0][1]  #开盘价
    for d in dats:
        if tmps[2] < d[2]:
            tmps[2] = d[2] # 最高价
        if tmps[3] == 0 or tmps[3] > d[3]:
            tmps[3] = d[3] #最低价
        tmps[5] += d[5]    #成交量
    tmps[4] = dats[-1][4]  #收盘价

    return tmps

def create1HourKline(kdat5m):
    h1dats = []

    lenk5 = len(kdat5m)

    k1hourIndexs = []
    for n in range(len(kdat5m)):
        tmps = []
        if lenk5 - n >= 12:
            sindex = n
            eindex = n + 12
            k1hourIndexs.append([sindex,eindex])


    for ns in k1hourIndexs:
        dattmps = kdat5m[ns[0]:ns[1]]
        newdat = conventNewKline(dattmps)
        h1dats.append(newdat)

    return h1dats

def savetestlist(dats,savename):
    outstrs = ''
    for d in dats:
        outstrs += str(d) + '\n'
    spth = 'data/perdata/'+ savename
    f = open(spth,'w')
    f.write(outstrs)
    f.close()


def create4HourKline(kdat5m):
    hdats = []

    count5m = 48 #4小时有48个5分钟

    lenk5 = len(kdat5m)

    k1hourIndexs = []
    for n in range(len(kdat5m)):
        tmps = []
        if lenk5 - n >= count5m:
            sindex = n
            eindex = n + count5m
            k1hourIndexs.append([sindex,eindex])


    for ns in k1hourIndexs:
        dattmps = kdat5m[ns[0]:ns[1]]
        newdat = conventNewKline(dattmps)
        hdats.append(newdat)


    # savetestlist(hdats, '4h.txt')
    

    return hdats

def create12HourKline(kdat5m):
    hdats = []

    count5m = 144 #12小时有144个5分钟

    lenk5 = len(kdat5m)

    k1hourIndexs = []
    for n in range(len(kdat5m)):
        tmps = []
        if lenk5 - n >= count5m:
            sindex = n
            eindex = n + count5m
            k1hourIndexs.append([sindex,eindex])


    for ns in k1hourIndexs:
        dattmps = kdat5m[ns[0]:ns[1]]
        newdat = conventNewKline(dattmps)
        hdats.append(newdat)

    return hdats

def create24HourKline(kdat5m):
    hdats = []

    count5m = 288 #24小时有288个5分钟

    lenk5 = len(kdat5m)

    k1hourIndexs = []
    for n in range(len(kdat5m)):
        tmps = []
        if lenk5 - n >= count5m:
            sindex = n
            eindex = n + count5m
            k1hourIndexs.append([sindex,eindex])


    for ns in k1hourIndexs:
        dattmps = kdat5m[ns[0]:ns[1]]
        newdat = conventNewKline(dattmps)
        hdats.append(newdat)

    return hdats

def conventStrTOUtf8(oldstr):
    try:
        nstr = oldstr.encode("utf-8")
        return nstr
    except Exception as e:
        print 'nstr do not encode utf-8'
    cnstrtype = chardet.detect(oldstr)['encoding']
    utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
    return utf8str

def getUrl(purl):
    try:
        req = urllib2.Request(purl)
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req)
        html = conventStrTOUtf8(res.read())
        return html
    except Exception, e:
        print e
    return None


def getOneYearMaxVale():
    #https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1day&contract_type=quarter&size=400
    yeardatpth = 'data/yearDayData.txt'
    if not os.path.exists(yeardatpth):
        tmpurl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1day&contract_type=quarter&size=400'
        dat = getUrl(tmpurl)
        f = open(yeardatpth,'w')
        f.write(dat)
        f.close()
        klines = json.loads(dat)
        if klines:
            maxvalve = 0.0
            #时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
            for d in klines:
                if d[5] > maxvalve:
                    maxvalve = d[5]
            return maxvalve
        else:
            return 0
    else:
        f = open(yeardatpth,'r')
        dat = f.read()
        f.close()
        klines = json.loads(dat)
        if klines:
            maxvalve = 0.0
            #时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
            for d in klines:
                if d[5] > maxvalve:
                    maxvalve = d[5]
            return maxvalve
        else:
            return 0
def conventForNNData(datas,valveBase,priceSalce,savepth):
    outdatas = []
    #时间戳，开，高，低，收，交易量
    baseIndex = 4    #以收盘价为0基准
    for d in datas:
        tmps = []
        priceBase = priceSalce*d[baseIndex]
        tmps.append(d[0])
        tmps.append((d[1] - d[baseIndex])/priceBase)
        tmps.append((d[2] - d[baseIndex])/priceBase)
        tmps.append((d[3] - d[baseIndex])/priceBase)
        tmps.append((d[4] - d[baseIndex])/priceBase)
        tmps.append(d[5]/valveBase)
        if tmps[1] > 1.0:
            print 'ddddd1'
        if tmps[2] > 1.0:
            print 'ddddd2'
        if tmps[3] > 1.0:
            print 'ddddd3'
        if tmps[4] > 1.0:
            print 'ddddd4'
        if tmps[5] > 1.0:
            print 'ddddd5',d[5],valveBase
        outdatas.append(tmps)

    # savetestlist(outdatas, '4h2.txt')

    outstr = json.dumps(outdatas)
    f = open(savepth,'w')
    f.write(outstr)
    f.close()
    print savepth

prekline5mpth = 'data/perdata/kline5m.txt'
perkline1hpth = 'data/perdata/kline1h.txt'
perkline4hpth = 'data/perdata/kline4h.txt'
perkline12hpth = 'data/perdata/kline12h.txt'
perkline24hpth = 'data/perdata/kline24h.txt'

if not os.path.exists('data/perdata'):
    os.mkdir('data/perdata')
    os.mkdir('data/nndata')
def conventAllNNdata():


    maxv = getOneYearMaxVale()
    if maxv < 0:
        return False

    kdat5m = read5MimKline()
    v5m =  maxv/8.0            #5分钟的基础成交量取400天中最大一天成交量的八分之一
    price5mbase = 0.2          #5分钟的价格最大变化标准化基数为收盘价的20%
    conventForNNData(kdat5m, v5m, price5mbase,prekline5mpth)

    k1hours = create1HourKline(kdat5m)
    v1h = maxv/4.0              #1小时基础成交量取400天中最大一天成交量的四分之一
    price1hbase = 0.4          #1小时的价格最大变化标准化基数为收盘价的40%
    conventForNNData(k1hours, v1h,price1hbase, perkline1hpth)

    k4hours = create4HourKline(kdat5m)

    v4h = maxv                 #4小时基础成交量取400天中最大一天成交量的二分之一
    price4hbase = 0.6          #4小时的价格最大变化标准化基数为收盘价的60%
    conventForNNData(k4hours, v4h,price4hbase, perkline4hpth)

    k12hours = create12HourKline(kdat5m)
    v12h = maxv                 #12小时基础成交量取400天中最大一天成交量
    price12hbase = 0.8          #12小时的价格最大变化标准化基数为收盘价的80%
    conventForNNData(k12hours, v12h,price12hbase, perkline12hpth)

    k24hours = create24HourKline(kdat5m)
    v24h = maxv*2.0             #24小最基础成交量取400天中最大成交量的2倍
    price24hbase = 1.0          #24小时的价格最大变化标准化基数为收盘价的100%
    conventForNNData(k24hours, v24h,price24hbase, perkline24hpth)




    return True

# prekline5mpth = 'data/perdata/kline5m.txt'
# perkline1hpth = 'data/perdata/kline1h.txt'
# perkline4hpth = 'data/perdata/kline4h.txt'
# perkline12hpth = 'data/perdata/kline12h.txt'
# perkline24hpth = 'data/perdata/kline24h.txt'

trainingAllpth = 'data/nndata/data24h12h4h1h5m_10.txt' 
trainingOlay5mPth = 'data/nndata/data5m_10.txt'
trainingOlay1hPth = 'data/nndata/data1h_10.txt'
trainingOlay4hPth = 'data/nndata/data4h_10.txt'
trainingOlay12hPth = 'data/nndata/data12h_10.txt'
trainingOlay24hPth = 'data/nndata/data24h_10.txt'

training5mpth = 'data/nndata'

def saveListDataToPth(datas,pth):
    print pth
    outstr = json.dumps(datas)
    f = open(pth,'w')
    f.write(outstr)
    f.close()


def createTrainingNNData(trainDcount = 10):   #默认取10个数据为一组进行训练
    f = open(perkline24hpth,'r')
    tmpstr = f.read()
    f.close()
    h24dats = json.loads(tmpstr)

    lendata = len(h24dats)

    f = open(perkline12hpth,'r')
    tmpstr = f.read()
    f.close()
    h12dats = json.loads(tmpstr)
    h12dats = h12dats[-lendata:]

    f = open(perkline4hpth,'r')
    tmpstr = f.read()
    f.close()
    h4dats = json.loads(tmpstr)
    h4dats = h4dats[-lendata:]

    f = open(perkline1hpth,'r')
    tmpstr = f.read()
    f.close()
    h1dats = json.loads(tmpstr)
    h1dats = h1dats[-lendata:]

    f = open(prekline5mpth,'r')
    tmpstr = f.read()
    f.close()
    m5dats = json.loads(tmpstr)
    m5dats = m5dats[-lendata:]

    print '训练数据总长度',lendata
    dataIndexs = []
    for i in range(lendata):
        if lendata - i >= trainDcount:
            dataIndexs.append([i,i + trainDcount])

    trdatas = []
    trm5datas = []
    trh1datas = []
    trh4datas = []
    trh12datas = []
    trh24datas = []
    print dataIndexs[-1]
    for ix in dataIndexs:
        h24tmps = h24dats[ix[0]:ix[1]]
        oh24tmps = []
        for d in h24tmps:
            oh24tmps += d[1:]
        trh24datas.append(oh24tmps)

        h12tmps = h12dats[ix[0]:ix[1]]
        oh12tmps = []
        for d in h12tmps:
            oh12tmps += d[1:]
        trh12datas.append(oh12tmps)

        h4tmps = h4dats[ix[0]:ix[1]]
        oh4tmps = []
        for d in h4tmps:
            oh4tmps += d[1:]
        trh4datas.append(oh4tmps)

        h1tmps = h1dats[ix[0]:ix[1]]
        oh1tmps = []
        for d in h1tmps:
            oh1tmps += d[1:]
        trh1datas.append(oh1tmps)

        m5tmps = m5dats[ix[0]:ix[1]]
        om5tmps = []
        for d in m5tmps:
            om5tmps += d[1:]
        trm5datas.append(om5tmps)

        outtmp = oh24tmps + oh12tmps + oh4tmps + oh1tmps + om5tmps
        trdatas.append(outtmp)


    saveListDataToPth(trh24datas, trainingOlay24hPth)   #单独保存24小时数据
    saveListDataToPth(trh12datas, trainingOlay12hPth)   #单独保存12小时数据
    saveListDataToPth(trh4datas, trainingOlay4hPth)     #单独保存4小时数据
    saveListDataToPth(trh1datas, trainingOlay1hPth)     #单独保存1小时数据
    saveListDataToPth(trm5datas, trainingOlay5mPth)     #单独保存5分钟数据

    saveListDataToPth(trdatas, trainingAllpth)          #保存所有组合数据



def createTrainingSigmoidData(datpth,savepth):
    f = open(datpth,'r')
    jstr = f.read()
    f.close()
    dats = json.loads(jstr)
    outs = []
    lcount = 0
    for d in dats:

        tmps = []
        llcount = 0
        for t in d:
            tmp = (t/2.0) + 0.5
            if tmp < 0:
                tmp = 0.0
                print('is small')
            if tmp > 1.0:
                print tmp,t
                print datpth
                print('is big',lcount,llcount)
                tmp = 1.0

            tmps.append(tmp)
            llcount += 1
        outs.append(tmps)
        lcount += 1
    ostr = json.dumps(outs)
    f = open(savepth,'w')
    f.write(ostr)
    f.close()
def createAllTrainingSigmoidData():
    pths = [trainingOlay5mPth,trainingOlay1hPth,trainingOlay4hPth,trainingOlay12hPth,trainingOlay24hPth]
    for p in pths:
        pthtmp,pname = os.path.split(p)
        savepth = pthtmp + os.sep + 'sigmoid_' + pname
        createTrainingSigmoidData(p, savepth)

hash5mklinefile = 'data/klinehash.txt'

def main():
    f = open('data/kline.txt','r')
    klinehash = hashlib.sha256(f.read()).hexdigest()

    isKlineChange = True
    if not os.path.exists(hash5mklinefile):
        conventAllNNdata()
        f = open(hash5mklinefile,'w')
        f.write(klinehash)
        f.close()
    else:
        f = open(hash5mklinefile,'r')
        lasthash = f.read()
        f.close()
        if lasthash != klinehash:
            conventAllNNdata()
            f = open(hash5mklinefile,'w')
            f.write(klinehash)
            f.close()
        else:
            print 'k线数据未改变，不会生成数的其他k线数据'
            isKlineChange = False
    if isKlineChange:
        print 'k线数据发生改变，开始生成新的训练数据'
        createTrainingNNData()
        createAllTrainingSigmoidData()
        print '新的训练数据生成完成，保存在:%s'%(training5mpth)
    conventAllNNdata()
    createTrainingNNData()
    createAllTrainingSigmoidData()


def test():
    maxvalue = getOneYearMaxVale()
    print maxvalue
    kdat5m = read5MimKline()
    print '5mim clount=',len(kdat5m)
    k1hours = create1HourKline(kdat5m)
    print '1hour count=',len(k1hours)
    print k1hours[0]
    print k1hours[-1]


    print '--------------'
    k4hours = create4HourKline(kdat5m)
    print '4hour count=',len(k4hours),len(kdat5m) - len(k4hours)
    print k4hours[0]
    print k4hours[-1]

    print '--------------'
    k4hours = create12HourKline(kdat5m)
    print '12hour count=',len(k4hours),len(kdat5m) - len(k4hours)
    print k4hours[0]
    print k4hours[-1]

    print '--------------'
    k4hours = create24HourKline(kdat5m)
    print '24hour count=',len(k4hours),len(kdat5m) - len(k4hours)
    print k4hours[0]
    print k4hours[-1]

#测试
if __name__ == '__main__':
    # a = [0] * 6
    # hour1s = range(12)
    # print hour1s
    # print a
    main()
    # test()
