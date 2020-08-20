import numpy as np

class ListManager:

    def check_bounds(lst, i, j):
        assert i >= 0 and i < len(lst)
        assert j >= 0 and j < len(lst)

    def replace(lst, i, item):
        lst[i] = item

    def swap(lst, i, j):
        ListManager.check_bounds(lst, i, j)
        spam = lst[i]
        lst[i] = lst[j]
        lst[j] = spam

    def move_to(lst, i, j):
        ListManager.check_bounds(lst, i, j)
        spam = lst[i]
        del lst[i]
        lst.insert(j, spam)

    def add_above(lst, indices, obj_constructor):
        indices.sort()
        for i in range(len(indices) - 1, -1, -1):
            lst.insert(indices[i], obj_constructor())
        indices = indices + np.array(range(1, len(indices) + 1))
        added = indices - 1
        return indices, added

    def add_below(lst, indices, obj_constructor):
        indices.sort()
        for i in range(len(indices) - 1, -1, -1):
            lst.insert(indices[i] + 1, obj_constructor())
        indices = indices + np.array(range(0, len(indices)))
        added = indices + 1
        return indices, added

    def move_up(lst, indices):
        indices.sort()
        if len(indices) > 0:
            first_index_to_process = 0
            unprocessable_length = 0
            while True:
                if (first_index_to_process >= len(lst)):
                    break
                if (first_index_to_process >= len(indices)):
                    break
                if (indices[first_index_to_process] != unprocessable_length):
                    break
                first_index_to_process = first_index_to_process + 1
                unprocessable_length = unprocessable_length + 1

            for i in range(first_index_to_process, len(indices)):
                ListManager.swap(lst, indices[i], indices[i] - 1)
                indices[i] = indices[i] - 1
        return indices

    def move_down(lst, indices):
        indices.sort()
        if (len(indices) > 0) & (len(indices) < len(lst)):
            last_index_to_process = len(indices) - 1
            unprocessable_length = len(lst) - 1
            while (last_index_to_process >= 0) \
                  & (indices[last_index_to_process] == unprocessable_length):
                last_index_to_process = last_index_to_process - 1
                unprocessable_length = unprocessable_length - 1

            for i in range(last_index_to_process, -1, -1):
                ListManager.swap(lst, indices[i], indices[i] + 1)
                indices[i] = indices[i] + 1
        return indices

    def move_to_top(lst, indices):
        if len(indices) > 0:
            indices.sort()
            for i in range(len(indices)):
                ListManager.move_to(lst, indices[i], i)
            indices = np.arange(0, len(indices))
        return indices

    def move_to_bottom(lst, indices):
        if len(indices) > 0:
            indices.sort()
            for i in range(len(indices) - 1, -1, -1):
                ListManager.move_to(lst, indices[i], len(lst) - (len(indices) - i))
            indices = np.arange(len(lst) - len(indices), len(lst))
        return indices
