#!/usr/bin/python3
# -*- coding: utf-8 -*-
# GET_Ftp        : Reconstruct FTP address
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University & Chinese Academy of Surveying and mapping
# Latest Version : 2.09
# Creation Date  : 2022.03.27 - Version 1.00
# Date           : 2023-06-30 - Version 2.09


from datetime import datetime, timedelta
from FTP_Source import FTP_S
from MGEX_name import mgex
from GNSS_Timestran import *


def getftp(t, y, d, hour=None):
    """
    2022-03-27 : * 通过数据类型、年、年积日，获取下载列表，并调用ReplaceTimeWildcard生成下载链接list
                 by Chang Chuntao -> Version : 1.00
    2022-11-02 : > 添加DORIS判断
                 by Chang Chuntao -> Version : 1.25
    """
    if hour is None:
        hour = [0]
    yeard1 = '%04d' % y + '-01-01 00:00:00'
    yeard1 = datetime.datetime.strptime(yeard1, '%Y-%m-%d %H:%M:%S')
    spectime = yeard1 + timedelta(days=d - 1)
    gpsweek, dayofweek = doy2gpswd(y, d)
    ftpsiteout = []
    if t == 'IDS_week_snx':
        if dayofweek == 0:
            ftpsite = FTP_S[t]
            for fd in ftpsite:
                for nowHour in hour:
                    nowSpectime = spectime + datetime.timedelta(hours=nowHour)
                    ftpsiteout.append(ReplaceTimeWildcard(fd, nowSpectime))
    else:
        ftpsite = FTP_S[t]
        for fd in ftpsite:
                for nowHour in hour:
                    nowSpectime = spectime + datetime.timedelta(hours=nowHour)
                    ftpsiteout.append(ReplaceTimeWildcard(fd, nowSpectime))
    return ftpsiteout


def ReplaceTimeWildcard(string, spectime):
    """
    2022-03-27 :    * Replace time wild cards in string with specific date time
                    by Jiang Kecai -> Version : 1.00
    2023-03-17 :    + YYYY_F / YYYY_B / MONTH_F / MONTH_B / DAY_F/ DAY_B
                    by Chang Chuntao  -> Version : 2.08
    """
    import datetime
    newstr = str(string)
    spectime_B = spectime + datetime.timedelta(days=-1)
    spectime_F = spectime + datetime.timedelta(days=1)
    # replace four digit GPS week
    if newstr.find('<GPSW>') >= 0:
        deltime = spectime - datetime.datetime(year=1980, month=1, day=6)
        gpsweek = deltime.days // 7
        newstr = newstr.replace('<GPSW>', '%04d' % gpsweek)
    # replace four digit GPS week and one digit week day
    if newstr.find('<GPSWD>') >= 0:
        deltime = spectime - datetime.datetime(year=1980, month=1, day=6)
        gpsweek = deltime.days // 7
        gpswday = deltime.days - gpsweek * 7
        newstr = newstr.replace('<GPSWD>', '%04d%1d' % (gpsweek, gpswday))
    # replace four digit year
    if newstr.find('<YEAR>') >= 0:
        newstr = newstr.replace('<YEAR>', '%04d' % spectime.year)
    if newstr.find('<YYYY>') >= 0:
        newstr = newstr.replace('<YYYY>', '%04d' % spectime.year)
    if newstr.find('<YY>') >= 0:
        newstr = newstr.replace('<YY>', '%02d' % (spectime.year % 100))
    # replace three digit day number in year
    if newstr.find('<DOY>') >= 0:
        deltime = spectime - datetime.datetime(year=spectime.year, month=1, day=1)
        newstr = newstr.replace('<DOY>', '%03d' % (deltime.days + 1))
    if newstr.find('<DDD>') >= 0:
        newstr = newstr.replace('<DDD>', spectime.strftime('%j'))
    # replace two_digit month in year
    if newstr.find('<MONTH>') >= 0:
        newstr = newstr.replace('<MONTH>', '%02d' % spectime.month)
    # replace two digit day in month
    if newstr.find('<DAY>') >= 0:
        newstr = newstr.replace('<DAY>', '%02d' % spectime.day)

    # replace four digit year
    if newstr.find('<YYYY_F>') >= 0:
        newstr = newstr.replace('<YYYY_F>', '%04d' % spectime_F.year)
    # replace two digit hour in day
    if newstr.find('<MONTH_F>') >= 0:
        newstr = newstr.replace('<MONTH_F>', '%02d' % spectime_F.month)
    if newstr.find('<DAY_F>') >= 0:
        newstr = newstr.replace('<DAY_F>', '%02d' % spectime_F.day)

    # replace four digit year
    if newstr.find('<YYYY_B>') >= 0:
        newstr = newstr.replace('<YYYY_B>', '%04d' % spectime_B.year)
    if newstr.find('<MONTH_B>') >= 0:
        newstr = newstr.replace('<MONTH_B>', '%02d' % spectime_B.month)
    # replace two digit day in month
    if newstr.find('<DAY_B>') >= 0:
        newstr = newstr.replace('<DAY_B>', '%02d' % spectime_B.day)
    # replace two digit hour in day
    if newstr.find('<HOUR>') >= 0:
        newstr = newstr.replace('<HOUR>', '%02d' % spectime.hour)
    # replace two digit minute in hour
    if newstr.find('<MINUTE>') >= 0:
        newstr = newstr.replace('<MINUTE>', '%02d' % spectime.minute)
    # replace two digit second in minute
    if newstr.find('<SECOND>') >= 0:
        newstr = newstr.replace('<SECOND>', '%02d' % spectime.second)
    if newstr.find('<MM>') >= 0:
        newstr = newstr.replace('<MM>', '%02d' % spectime.month)
    if newstr.find('<MMM>') >= 0:
        month_num = spectime.month
        if month_num == 1:
            month_str = "JAN"
        elif month_num == 2:
            month_str = "FEB"
        elif month_num == 3:
            month_str = "MAR"
        elif month_num == 4:
            month_str = "APR"
        elif month_num == 5:
            month_str = "MAY"
        elif month_num == 6:
            month_str = "JUN"
        elif month_num == 7:
            month_str = "JUL"
        elif month_num == 8:
            month_str = "AUG"
        elif month_num == 9:
            month_str = "SEP"
        elif month_num == 10:
            month_str = "OCT"
        elif month_num == 11:
            month_str = "NOV"
        elif month_num == 12:
            month_str = "DEC"
        else:
            month_str = "JAN"
        newstr = newstr.replace('<MMM>', month_str)
    if newstr.find('<WEEK0DOY>') >= 0:
        find_gpsweek, wd = datetime2gpswd(spectime)
        year, week_0_doy = gpswd2doy(find_gpsweek, 0)
        newstr = newstr.replace('<WEEK0DOY>', '%03d' % week_0_doy)

    # return new string
    return newstr


