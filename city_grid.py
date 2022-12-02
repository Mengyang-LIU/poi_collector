import numpy as np
from area_boundary import getlnglat
import pandas as pd


def generate_grids(start_long, start_lat, end_long, end_lat, resolution):

    assert start_long < end_long, '需要从左上到右下设置经度，start的经度应小于end的经度'
    assert start_lat > end_lat, '需要从左上到右下设置纬度，start的纬度应大于end的纬度'
    assert resolution > 0, 'resolution应大于0'


    grids_lib = []
    # 经度从左上到右下，resolution为正数
    longs = np.arange(start_long, end_long, resolution)
    if longs[-1] != end_long:
        longs = np.append(longs, end_long)

    # 纬度从左上到右下，resolution为负数
    lats = np.arange(start_lat, end_lat, -resolution)
    if lats[-1] != end_lat:
        lats = np.append(lats, end_lat)
    for i in range(len(longs)-1):
        for j in range(len(lats)-1):
            grids_lib.append([round(float(longs[i]), 6), round(float(lats[j]), 6), round(float(longs[i+1]), 6), round(float(lats[j+1]), 6)])
            #yield [round(float(longs[i]),6),round(float(lats[j]),6),round(float(longs[i+1]),6),round(float(lats[j+1]),6)]
    return grids_lib


# grids_lib = generate_grids(112.958507, 23.932988, 114.059957, 22.51436, 0.1)
# print(grids_lib)


if __name__ == "__main__":
    city = '310000' # 上海编码 （'310000'）
    amap_key = '818880ba1814671017853a3daaf88ee4'

    lattice_split_distance = 0.01
    # 得到城市整个的边界数据
    maxX, minX, maxY, minY = getlnglat(city, amap_key)
    # 生成网格切片格式：
    grids_lib = generate_grids(minX, maxY, maxX, minY, lattice_split_distance)
    print(grids_lib)
    print('划分后的网格数：', len(grids_lib))

    df = pd.DataFrame(grids_lib, columns=['minX', 'maxY', 'maxX', 'minY'])
    df.to_csv('{0}.csv'.format(city), encoding='gbk')
    print('done')