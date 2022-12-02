import area_boundary
import city_grid
import get_poi
import time
import random

# 更改高德密钥
amap_key = '818880ba1814671017853a3daaf88ee4'
# 更改城市，中文'上海'，或者编码'310000'
city = '310000'

# 瓦片间隔距离，不超过0.05
lattice_split_distance = 0.01

# 搜索的种类 ['加油站', '企业', '公园', '广场', '风景名胜', '小学']等
types = '070000|080000' # 生活服务（070000）和体育休闲服务 （080000）

# 设置输出路径
outputpath = "test_service.csv"


# 1. 获取城市边界的最大、最小经纬度
maxX, minX, maxY, minY = area_boundary.getlnglat(city, amap_key)
print('当前城市：', city, "maxX, minX, maxY, minY：", maxX, minX, maxY, minY)

# 2. 生成网格切片格式：
grids_lib = city_grid.generate_grids(minX, maxY, maxX, minY, lattice_split_distance)

print('划分后的网格数：', len(grids_lib))
print(grids_lib)


# 3. 根据生成的网格爬取数据，这里案例是[0:100]
for grid in grids_lib[0:100]:
    # grid格式：[112.23, 23.23, 112.24, 23.22]
    extent = str(grid[0]) + "," + str(grid[1]) + "|" + str(grid[2]) + "," + str(grid[3])
    print("range", grid)
    #开始翻页
    for page in range(1, 100):
        print('page', str(page))
        # 访问的完整url，输入的params： 包括区域信息和页数
        params = {
            "types": types,
            "offset": 50,
            "key": amap_key,
            "output": "json",
            "page": str(page),
            "polygon": extent
        }
        #访问网址
        poistring = get_poi.getPOI(params, amap_key)
        if poistring != 0 and poistring != -1:
            get_poi.parsePOI(outputpath, poistring)
        #当该页为空，跳出循环，进入下一个区域的查询
        elif poistring == 0:
            break
        #time.sleep(1 + random.randint(0, 9))
    #time.sleep(1 + random.randint(0, 5))
