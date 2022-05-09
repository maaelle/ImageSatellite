from osgeo import gdal,osr
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches



gdal.AllRegister()
driver = gdal.GetDriverByName('GTiff')
if driver is None:
    print('none')

dsB = gdal.Open("EO_Browser_images_uint16/2022-04-16-00_00_2022-04-16-23_59_Sentinel-2_L2A_B02_(Raw).tiff")
dsG = gdal.Open("EO_Browser_images_uint16/2022-04-16-00_00_2022-04-16-23_59_Sentinel-2_L2A_B03_(Raw).tiff")
dsR = gdal.Open("EO_Browser_images_uint16/2022-04-16-00_00_2022-04-16-23_59_Sentinel-2_L2A_B04_(Raw).tiff")

geo_transform = dsB.GetGeoTransform()
pixel_x = (989607.107  - geo_transform[0] )/geo_transform[1]
pixel_y = (5531649.79 - geo_transform[3])/(geo_transform[5])

Xkilometer = (998057.388 - 980906.829) /(geo_transform[1]*12)
Ykilometer = (5526244.271 - 5534852.991) /((geo_transform[5])*6)



b = dsB.GetRasterBand(1).ReadAsArray()
g = dsG.GetRasterBand(1).ReadAsArray()
r = dsR.GetRasterBand(1).ReadAsArray()


def scaleCCC(x):
    return ((x - np.nanpercentile(x, 2)) / (np.nanpercentile(x, 98) - np.nanpercentile(x, 2)))


rCCC = scaleCCC(r)
gCCC = scaleCCC(g)
bCCC = scaleCCC(b)


rgbCCC = np.dstack((rCCC, gCCC, bCCC))
fig, ax = plt.subplots()
ax.imshow(rgbCCC,interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth )
plt.xlim(0,1700)
plt.ylim(850,0)
ax.add_patch(
     patches.Rectangle(
        (pixel_x - Xkilometer, pixel_y - Ykilometer),
        2 * Xkilometer,
        2 * Ykilometer,
        edgecolor = 'red',
        fill=False
     ) )
plt.show()
plt.close()
