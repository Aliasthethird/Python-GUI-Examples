from collections import deque
import numpy as np

def data_history_list(data, n_history: int) -> list:
    """ 
    Returns the last n_history data elements supplied during 
    repeated calls. The data elements can be of any type.
    If the number of "historic" data elements is smaller
    than n_history only the available data is returned
    
    Author:
    G. Nootz - 01.18.2022
    """
    if not hasattr(data_history_list, 'data_history'):
        # initialize history_list
        data_history_list.n_history = n_history
        data_history_list.data_history = deque([data], n_history)
        return list(data_history_list.data_history)

    if  data_history_list.n_history != n_history:
        # change history length
        data_history_list.n_history = n_history
        data_history = list(data_history_list.data_history)
        data_history_list.data_history = deque(data_history, n_history)
        data_history_list.data_history.append(data)
        return list(data_history_list.data_history)
            
    data_history_list.data_history.append(data)
    return list(data_history_list.data_history)
    
if __name__ == '__main__':

    print(data_history_list([1, 3],3))
    print(data_history_list([2,3],3))
    print(data_history_list([3,3],3))
    print(data_history_list([4,3],3))
    print(data_history_list([5,7],7))
    print(data_history_list([6,7],7))
    print(data_history_list([7,2],2))
    my_array = np.array(data_history_list([1,3],3))
    print(my_array)

    print(data_history_list({'arg1': 'test', 'arg2': 1},2))
    # # fails since data is not of the same type
    # my_array = np.array(history_list([1,3],3))
    # print(my_array)