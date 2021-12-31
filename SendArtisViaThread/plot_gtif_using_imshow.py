import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# https://gist.github.com/jackieleng/552349f3412472a3702b8d0d706600a4

# import cartopy.crs as ccrs
import rasterio


# ax = plt.axes(projection=ccrs.PlateCarree())
# # ax.set_global()
# ax.set_extent((103, 104, 0.8, 1.5), crs=ccrs.PlateCarree())
# ax.coastlines()

# from https://medium.com/the-barometer/read-and-plot-geotiff-in-python-xarray-cartopy-fd48faf1c503
# d = rasterio.open(b)
d = rasterio.open('Stennis_QW.tif')
fig = plt.figure()
ax = fig.add_subplot(xlim=(0, 2), ylim=(-1.1, 1.1))
# ny, nx = d.shape
# xs, ys = np.meshgrid(np.arange(nx), np.arange(ny)) * d.transform
zs = d.read(1)
vmin, vmax = np.min(zs), np.max(zs)
# mesh = ax.pcolormesh(xs, ys, zs, transform=ccrs.PlateCarree(),
#                      shading='nearest', vmin=vmin, vmax=vmax)
mesh = ax.imshow(
    zs, origin='upper', extent=(d.bounds.left, d.bounds.right, d.bounds.bottom, d.bounds.top),
    transform=ccrs.PlateCarree(),
    vmin=vmin, vmax=vmax
)



# x = np.linspace(-80, 80)
# xs, ys = np.meshgrid(2 * x + 180, x)
# zs = xs + ys
# vmin, vmax = np.min(zs), np.max(zs)
# mesh = ax.pcolormesh(xs, ys, np.ones_like(zs), transform=ccrs.PlateCarree(),
#                      shading='auto', vmin=vmin, vmax=vmax)

# Data from https://aster.geogrid.org/ASTER/fetchL3A/ASTB210828033024.tar.bz2
files = [
    './2108280330242108299006/data1.l3a.demzs.tif',
    './2108280330242108299006/data1.l3a.vnir1.tif',
    './2108280330242108299006/data1.l3a.vnir2.tif',
    './2108280330242108299006/data1.l3a.vnir3n.tif',
]


def update_mesh(i):
#     mesh.set_array(zs.ravel() * t)
    d = rasterio.open(files[i])
    zs = d.read(1)
    zs = np.ma.masked_where((zs == 0) | (zs == -9999), zs)
    mesh.set_array(zs)
    return mesh,


ts = list(range(len(files)))
# Go back to the start to make it a smooth repeat
# ts += ts[::-1]
ani = FuncAnimation(fig, update_mesh, frames=ts,
                    interval=500, blit=True)
plt.close()
# from IPython.display import HTML
# HTML(ani.to_jshtml())
# plt.show()