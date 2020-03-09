from braphy.atlas.brain_region import BrainRegion
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET 
class BrainAtlas():
    def __init__(self, name = 'Atlas', brain_regions = []):
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

    def add_brain_region(self, br = None, i = None):
        if i == None:
            i = len(self.brain_regions)
        if br == None:
            br = BrainRegion()
        self.brain_regions.insert(i, br)

    def remove_brain_region(self, i):
        del self.brain_regions[i]

    def remove_brain_regions(self, selected):
        new_selected = list(selected)
        for i in range(len(selected) - 1, -1, -1):
            del self.brain_regions[selected[i]]
            del new_selected[i]

        return np.array(new_selected)

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
            while True:
                if (first_index_to_process >= self.brain_region_number()):
                    break
                if (first_index_to_process >= len(selected)):
                    break
                if (selected[first_index_to_process] != unprocessable_length):
                    break
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
            while (last_index_to_process >= 0) \
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

    def load_from_txt(self, file_path = '', file_name = ''):
        try:
            with open(file_path + file_name, 'r') as f:
                for i, line in enumerate(f):
                    line = line.split()
                    if i == 0:
                        continue
                    self.brain_regions.append(BrainRegion(label = line[0],
                                                        name = (' '.join(line[1:-5])).replace('  ', ' '),
                                                        x = float(line[-5]),
                                                        y = float(line[-4]),
                                                        z = float(line[-3])
                                                        ))
        except:
            print('Could not open file and add brain regions.')
    
    def load_from_xls(self, file_path = '', file_name = ''):
        
        try:
            data = pd.read_excel(file_path + file_name)
            
            # Remove leading, trailing and double whitespaces
            data.iloc[:,0] = data.iloc[:,0].str.strip().str.replace('  ', ' ')
            data.iloc[:,1] = data.iloc[:,1].str.strip().str.replace('  ', ' ')
            
            br = np.array( data.apply(lambda x: BrainRegion(x[0], x[1], x[2], x[3], x[4]),
                                    axis = 1)).tolist()
            self.brain_regions = br
        except: 
            print('Could not open file and add brain regions.')

    def load_from_xml(self, file_path = '', file_name = ''):
        try:
            with open(file_path + file_name, 'r') as f:
                tree = ET.parse(f)
                root = tree.getroot() 
                for brain_region in root.findall('BrainAtlas/BrainRegion'):
                    br = brain_region.attrib
                    self.brain_regions.append(BrainRegion(  label = br['label'].replace('  ', ' ').strip(),
                                                            name = br['name'].replace('  ', ' ').strip(),
                                                            x = float(br['x']),
                                                            y = float(br['y']),
                                                            z = float(br['z'])
                                                            ))
        except: 
            print('Could not open file and add brain regions.')

