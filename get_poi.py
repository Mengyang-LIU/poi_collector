import requests
import csv
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方


# 以下是用于坐标转换的函数
def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) +
            20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) +
            40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) +
            320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) +
            20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) +
            40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) +
            300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def WriteLog(str):
    f = open("log2.txt", 'a')
    print(str)
    f.write(str)
    f.close()


def writetoFile(outputpath, poiInfoList):
    with open(outputpath, "a", newline='') as f:
        csvW = csv.writer(f)
        csvW.writerow(poiInfoList)


def parsePOI(outputpath, poiString):
    for poi in poiString:
        infoList = []

        infoList.append(poi['id'])
        infoList.append(poi['name'])
        infoList.append(poi['typecode'])

        tempX = str(poi["location"]).split(',')[0]
        tempY = str(poi["location"]).split(',')[1]
        # 将高德坐标转换为WGS84坐标
        infoX, infoY = gcj02_to_wgs84(float(tempX), float(tempY))
        infoList.append(infoX)
        infoList.append(infoY)
        writetoFile(outputpath, infoList)
        # 这里只示例输出最简单的经纬度、ID、名称、类型信息，需要何种信息可自己设置


def getPOI(params, key):
    url = "http://restapi.amap.com/v3/place/polygon?"
    try:
        r = requests.get(url, params, timeout=20)
        rjson = r.json(encoding="utf-8")
        # 判断是否爬取成功
        if rjson["info"] == "OK":
            # 判断该页是否不为空，不为空则返回pois进行解析
            if len(rjson["pois"]) > 0:
                return rjson["pois"]
            # 该页为空
            else:
                return 0
        # 爬取失败
        else:
            print("error info:", rjson["info"])  # 输出状态信息
            return -1
    except Exception as e:
        # 出错则将错误写入日志
        WriteLog("url={0},key:{1},message:{2}\n".format(url, key, repr(e)))
        return -1
        pass


if __name__ == "__main__":
    amap_key = '818880ba1814671017853a3daaf88ee4'
    types = '070000|080000'
    # 左下 右上范围
    minX = 116.3
    maxX = 116.4
    minY = 39.9
    maxY = 40.0
    # X为经度范围，Y为纬度范围
    # 搜索网格的大小
    interX = 0.01
    interY = 0.01
    # 取余加1变成完整的格子
    xnum = int((maxX - minX) / interX) + 1
    ynum = int((maxY - minY) / interY) + 1

    # 设置输出路径
    outputpath = "test.csv"

    # 对每个划分的网格遍历，搜索POI，i从0开始
    for i in range(xnum):
        for j in range(ynum):  # 左上，右下xy
            startX = minX + i * interX
            startY = minY + (j + 1) * interY
            endX = minX + (i + 1) * interX
            endY = minY + j * interY
            # 设置范围
            extent = str(startX) + "," + str(startY) + "|" + str(endX) + "," + str(endY)
            print("range", startX, startY, endX, endY)
            # 开始翻页
            for page in range(1, 100):
                # 访问的完整url
                params = {
                    "types": types,
                    "offset": 50,
                    "coord_type": 1,
                    "key": amap_key,
                    "output": "json",
                    "page": str(page),
                    "polygon": extent
                }

                # 访问网址
                poistring = getPOI(params, amap_key)
                if poistring != 0 and poistring != -1:
                    parsePOI(outputpath, poistring)
                # 当该页为空，跳出循环，进入下一个区域的查询
                elif poistring == 0:
                    break
