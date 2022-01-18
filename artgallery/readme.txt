To avoid a race condition where the xy data of a line are not of the same length because the line is updated while being plotted the following changes must be made to the line method in the Line2D NumPy class defined in lines.py.
replaced:
self._xy = np.column_stack(np.broadcast_arrays(x, y)).astype(float)
with:
if x.size != y.size:
   logging.warning('line xy ...')
   minl= min(x.size, y.size)
   self._xy = np.column_stack(np.broadcast_arrays(x[:minl], y[:minl])).astype(float)
else:
   self._xy = np.column_stack(np.broadcast_arrays(x, y)).astype(float)
 