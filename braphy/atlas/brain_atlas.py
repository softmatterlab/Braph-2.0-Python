from braphy.atlas.brain_region import BrainRegion
from braphy.utility.helper_functions import ListManager as lm
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

class BrainAtlas():
    def __init__(self, mesh_file = '', name = 'Atlas', brain_regions = None):
        self.mesh_file = mesh_file
        self.name = name
        self.brain_regions = brain_regions if brain_regions else []
        self.new_brain_regions_added = len(self.brain_regions)

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

    def new_brain_region(self):
        unique = False
        while not unique:
            self.new_brain_regions_added += 1
            label = "BR_{}".format(self.new_brain_regions_added)
            name = "brain_region_{}".format(self.new_brain_regions_added)
            unique = True
            for region in self.brain_regions:
                if region.label == label or region.name == name:
                    unique = False
        return BrainRegion(label = label, name = name)

    def add_brain_region(self, br = None, i = None):
        if i == None:
            i = len(self.brain_regions)
        if br == None:
            br = self.new_brain_region()
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
        lm.swap(self.brain_regions, i, j)

    def move_to_brain_region(self, i, j):
        lm.move_to(self.brain_regions, i, j)

    def add_above_brain_regions(self, selected):
        return lm.add_above(self.brain_regions, selected, self.new_brain_region)

    def add_below_brain_regions(self, selected):
        return lm.add_below(self.brain_regions, selected, self.new_brain_region)

    def move_up_brain_regions(self, selected):
        return lm.move_up(self.brain_regions, selected)

    def move_down_brain_regions(self, selected):
        return lm.move_down(self.brain_regions, selected)

    def move_to_top_brain_regions(self, selected):
        return lm.move_to_top(self.brain_regions, selected)

    def move_to_bottom_brain_regions(self, selected):
        return lm.move_to_bottom(self.brain_regions, selected)

    def load_from_txt(self, file_path = '', file_name = ''):
        with open(file_path + file_name, 'r') as f:
            success = False
            for i, line in enumerate(f):
                line = line.split('\t')
                if i == 0:
                    self.name = line[0].strip()
                    self.mesh_file = line[1].strip()
                    continue
                success = True
                assert len(line) >= 5 and len(line) <= 7, "Invalid text file"
                label = line[0]
                name = line[1]
                x = float(line[2])
                y = float(line[3])
                z = float(line[4])
                self.brain_regions.append(BrainRegion(label, name, x, y, z))
            assert success == True, "Could not find any brain regions in file"

    def load_from_xlsx(self, file_path = '', file_name = ''):
        try:
            data = pd.read_excel(file_path + file_name)
            data.iloc[:,0] = data.iloc[:,0].str.strip().str.replace('  ', ' ')
            data.iloc[:,1] = data.iloc[:,1].str.strip().str.replace('  ', ' ')
            self.name = data.columns[0].strip()
            self.mesh_file = data.columns[1].strip()
            br = np.array( data.apply(lambda x: BrainRegion(x[0], x[1], x[2], x[3], x[4]),
                                    axis = 1)).tolist()
            self.brain_regions.extend(br)
        except:
            raise Exception("Invalid file")

    def load_from_xml(self, file_path = '', file_name = ''):
        with open(file_path + file_name, 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            atlas = root.find('BrainAtlas')
            assert atlas != None, "Could not find atlas in file"
            self.name = atlas.attrib['name'].strip()
            self.mesh_file = atlas.attrib['brainsurf'].strip()
            assert root.find('BrainAtlas/BrainRegion') != None, "Could not find any brain regions in file"
            for brain_region in root.findall('BrainAtlas/BrainRegion'):
                br = brain_region.attrib
                for key in ['label', 'name', 'x', 'y', 'z']:
                    assert key in br.keys(), "{} missing from brain region".format(key)
                label = br['label'].replace('  ', ' ').strip()
                name = br['name'].replace('  ', ' ').strip()
                x = float(br['x'])
                y = float(br['y'])
                z = float(br['z'])
                self.brain_regions.append(BrainRegion(label = label, name = name, x = x, y = y, z = z))

    def __str__(self):
        s = "{}\t{}\n".format(self.name, self.mesh_file)
        for region in self.brain_regions:
            s = s + str(region)
        return s

    def save_to_txt(self, file_name):
        with open(file_name, 'w') as f:
            f.write(str(self))

    def str_xml(self):
        s = "<xml>\n  <BrainAtlas brainsurf=\"{}\" name=\"{}\">\n".format(self.mesh_file, self.name)
        for region in self.brain_regions:
            s = s + "    {}\n".format(region.str_xml())
        s = s + "  </BrainAtlas>\n</xml>"
        return s

    def save_to_xml(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.str_xml())

    def save_to_xlsx(self, file_name):
        labels = self.get_brain_region_labels()
        names = self.get_brain_region_names()
        x = self.get_brain_region_xs()
        y = self.get_brain_region_ys()
        z = self.get_brain_region_zs()
        data = {self.name: labels, self.mesh_file: names, ' ': x, '  ': y, '   ': z}
        df = pd.DataFrame.from_dict(data)
        with open(file_name, 'w') as f:
            df.to_excel(file_name, index = None, columns = None)

    def to_file(self, atlas_file):
        d = {}
        d['atlas'] = self.to_dict()
        with open(atlas_file, 'w') as f:
            json.dump(d, f, sort_keys=True, indent=4)

    def to_dict(self):
        d = {}
        d['mesh_file'] = self.mesh_file
        d['name'] = self.name
        d['brain_regions'] = []
        for brain_region in self.brain_regions:
            d['brain_regions'].append(brain_region.to_dict())
        return d

    def from_file(self, atlas_file):
        with open(atlas_file, 'r') as f:
            d = json.load(f)
        return BrainAtlas.from_dict(d['atlas'])

    def from_dict(d):
        brain_regions = []
        for brain_region in d['brain_regions']:
            brain_regions.append(BrainRegion.from_dict(brain_region))
        return BrainAtlas(mesh_file = d['mesh_file'], name = d['name'], brain_regions = brain_regions)
