# -*- coding:utf-8 -*-
import urllib.request
from urllib.parse import quote
import json


url = 'http://restapi.amap.com/v3/config/district?'


def getlnglat(address, key):
    uri = url + 'keywords=' + quote(address) + '&key=' + key + '&subdistrict=1' + '&extensions=all'
    print(uri)

    # 访问链接后，api会回传给一个json格式的数据
    temp = urllib.request.urlopen(uri)
    temp = json.loads(temp.read())

    # polyline是坐标，name是区域的名字
    Data = temp["districts"][0]['polyline']

    lngs = []
    lats = []
    points = []
    for line in str(Data).split(";"):
        if len(line.split("|")) > 1:
            for uu in line.split("|"):
                if float(uu.split(",")[0]) != None:
                    lngs.append(float(uu.split(",")[0]))
                    lats.append(float(uu.split(",")[1]))
                    points.append([float(uu.split(",")[0]), float(uu.split(",")[1])])
        else:
            if float(line.split(",")[0]) != None:
                lngs.append(float(line.split(",")[0]))
                lats.append(float(line.split(",")[1]))
                points.append([float(line.split(",")[0]), float(line.split(",")[1])])

    print(points)
    print(max(lngs), min(lngs), max(lats), min(lats))
    return max(lngs), min(lngs), max(lats), min(lats)





