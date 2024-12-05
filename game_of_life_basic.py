import numpy as np
import matplotlib.pyplot as plt

def init_life_state_1(n, m, p):
    """
    Generate an initial random subset of life cells (2D points).
    
    IN: 
        n, int: number of rows.
        m, int: number of columns.
        p, float: probability of a cell being alive.
    
    OUT:
        ndarray of shape (n, m), initial state of the cells where 1 represents alive, 0 represents dead.
    """
    # Generate a random grid of shape (n, m) with values from 0 to 1 and if the value is less than p, set the cell to 1 and otherwise 0
    return np.random.rand(n, m) < p


def draw_cell_background(x, y):
    plt.fill([x-0.5, x-0.5, x+0.5, x+0.5], [y-0.5, y+0.5, y+0.5, y-0.5], color='lightgray')


def draw_life_state_1(life_state):
    """
    Display the 2D positions of the selected collection of cells (2D points).
    IN:
        life_state, ndarray of shape (n, m): Initial state of the cells.
    OUT:
        None (it will plot the state using matplotlib).
    """
    n, m = life_state.shape
    
    plt.figure(figsize=(m/2, n/2))
    
    # Iterate over all cells and draw the background and alive cells
    for i in range(n):
        for j in range(m):
            draw_cell_background(j, i)
            if life_state[i, j]:  # If the cell is alive (value 1)
                plt.fill([j-0.5, j-0.5, j+0.5, j+0.5], [i-0.5, i+0.5, i+0.5, i-0.5], color='black')
    
    plt.xlim(-0.5, m-0.5)
    plt.ylim(n-0.5, -0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')  # Hide the axis for better visualization
    plt.show()

# Example usage:
n, m, p = 20, 30, 0.2  # 20 rows, 30 columns, 20% chance of being alive
life_state = init_life_state_1(n, m, p)
draw_life_state_1(life_state)