def ReplaceMMM(url, month):
    """
    2022-03-27 : * 替换字符串中<MMM>为三位字符月份
             by Chang Chuntao -> Version : 1.00
    """
    newurl = str(url)
    if month == 1:
        month = "JAN"
    elif month == 2:
        month = "FEB"
    elif month == 3:
        month = "MAR"
    elif month == 4:
        month = "APR"
    elif month == 5:
        month = "MAY"
    elif month == 6:
        month = "JUN"
    elif month == 7:
        month = "JUL"
    elif month == 8:
        month = "AUG"
    elif month == 9:
        month = "SEP"
    elif month == 10:
        month = "OCT"
    elif month == 11:
        month = "NOV"
    elif month == 12:
        month = "DEC"
    newurl = newurl.replace('<MMM>', month)
    return newurl


def ReplaceMM(url, month):
    """
    2022-03-27 : * 替换字符串中<MM>为两位数字
                 by Chang Chuntao -> Version : 1.00
    """
    newurl = str(url)
    month = int(month)
    newurl = newurl.replace('<MM>', '%02d' % month)
    return newurl


def getSite(file, datatype):
    """
    2022-03-27 : * 读取file中站点名，返回site
                 by Chang Chuntao -> Version : 1.00
    2022-08-04 : 修正时序文件下载需求
                 by Chang Chuntao -> Version : 1.19
    2022-09-11 : 站点文件可支持行列两种格式，或混合模式
                 by Chang Chuntao -> Version : 1.20
    2023-01-14 : 支持支持输入站点
                 by Chang Chuntao -> Version : 2.06
    """
    import os
    site = []
    if file == '':
        site = []
    else:
        if os.path.isfile(file):
            fileLine = open(file, "r").readlines()
            for line in fileLine:
                lineSplit = line.split()
                for siteInLine in lineSplit:
                    site.append(siteInLine)
        else:
            site = str(file).split()
    if datatype == "MGEX_IGS_rnx" or datatype == "MGEX_HK_cors":
        for s in range(0, len(site)):
            if len(site[s]) == 9:
                continue
            else:
                site[s] = site[s].lower()
                for m in mgex:
                    if site[s] == m[0]:
                        site[s] = m[1]
    elif datatype == "IGS14_TS_ENU" or datatype == "IGS14_TS_XYZ" or datatype == "Series_TS_Plot":
        for s in range(0, len(site)):
            site[s] = site[s].upper()[0:4]
    else:
        for s in range(0, len(site)):
            site[s] = site[s].lower()[0:4]
    return site


def replaceSiteStr(ftpInList, siteInList):
    """
    2022-09-16 :    替换站点字符串
                    by Chang Chuntao  -> Version : 1.21
    2023-01-14 :    支持大小长短自由
                    by Chang Chuntao  -> Version : 2.06
    2023-03-12 :    新增SITE_SHORT,支持时间序列产品下载
                    by Chang Chuntao  -> Version : 2.18
    """
    upperSite = ''
    if len(siteInList) == 4:
        lowSite = str(siteInList).lower()
        upperShortSite = lowSite.upper()
        for mgexSite in mgex:
            if mgexSite[0] == lowSite:
                upperSite = mgexSite[1]
    elif len(siteInList) == 9:
        lowSite = str(siteInList[0:4]).lower()
        upperSite = str(siteInList).upper()
        upperShortSite = lowSite.upper()
    else:
        lowSite = ''
        upperSite = ''
        upperShortSite = ''
    if '<SITE>' in ftpInList:
        ftpInList = str(ftpInList).replace('<SITE>', lowSite)
    if '<SITE_LONG>' in ftpInList:
        ftpInList = str(ftpInList).replace('<SITE_LONG>', upperSite)
    if '<SITE_SHORT>' in ftpInList:
        ftpInList = str(ftpInList).replace('<SITE_SHORT>', upperShortSite)
    return ftpInList
