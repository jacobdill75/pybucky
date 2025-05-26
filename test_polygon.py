import unittest
import numpy as np
from polygon import Polygon

class TestPolygon(unittest.TestCase):
    def test_triangle(self):
        triangle = Polygon([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        self.assertTrue(triangle.is_convex())
        self.assertTrue(triangle.has_consistent_winding())
        self.assertTrue(triangle.is_manifold())

    def test_quad(self):
        quad = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
        self.assertTrue(quad.is_convex())
        self.assertTrue(quad.has_consistent_winding())
        self.assertTrue(quad.is_manifold())

    def test_non_convex(self):
        concave = Polygon([[0, 0, 0], [2, 0, 0], [1, 1, 0], [2, 2, 0], [0, 2, 0]])
        self.assertFalse(concave.is_convex())

if __name__ == "__main__":
    unittest.main()

