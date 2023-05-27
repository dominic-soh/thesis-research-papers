from osgeo import gdal
import numpy as np
import datetime
import dill
from dateutil.relativedelta import relativedelta


# util functions
def get_bloom_pixels(bloom_array):
    # convert to np array
    np_bloom_array = np.array(bloom_array)
    return np.right_shift(np_bloom_array, 7)

def task(yearmonth):
    year, month = yearmonth
    folder_dir = "../Downloads/"
    end_date = datetime.date(year,month,1) + relativedelta(months=+1)
    curr_date = datetime.date(year,month,1)

    init_array = np.zeros((18000, 36000))

    while curr_date <= end_date:
        folder_path = f"{curr_date.year}_daily_001grd/"
        formatted_date = curr_date.strftime("%Y%m%d")
        file_location = f"{formatted_date}.tif"
        print(init_array)
        try:
            dataset = gdal.Open(f"{folder_dir}{folder_path}{file_location}", gdal.GA_ReadOnly) 
            arr = dataset.GetRasterBand(1)
            arr = arr.ReadAsArray()
            arr = get_bloom_pixels(arr)
            init_array = init_array + arr
        except:
            print(f"no directory: {folder_dir}{folder_path}{file_location}")
        curr_date += datetime.timedelta(days=1)
        if curr_date.day == 1:
            key_date = curr_date - datetime.timedelta(days=1)
            dill.dump(init_array, file = open(f"big_boi{key_date.year}{key_date.month}.pickle", "wb"))
            print('dumped')
            init_array = np.zeros((18000, 36000))
    return 0

from multiprocessing.pool import Pool
if __name__ == '__main__':
    years = list(range(2014, 2021))
    months1 = list(range(1,7))
    months2 = list(range(7,13))
    for year in years:
        yearmonth1 = [(year, month) for month in months1]
        yearmonth2 = [(year, month) for month in months2]
        pool = Pool(6)
        for result in pool.map(task, yearmonth1):
            print(0)
        for result in pool.map(task, yearmonth2):
            print(0)

