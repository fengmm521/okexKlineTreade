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
import time   

    #[1510590900000, 64.535, 64.564, 64.38, 64.518, 9022.0, 1399.350184200521]
    ##时间戳，开，高，低，收，交易量，交易量转化为BTC或LTC数量
def get1minKline():
    turl = 'https://www.okex.com/api/v1/future_kline.do?symbol=ltc_usd&type=1min&contract_type=quarter&size=300'
    try:
        data = urltool.getUrl(turl)
        ddic = json.loads(data)
        print len(ddic)
        return ddic
    except Exception as e:
        print '获取数据错误,%s'%(str(timetool.getNowDate()))
        return None
    
def getListDatasForLineTxt(datas):
    outstr = ''
    for d in datas:
        outstr += json.dumps(d) + '\n'
    outstr = outstr[:-1]
    return outstr


def save1minKline(klinedat):
    daystr = timetool.getDateDay()
    if not os.path.exists('data'):
        os.mkdir('data')
    kline1mpth = 'data/' + daystr +'kline1m.txt'
    if not os.path.exists(kline1mpth):
        datas = klinedat[::-1]
        listtool.saveListWithLineTxt(datas, kline1mpth)
    else:
        datas = klinedat[::-1]
        outstr = '\n' + getListDatasForLineTxt(datas)
        f = open(kline1mpth,'a')
        f.write(outstr)
        f.close()

def runloop():
    lastsec = 0
    lastklines = []
    while True:
        loctim = time.localtime()
        hsec = loctim.tm_sec
        
        if hsec == 0:
            k1d = get1minKline()
            if k1d:
                k1d = k1d[:-1]
                k1d = k1d[::-1]
                lastklines = k1d
                save1minKline(k1d)
                delaytime = 299*60 + 0.4
                time.sleep(delaytime) #每次取300分钟数据
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
