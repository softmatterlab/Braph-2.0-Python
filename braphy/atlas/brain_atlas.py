from braphy.atlas.brain_region import BrainRegion
import numpy as np

class BrainAtlas():
    def __init__(self, name, brain_regions):
        self.name = name
        self.brain_regions = brain_regions

    def brain_region_number(self):
        return len(self.brain_regions)

    def get_brain_region(self, i):
        return self.brain_regions[i]

    def get_brain_region_labels(self):
        br_labels = np.zeros(self.brain_region_number()).astype(str)
        for i in range(self.brain_region_number()):
            br_labels[i] = self.get_brain_region(i).label
        return br_labels

    def get_brain_region_names(self):
        br_names = np.zeros(self.brain_region_number()).astype(str)
        for i in range(self.brain_region_number()):
            br_names[i] = self.get_brain_region(i).name
        return br_names

    def get_brain_region_xs(self):
        br_xs = np.zeros(self.brain_region_number())
        for i in range(self.brain_region_number()):
            br_xs[i] = self.get_brain_region(i).x
        return br_xs

    def get_brain_region_ys(self):
        br_ys = np.zeros(self.brain_region_number())
        for i in range(self.brain_region_number()):
            br_ys[i] = self.get_brain_region(i).y
        return br_ys

    def get_brain_region_zs(self):
        br_zs = np.zeros(self.brain_region_number())
        for i in range(self.brain_region_number()):
            br_zs[i] = self.get_brain_region(i).z
        return br_zs

    def get_brain_region_positions(self):
        br_positions = np.zeros((self.brain_region_number(), 3))
        for i in range(self.brain_region_number()):
            br_positions[i, :] = self.get_brain_region(i).get_position()
        return br_positions

    def add_brain_region(self, br, i):
        self.brain_regions.insert(i, br)

    def remove_brain_region(self, i):
        del self.brain_regions[i]

    def remove_brain_regions(self, selected):
        for i in range(len(selected) - 1, -1, -1):
            del self.brain_regions[selected[i]]
        selected = []
        return selected

    def replace_brain_region(self, i, br):
        self.brain_regions[i] = br

    def invert_brain_regions(self, i, j):
        if (i >= 0) & (i < self.brain_region_number()) & (j >= 0) & (j < self.brain_region_number()) & (i != j):
            br_i = self.get_brain_region(i)
            br_j = self.get_brain_region(j)
            self.replace_brain_region(i, br_j)
            self.replace_brain_region(j, br_i)

    def move_to_brain_region(self, i, j):
        if (i >= 0) & (i < self.brain_region_number()) & (j >= 0) & (j < self.brain_region_number()) & (i != j):
            br = self.get_brain_region(i)
            self.remove_brain_region(i)
            self.add_brain_region(br, j)

    def add_above_brain_regions(self, selected):
        for i in range(len(selected) - 1, -1, -1):
            self.add_brain_region(BrainRegion(), selected[i])
        selected = selected + np.array(range(1, len(selected) + 1))
        added = selected - 1
        return selected, added

    def add_below_brain_regions(self, selected):
        for i in range(len(selected) - 1, -1, -1):
            self.add_brain_region(BrainRegion(), selected[i] + 1)
        selected = selected + np.array(range(0, len(selected)))
        added = selected + 1
        return selected, added

    def move_up_brain_regions(self, selected):
        if len(selected) > 0:
            first_index_to_process = 0
            unprocessable_length = 0
            while first_index_to_process <= self.brain_region_number() \
                  & first_index_to_process <= len(selected) \
                  & selected[first_index_to_process] == unprocessable_length:
                first_index_to_process = first_index_to_process + 1
                unprocessable_length = unprocessable_length + 1

            for i in range(first_index_to_process, len(selected)):
                self.invert_brain_regions(selected[i], selected[i] - 1)
                selected[i] = selected[i] - 1
        return selected

    def move_down_brain_regions(self, selected):
        if (len(selected) > 0) & (len(selected) < self.brain_region_number()):
            last_index_to_process = len(selected) - 1
            unprocessable_length = self.brain_region_number() - 1
            while (last_index_to_process > 0) \
                  & (selected[last_index_to_process] == unprocessable_length):
                last_index_to_process = last_index_to_process - 1
                unprocessable_length = unprocessable_length - 1

            for i in range(last_index_to_process, -1, -1):
                self.invert_brain_regions(selected[i], selected[i] + 1)
                selected[i] = selected[i] + 1
        return selected

    def move_to_top_brain_regions(self, selected):
        if len(selected) > 0:
            for i in range(len(selected)):
                self.move_to_brain_region(selected[i], i)
            selected = np.arange(0, len(selected))
            return selected

    def move_to_bottom_brain_regions(self, selected):
        if len(selected) > 0:
            for i in range(len(selected) - 1, -1, -1):
                self.move_to_brain_region(selected[i], self.brain_region_number() - (len(selected) - i))
            selected = np.arange(self.brain_region_number() - len(selected), self.brain_region_number())
        return selected








