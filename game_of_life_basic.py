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
    
    # Add axis labels  
    plt.title('Game of Life')
    
    plt.axis('off')
    #add grid
    plt.grid(True)
    plt.show()

# Example usage 1.1:
n, m, p = 20, 30, 0.1  # 20 rows, 30 columns, 20% chance of being alive
life_state = init_life_state_1(n, m, p)
draw_life_state_1(life_state)

#helper function that returns the number of alive neighbors
def count_neighbors(i, j, life_state):
        n, m = life_state.shape
        #positions of neighbors relative to (i,j)
        neighbors = [(-1, -1), (-1, 0), (-1, 1),( 0, -1),( 0, 1),( 1, -1), ( 1, 0), ( 1, 1)]
        count = 0
        for di, dj in neighbors:
            ni, nj = i + di, j + dj
            # Check if the neighbor is within bounds and is alive
            if 0 <= ni < n and 0 <= nj < m:
                count += life_state[ni, nj]
        return count
    

def update_life_state_1(life_state, out_life_state=None):
    """
    For each cell, evaluate the update rules specified above to obtain its new state.
    
    IN: 
        life_state (ndarray of shape (n, m)): the current state of the grid.
        out_life_state (ndarray of shape (n, m), optional): a pre-allocated array for storing the next state of the cells. 
                                                            If None, a new array will be created.
    
    OUT:
        out_life_state (ndarray of shape (n, m)): the next state of the grid after applying the rules.
    """
    #dimensions of the life_state
    n, m = life_state.shape
    
    #create a new array with the same shape as life_state if out_life_state is None
    if out_life_state is None:
        out_life_state = np.zeros_like(life_state)
    
    # Update each cell in the grid based on the rules
    for i in range(n):
        for j in range(m):
            alive_neighbors = count_neighbors(i, j, life_state)
            #cell is alive, (i,j) = 1
            if life_state[i, j] == 1:
                if alive_neighbors == 2 or alive_neighbors == 3:
                    out_life_state[i, j] = 1
                else:
                    out_life_state[i, j] = 0
            #cell is dead, (i,j) = 0
            else:
                if alive_neighbors == 3:
                    out_life_state[i, j] = 1
    
    return out_life_state


new_life_state = update_life_state_1(life_state)
draw_life_state_1(new_life_state)