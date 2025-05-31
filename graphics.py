from tkinter import ttk, Canvas, BOTH
import tkinter as tk
import time

class Window:
    def __init__(self, width, height, master):
        self.width = width
        self.height = height
        self.root = master
        self.root.title("Maze Solver")
        # Main frame: left controls, right canvas
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Left control panel
        self.ctrl_panel = ttk.Frame(self.frame, padding=10)
        self.ctrl_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Right canvas panel
        self.canvas_panel = ttk.Frame(self.frame)
        self.canvas_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.canvas_panel, width=width, height=height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.close)
    
    def sleep(self, seconds=0.05):
        if self.running:
            time.sleep(seconds)
    
    def redraw(self):
        if self.running:   
            self.root.update_idletasks()
            self.root.update()
   
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print ("Window Closed")

    
    def close(self):
        self.running = False
        self.root.destroy()

    def draw_line(self, line, fill_color):
        if self.running and self.canvas.winfo_exists():
            line.draw(self.canvas, fill_color)


        

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, color="black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=color, width=2)
            

         
class Cell:
    def __init__(self, window=None):
        self.window = window
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = -1
        self.x2 = -1
        self.y1 = -1
        self.y2 = -1
        self.visited = False

    def draw(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        if self.has_left_wall:
            p1 = Point(self.x1, self.y1)
            p2 = Point(self.x1, self.y2)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "black")
        else:
            p1 = Point(self.x1, self.y1)
            p2 = Point(self.x1, self.y2)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "white")

        if self.has_right_wall:
            p1 = Point(self.x2, self.y1)
            p2 = Point(self.x2, self.y2)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "black")
        else:
            p1 = Point(self.x2, self.y1)
            p2 = Point(self.x2, self.y2)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "white")

        if self.has_top_wall:
            p1 = Point(self.x1, self.y1)
            p2 = Point(self.x2, self.y1)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "black")
        else:
            p1 = Point(self.x1, self.y1)
            p2 = Point(self.x2, self.y1)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "white")

        if self.has_bottom_wall:
            p1 = Point(self.x1, self.y2)
            p2 = Point(self.x2, self.y2)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "black")
        else:
            p1 = Point(self.x1, self.y2)
            p2 = Point(self.x2, self.y2)
            if self.window != None:
                self.window.draw_line(Line(p1, p2), "white")

    def draw_move(self, to_cell, undo=False):
        x1 = (self.x1 + self.x2) // 2
        y1 = (self.y1 + self.y2) // 2
        x2 = (to_cell.x1 + to_cell.x2) // 2
        y2 = (to_cell.y1 + to_cell.y2) // 2

        color = "white" if undo else "red"

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        if self.window != None:
            self.window.draw_line(Line(p1, p2), color)

    


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
        animation_delay=0.05
        
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.seed = seed
        self.animation_delay = animation_delay
        self.create_cells()
        if self.seed is not None:
            import random
            random.seed(self.seed)
    
    def create_cells(self):
        if self.win and self.win.canvas.winfo_exists():
            self.win.canvas.delete("all")
        self.cells = []
        self.win.canvas.delete("all")  # Clear previous maze drawing
        for row in range(self.num_rows):
            row_cells = []
            for col in range(self.num_cols):
                cell = Cell(self.win)
                x1 = self.x1 + col * self.cell_size_x
                x2 = x1 + self.cell_size_x
                y1 = self.y1 + row * self.cell_size_y
                y2 = y1 + self.cell_size_y
                cell.draw(x1, x2, y1, y2)
                row_cells.append(cell)
                self.animate()
            self.cells.append(row_cells)

    def draw_cell(self, i, j):
        cell = self.cells[j][i]
        x1 = self.x1 + i * self.cell_size_x
        x2 = x1 + self.cell_size_x
        y1 = self.y1 + j * self.cell_size_y
        y2 = y1 + self.cell_size_y
        cell.draw(x1, x2, y1, y2)
        

    def animate(self):
        if self.win != None:
            self.win.redraw()
            self.win.sleep(self.animation_delay)


    def break_entrance_and_exit(self):
        entrance_cell = self.cells[0][0]
        entrance_cell.has_top_wall = False
        entrance_cell.draw(entrance_cell.x1, entrance_cell.x2, entrance_cell.y1, entrance_cell.y2)

        exit_cell = self.cells[self.num_rows - 1][self.num_cols - 1]
        exit_cell.has_bottom_wall = False
        exit_cell.draw(exit_cell.x1, exit_cell.x2, exit_cell.y1, exit_cell.y2)

    def break_wall(self, i, j):
        self.cells[i][j].visited = True

        directions = []
        if i > 0 and not self.cells[i - 1][j].visited:
            directions.append((-1, 0))  # Up
        if i < self.num_rows - 1 and not self.cells[i + 1][j].visited:
            directions.append((1, 0))   # Down
        if j > 0 and not self.cells[i][j - 1].visited:
            directions.append((0, -1))  # Left
        if j < self.num_cols - 1 and not self.cells[i][j + 1].visited:
            directions.append((0, 1))   # Right

        while directions:
            # Use seed if you want repeatability
            import random
            if self.seed is not None:
                random.seed(self.seed)
                self.seed += 1
            di, dj = random.choice(directions)
            directions.remove((di, dj))
            ni, nj = i + di, j + dj

            if not self.cells[ni][nj].visited:
                # Remove walls between cells
                if di == -1:
                    self.cells[i][j].has_top_wall = False
                    self.cells[ni][nj].has_bottom_wall = False
                elif di == 1:
                    self.cells[i][j].has_bottom_wall = False
                    self.cells[ni][nj].has_top_wall = False
                elif dj == -1:
                    self.cells[i][j].has_left_wall = False
                    self.cells[ni][nj].has_right_wall = False
                elif dj == 1:
                    self.cells[i][j].has_right_wall = False
                    self.cells[ni][nj].has_left_wall = False

                self.draw_cell(j, i)
                self.animate()

                self.break_wall(ni, nj)

    def reset_cells_visited(self):
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        self.reset_cells_visited()
        self.prev_i, self.prev_j = 0, 0
        self.solve_r(0, 0)

    def solve_r(self, i, j, prev_cell=None):
        if i < 0 or i >= self.num_rows or j < 0 or j >= self.num_cols:
            return False

        cell = self.cells[i][j]
        if cell.visited:
            return False

        cell.visited = True
        if prev_cell is not None:
            prev_cell.draw_move(cell, undo=False)
        self.animate()

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        # Try each direction only if no wall and not visited
        if i > 0 and not cell.has_top_wall and not self.cells[i-1][j].visited:
            if self.solve_r(i - 1, j, cell):
                return True

        if i < self.num_rows - 1 and not cell.has_bottom_wall and not self.cells[i+1][j].visited:
            if self.solve_r(i + 1, j, cell):
                return True

        if j > 0 and not cell.has_left_wall and not self.cells[i][j-1].visited:
            if self.solve_r(i, j - 1, cell):
                return True

        if j < self.num_cols - 1 and not cell.has_right_wall and not self.cells[i][j+1].visited:
            if self.solve_r(i, j + 1, cell):
                return True

        # Backtrack line undo
        if prev_cell is not None:
            prev_cell.draw_move(cell, undo=True)
        self.animate()
        return False

