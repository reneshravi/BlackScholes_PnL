import unittest
import numpy as np
from src.heatmap_funcs import dynamic_annotation_format

class TestHeatmapFunctions(unittest.TestCase):

    def test_dynamic_annotation_format(self):
        self.assertEqual(dynamic_annotation_format(1_500_000), "1.5M")
        self.assertEqual(dynamic_annotation_format(10_000), "10.0K")
        self.assertEqual(dynamic_annotation_format(250.5), "250.5")
        self.assertEqual(dynamic_annotation_format(-50), "-50.0")

    def test_heatmap_annotation_logic(self):
        # Create a sample data grid
        data = np.array([[100, 200], [300, -400]])
        annotations = [[dynamic_annotation_format(value) for value in row] for row in data]
        expected_annotations = [["100.0", "200.0"], ["300.0", "-400.0"]]
        self.assertEqual(annotations, expected_annotations)

if __name__ == "__main__":
    unittest.main()
