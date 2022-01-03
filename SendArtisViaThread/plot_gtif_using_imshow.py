""" 
Demonstrates how to plot a geotiff file using matplotlib's imshow function
"""
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import logging


__author__ = 'Gero Nootz'
__copyright__ = ''
__credits__ = ['', '']
__license__ = ''
__version__ = '1.0.0'
__date__ = '01/01/2022'
__maintainer__ = 'Gero Nootz'
__email__ = 'gero.nootz@usm.edu'
__status__ = 'Prototype'


with rasterio.open('stennis_QW.tif', driver='GTiff') as geotif:    
    print(geotif.bounds.left, geotif.bounds.right, geotif.bounds.bottom, geotif.bounds.top)
    print("bands: ", geotif.count)
    print(geotif.bounds)
    print('transform: ', geotif.transform)
    print('upper left corner: ', geotif.transform * (0, 0))
    print('lower right corner: ', geotif.transform * (geotif.width, geotif.height))
    print('x_range = ', geotif.bounds[2]-geotif.bounds[0])
    print('y_range = ', geotif.bounds[3]-geotif.bounds[1])

    rgb = np.dstack((geotif.read(1), geotif.read(2), geotif.read(3)))

    if geotif.crs != 'EPSG:4326':
        logging.error('the file origon is not EPSG:4326')
        raise Warning('the file origon of the geotif is not EPSG:4326')
        


fig = plt.figure()
ax = fig.add_subplot(xlim=(geotif.bounds.left, geotif.bounds.right),
                     ylim=(geotif.bounds.bottom, geotif.bounds.top))

im = ax.imshow(rgb, origin='upper', extent=(
    geotif.bounds.left, geotif.bounds.right, geotif.bounds.bottom, geotif.bounds.top), zorder=1)
plt.show()