class MazeApp:
    def __init__(self, master):
        self.master = master

        self.win_width = 600
        self.win_height = 600

        self.window = Window(self.win_width, self.win_height, master)

        self.controls = {}
        self.create_controls()

        # Initial maze params
        self.num_rows = 20  
        self.num_cols = 20
        self.cell_size = 25
        self.animation_delay = 0.01
        self.seed = None

        self.maze = None

        self.generate_and_solve()

    def create_controls(self):
        ctrl = self.window.ctrl_panel

        # Rows
        ttk.Label(ctrl, text="Rows:").pack(anchor='w', pady=2)
        self.controls['rows'] = ttk.Entry(ctrl)
        self.controls['rows'].pack(anchor='w', pady=2)
        self.controls['rows'].insert(0, "20")

        # Columns
        ttk.Label(ctrl, text="Columns:").pack(anchor='w', pady=2)
        self.controls['cols'] = ttk.Entry(ctrl)
        self.controls['cols'].pack(anchor='w', pady=2)
        self.controls['cols'].insert(0, "20")

        # Cell size
        ttk.Label(ctrl, text="Cell size (px):").pack(anchor='w', pady=2)
        self.controls['cell_size'] = ttk.Entry(ctrl)
        self.controls['cell_size'].pack(anchor='w', pady=2)
        self.controls['cell_size'].insert(0, "25")

        # Animation delay
        ttk.Label(ctrl, text="Animation delay (sec):").pack(anchor='w', pady=2)
        self.controls['delay'] = ttk.Entry(ctrl)
        self.controls['delay'].pack(anchor='w', pady=2)
        self.controls['delay'].insert(0, "0.01")

        # Generate & Solve Button
        self.generate_btn = ttk.Button(ctrl, text="Generate & Solve", command=self.generate_and_solve)
        self.generate_btn.pack(pady=10, fill=tk.X)

    def generate_and_solve(self):
        # Read and validate inputs
        try:
            rows = int(self.controls['rows'].get())
            cols = int(self.controls['cols'].get())
            cell_size = int(self.controls['cell_size'].get())
            delay = float(self.controls['delay'].get())
        except ValueError:
            print("Invalid input(s). Please enter valid integers/floats.")
            return

        # Update params
        self.num_rows = max(2, min(rows, 50))
        self.num_cols = max(2, min(cols, 50))
        self.cell_size = max(10, min(cell_size, 100))
        self.animation_delay = max(0, min(delay, 1))

        # Create maze with new params
        self.maze = Maze(
            x1=10, y1=10,
            num_rows=self.num_rows,
            num_cols=self.num_cols,
            cell_size_x=self.cell_size,
            cell_size_y=self.cell_size,
            win=self.window,
            seed=self.seed,
            animation_delay=self.animation_delay
        )

        self.maze.break_entrance_and_exit()
        self.maze.break_wall(0, 0)
        self.maze.solve()

def main():
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()