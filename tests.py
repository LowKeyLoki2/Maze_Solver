import unittest
from graphics import * 
    

class MazeTests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_rows,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_cols,
        )

    def test_cell_default_walls(self):
        cell = Cell()
        self.assertTrue(cell.has_left_wall)
        self.assertTrue(cell.has_right_wall)
        self.assertTrue(cell.has_top_wall)
        self.assertTrue(cell.has_bottom_wall)

    def test_cell_coordinates_after_draw(self):
        cell = Cell()
        cell.draw(0, 10, 0, 10)
        self.assertEqual(cell.x1, 0)
        self.assertEqual(cell.x2, 10)
        self.assertEqual(cell.y1, 0)
        self.assertEqual(cell.y2, 10)

    def test_maze_cell_draw_positions(self):
        maze = Maze(0, 0, 2, 2, 10, 10)
        cell = maze.cells[1][1]
        # Bottom right cell should have these coordinates:
        self.assertEqual(cell.x1, 10)
        self.assertEqual(cell.x2, 20)
        self.assertEqual(cell.y1, 10)
        self.assertEqual(cell.y2, 20)

    def test_maze_draw_cell_does_not_crash(self):
        maze = Maze(0, 0, 3, 3, 10, 10)
        try:
            maze.draw_cell(2, 2)
        except Exception as e:
            self.fail(f"draw_cell raised an exception: {e}")

    def setUp(self):
        self.win = Window(200, 200)
        self.num_rows = 4
        self.num_cols = 3
        self.cell_size = 20
        self.maze = Maze(0, 0, self.num_rows, self.num_cols, self.cell_size, self.cell_size, self.win)

    def test_maze_dimensions(self):
        self.assertEqual(len(self.maze.cells), self.num_rows)
        self.assertEqual(len(self.maze.cells[0]), self.num_cols)

    def test_all_cells_have_all_walls_by_default(self):
        for row in self.maze.cells:
            for cell in row:
                self.assertTrue(cell.has_left_wall)
                self.assertTrue(cell.has_right_wall)
                self.assertTrue(cell.has_top_wall)
                self.assertTrue(cell.has_bottom_wall)

    def test_cell_coordinates_are_set_correctly(self):
        cell = self.maze.cells[1][1]  # Row 1, Column 1
        expected_x1 = 1 * self.cell_size
        expected_y1 = 1 * self.cell_size
        expected_x2 = expected_x1 + self.cell_size
        expected_y2 = expected_y1 + self.cell_size

        self.assertEqual(cell.x1, expected_x1)
        self.assertEqual(cell.y1, expected_y1)
        self.assertEqual(cell.x2, expected_x2)
        self.assertEqual(cell.y2, expected_y2)

    def test_draw_move_between_cells(self):
        c1 = self.maze.cells[0][0]
        c2 = self.maze.cells[0][1]

        try:
            c1.draw_move(c2)  # Should not raise
        except Exception as e:
            self.fail(f"draw_move() raised an exception: {e}")

    def test_animate_method_executes(self):
        try:
            self.maze.animate()  # Should not raise
        except Exception as e:
            self.fail(f"animate() raised an exception: {e}")

    def test_remove_wall(self):
        cell = Cell()
        cell.has_top_wall = False
        self.assertFalse(cell.has_top_wall)

    def test_draw_move_undo(self):
        c1 = self.maze.cells[0][0]
        c2 = self.maze.cells[0][1]
        try:
            c1.draw_move(c2, undo=True)
        except Exception as e:
            self.fail(f"draw_move with undo=True raised an exception: {e}")

    def test_break_entrance_and_exit_removes_correct_walls(self):
        self.maze.break_entrance_and_exit()

        entrance_cell = self.maze.cells[0][0]
        exit_cell = self.maze.cells[self.num_rows - 1][self.num_cols - 1]

        self.assertFalse(
            entrance_cell.has_top_wall,
            "Entrance cell should have top wall removed"
        )
        self.assertFalse(
            exit_cell.has_bottom_wall,
            "Exit cell should have bottom wall removed"
        )

    def test_break_wall_marks_cells_as_visited(self):
        maze = Maze(0, 0, 3, 3, 20, 20)
        maze.break_wall(0, 0)

        for row in maze.cells:
            for cell in row:
                self.assertTrue(cell.visited, "Cell was not visited during maze generation")

    def test_break_wall_removes_internal_walls(self):
        maze = Maze(0, 0, 3, 3, 20, 20)
        maze.break_wall(0, 0)

        # Every cell must be accessible, so each should have at least one wall removed
        has_some_removed_wall = any(
            not (cell.has_top_wall and cell.has_bottom_wall and cell.has_left_wall and cell.has_right_wall)
            for row in maze.cells for cell in row
        )
        self.assertTrue(has_some_removed_wall, "No internal walls were removed")

    def test_break_wall_preserves_outer_frame(self):
        maze = Maze(0, 0, 3, 3, 20, 20)
        maze.break_wall(0, 0)

        # Ensure outer edges aren't opened unless it's entrance or exit
        for i in range(3):
            self.assertTrue(maze.cells[0][i].has_top_wall or (i == 0), "Top wall removed unexpectedly")
            self.assertTrue(maze.cells[2][i].has_bottom_wall or (i == 2), "Bottom wall removed unexpectedly")
            self.assertTrue(maze.cells[i][0].has_left_wall or (i == 0), "Left wall removed unexpectedly")
            self.assertTrue(maze.cells[i][2].has_right_wall or (i == 2), "Right wall removed unexpectedly")

    def test_reset_cells_visited(self):
        # Mark all cells as visited
        for row in self.maze.cells:
            for cell in row:
                cell.visited = True

        # Call the method
        self.maze.reset_cells_visited()

        # Assert all cells are now unvisited
        for row in self.maze.cells:
            for cell in row:
                self.assertFalse(cell.visited, "reset_cells_visited failed to reset visited flag")



if __name__ == "__main__":
    unittest.main()