import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.cluster.vq as scv
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import datetime
import dateutil.relativedelta as relativedelta
import dill

# def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
#     new_cmap = colors.LinearSegmentedColormap.from_list(
#         'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
#         cmap(np.linspace(minval, maxval, n)))
#     return new_cmap

def create_linear_slope(x_start, x_end, y_start, y_end, i):
    slope = y_end - y_start / (x_end - x_start)
    c = y_start - slope * x_start
    return (slope * i + c) / 2

def colormap2arr(arr,cmap):    
    # http://stackoverflow.com/questions/3720840/how-to-reverse-color-map-image-to-scalar-values/3722674#3722674
    # gradient=cmap(np.apply_along_axis(func, 0,np.linspace(0.0,10.0,100)))
    gradient=cmap(np.linspace(0.0,1.0,1000))

    # Reshape arr to something like (240*240, 4), all the 4-tuples in a long list...
    arr2=arr.reshape((arr.shape[0]*arr.shape[1],arr.shape[2]))
    print(arr2.shape)

    # Use vector quantization to shift the values in arr2 to the nearest point in
    # the code book (gradient).
    code,dist=scv.vq(arr2,gradient)
    print(code.shape)

    # code is an array of length arr2 (240*240), holding the code book index for
    # each observation. (arr2 are the "observations".)
    # Scale the values so they are from 0 to 1.
    print(code.max(),code.min())
    values=code.astype('float')/gradient.shape[0]
    non_zero = values[values != 0]
    range_of_x = non_zero.max() - non_zero.min()
    for index, i in enumerate(values):
        if i == 0:
            continue
        else:
            i = (i - non_zero.min()) / range_of_x
            # 0, 0.05, 0.1, 0.2, 0.5, 2, 5, 10, 20, 100, 150
            if i <= 0.1:
                values[index] = create_linear_slope(0, 0.1, 0, 0.05)
            elif i <= 0.2:
                values[index] = create_linear_slope(0.1, 0.2, 0.05, 0.1)
            elif i <= 0.3:
                values[index] = create_linear_slope(0.2, 0.3, 0.1, 0.2)
            elif i <= 0.4:
                values[index] = create_linear_slope(0.3, 0.4, 0.2, 0.5)
            elif i <= 0.5:
                values[index] = create_linear_slope(0.4, 0.5, 0.5, 2)
            elif i <= 0.6:
                values[index] = create_linear_slope(0.5, 0.6, 2, 5)
            elif i <= 0.7:
                values[index] = create_linear_slope(0.6, 0.7, 5, 10)
            elif i <= 0.8:
                values[index] = create_linear_slope(0.7, 0.8, 10, 20)
            elif i <= 0.9:
                values[index] = create_linear_slope(0.8, 0.9, 20, 100)
            else:
                values[index] = create_linear_slope(0.9, 1.0, 100, 700)

    # Reshape values back to (240,240)
    values=values.reshape(1800, 3600)
    values=values[::-1]
    return values

def task(year):
    # starting date
    curr_date = datetime.date(year,1,1)
    # end date
    end_date = datetime.date(year,12,1)
    # read png file
    arr = plt.imread(f'{curr_date}_10km_density.png')
    values = colormap2arr(arr, cm.get_cmap('jet'))
    while curr_date < end_date:
        curr_date += relativedelta.relativedelta(months=1)
        try:
            arr = plt.imread(f'{curr_date}_10km_density.png')
        except:
            print(f'no file: {curr_date}_10km_density.png')
            curr_date += relativedelta.relativedelta(months=1)
        values += colormap2arr(arr, cm.get_cmap('jet'))
    dill.dump(values, file = open(f"shipping_log_scaled_{year}.pickle", "wb"))


from multiprocessing.pool import Pool
if __name__ == '__main__':
    years = list(range(2011, 2021))
    pool = Pool(10)
    for result in pool.map(task, years):
        print(0)
