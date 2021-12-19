import numpy as np

a = [[1], [2], [3], [4], [5]] # a list
b = [[1], [2], [3], [4], [5]]
print('Type of a is ',type(a))

a_array = np.array(a, dtype=float) # convert list to np array of type X
b_array = np. array(b)
print('Type of a_array is ',type(a_array))

data = np.hstack((a_array, b_array))
print('Type of data is ',type(data))
# print(data)
print(np.shape(data))

data = np.concatenate((data,[[5, 3]]))
# print(data)
print(np.shape(data))
print('Type of data is ',type(data))


# initalize empty array
data = np.array([], dtype=float).reshape(0,2)
print('data = ', data)
for i in range(3):
    # data = np.concatenate((data,[[i, i]]),axis=0) # use concatenate
    data = np.vstack([data, [[i, -i]]])              # or use vstack
print(data)
print(data.shape)

print(data[:,1])
