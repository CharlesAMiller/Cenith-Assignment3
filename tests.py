import unittest

from grid_game import calculate_relative_cost, find_path, InvalidGridException, is_in_bounds


class TestAssignment(unittest.TestCase):

    def test_relative_cost(self):
        start_stats = (100, 100)
        end_stats = (90, 90)
        expected = 18
        actual = calculate_relative_cost(start_stats, end_stats)
        self.assertEqual(expected, actual)

    def test_relative_cost_comparison(self):
        start_stats = (100, 100)
        end_stats = (50, 50)
        costs_1 = calculate_relative_cost(start_stats, end_stats)

        start_stats_2 = (50, 50)
        end_stats_2 = (25, 25)
        costs_2 = calculate_relative_cost(start_stats_2, end_stats_2)

        start_stats_3 = (4, 4)
        end_stats_3 = (2, 2)
        costs_3 = calculate_relative_cost(start_stats_3, end_stats_3)

        self.assertEqual(costs_1, costs_2)
        self.assertEqual(costs_1, costs_3)

    def test_is_in_bounds(self):
        grid = [['E', 'E'],
                ['E', 'E']]
        self.assertTrue(is_in_bounds((0, 0), grid))
        self.assertTrue(is_in_bounds((1, 1), grid))
        self.assertFalse(is_in_bounds((-1, 0), grid))
        self.assertFalse(is_in_bounds((2, 0), grid))
        self.assertFalse(is_in_bounds((0, 2), grid))
        self.assertFalse(is_in_bounds((0, -1), grid))

    def test_find_path_invalid_grid(self):
        with self.assertRaises(InvalidGridException):
            find_path([['E', 'E'], ['E', 'E']])

    def test_find_path_no_start(self):
        with self.assertRaises(InvalidGridException):
            find_path([['E', 'E'], ['E', 'B']])

    def test_find_path_no_end(self):
        with self.assertRaises(InvalidGridException):
            find_path([['A', 'E'], ['E', 'E']])

    def test_find_path_simple_avoidable_hazard(self):
        grid = [['A', 'E'],
                ['L', 'B']]
        expected = ([(0, 0), (0, 1), (1, 1)], (200, 448))
        actual = find_path(grid)
        self.assertEqual(expected, actual)

    def test_no_valid_path_health_hazards(self):
        grid = [['A', 'L'],
                ['L', 'B']]
        expected = None
        actual = find_path(grid, health=1)
        self.assertEqual(expected, actual)

    def test_no_valid_path_exhaust_moves(self):
        grid = [['A', 'L'],
                ['L', 'B']]
        expected = None
        actual = find_path(grid, moves=1)
        self.assertEqual(expected, actual)

    def test_take_hazard_shortcut_if_exhaust_moves(self):
        grid = [['A', 'L', 'B'],
                ['M', 'M', 'M']]
        expected = ([(0, 0), (0, 1), (0, 2)], (150, 0))
        actual = find_path(grid, moves=11)
        self.assertEqual(expected, actual)

    def test_take_long_path_if_would_exhaust_health(self):
        grid = [['A', 'L', 'B'],
                ['E', 'E', 'E']]
        expected = ([(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)], (50, 446))
        actual = find_path(grid, health=50)
        self.assertEqual(expected, actual)

    def test_take_speeder_if_would_exhaust_moves(self):
        grid = [['A', 'E', 'E'],
                ['E', 'S', 'E'],
                ['E', 'E', 'B']]
        expected = ([(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)], (5, 0))
        actual = find_path(grid, moves=3, health=10)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
