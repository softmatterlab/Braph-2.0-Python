import unittest
import numpy as np
from braphy.atlas.brain_region import BrainRegion
from braphy.atlas.brain_atlas import BrainAtlas
from braphy.test.test_utility import TestUtility

class TestBrainAtlas(TestUtility):
    def test(self):
        br1 = BrainRegion('BR1', 'brain region 1', 1, 11, 111)
        br2 = BrainRegion('BR2', 'brain region 2', 2, 22, 222)
        br3 = BrainRegion('BR3', 'brain region 3', 3, 33, 333)
        br4 = BrainRegion('BR4', 'brain region 4', 4, 44, 444)
        br5 = BrainRegion('BR5', 'brain region 5', 5, 55, 555)
        br6 = BrainRegion('BR6', 'brain region 6', 6, 66, 666)
        br7 = BrainRegion('BR7', 'brain region 7', 7, 77, 777)
        br8 = BrainRegion('BR8', 'brain region 8', 8, 88, 888)
        br9 = BrainRegion('BR9', 'brain region 9', 9, 99, 999)
        brain_regions = [br1, br2, br3, br4, br5, br6, br7, br8, br9]
        atlas = BrainAtlas('atlas', brain_regions)

        self.assertTrue(atlas.brain_region_number() == 9)
        self.assertTrue(atlas.get_brain_region(2) == br3)

        labels = ['BR1', 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'BR8', 'BR9']
        self.assertSequenceEqual(atlas.get_brain_region_labels().tolist(), labels)

        names = ['brain region 1', 'brain region 2', 'brain region 3', 'brain region 4',
                 'brain region 5', 'brain region 6', 'brain region 7', 'brain region 8',
                 'brain region 9']
        self.assertSequenceEqual(atlas.get_brain_region_names().tolist(), names)

        x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertSequenceEqual(atlas.get_brain_region_xs().tolist(), x)
        y = [11, 22, 33, 44, 55, 66, 77, 88, 99]
        self.assertSequenceEqual(atlas.get_brain_region_ys().tolist(), y)
        z = [111, 222, 333, 444, 555, 666, 777, 888, 999]
        self.assertSequenceEqual(atlas.get_brain_region_zs().tolist(), z)
        positions = np.column_stack((x, y, z))
        self.assertMatrixEqual(atlas.get_brain_region_positions(), positions)

        atlas.add_brain_region(br1, 3)
        atlas.remove_brain_region(6)
        atlas.remove_brain_regions(np.array([1, 8]))
        atlas.replace_brain_region(4, br9)
        atlas.invert_brain_regions(2, 5)
        self.assertSequenceEqual(atlas.get_brain_region_labels().tolist(), ['BR1', 'BR3', 'BR7', 'BR4', 'BR9', 'BR1', 'BR8'])
        
        atlas.move_to_brain_region(6, 6)
        atlas.move_to_brain_region(6, 0)
        selected, added = atlas.add_above_brain_regions(np.array([0, 4]))
        self.assertSequenceEqual(atlas.get_brain_region_labels().tolist(), ['BR', 'BR8', 'BR1', 'BR3', 'BR7', 'BR', 'BR4', 'BR9', 'BR1'])
        self.assertSequenceEqual(selected.tolist(), [1, 6])
        self.assertSequenceEqual(added.tolist(), [0, 5])

        selected, added = atlas.add_below_brain_regions(np.array([2, 8]))
        self.assertSequenceEqual(atlas.get_brain_region_labels().tolist(), ['BR', 'BR8', 'BR1', 'BR', 'BR3', 'BR7', 'BR', 'BR4', 'BR9', 'BR1', 'BR'])
        self.assertSequenceEqual(selected.tolist(), [2, 9])
        self.assertSequenceEqual(added.tolist(), [3, 10])

        atlas.remove_brain_regions(np.array([0, 1, 2, 3, 6, 10]))
        atlas.move_up_brain_regions(np.array([0, 2]))
        atlas.move_down_brain_regions(np.array([0, 3, 4]))
        selected = atlas.move_down_brain_regions(np.array([0, 1, 2, 3, 4]))
        self.assertSequenceEqual(atlas.get_brain_region_labels().tolist(), ['BR4', 'BR3', 'BR7', 'BR9', 'BR1'])
        self.assertSequenceEqual(selected.tolist(), [0, 1, 2, 3, 4])

        atlas.move_to_top_brain_regions(np.array([2, 4]))
        selected = atlas.move_to_bottom_brain_regions(np.array([1, 2, 4]))
        self.assertSequenceEqual(atlas.get_brain_region_labels().tolist(), ['BR7', 'BR3', 'BR1', 'BR4', 'BR9'])
        self.assertSequenceEqual(selected.tolist(), [2, 3, 4])


if __name__ == '__main__':
    unittest.main()
