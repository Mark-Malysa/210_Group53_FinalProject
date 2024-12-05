import numpy as np
import matplotlib.pyplot as plt
import csv
import json

def init_life_state_3(n, m, p_list, states):
    """
    Generate an initial random subset of non-binary cells with specified probabilities.
    
    IN: 
        n (int): Number of rows.
        m (int): Number of columns.
        p_list (list of float): List of probabilities for each state.
        states (list of int): List of possible states for the cells.
    
    OUT: 
        ndarray of shape (n, m): Initial state of the cells.
    """
    # Ensure probabilities sum to 1
    assert np.isclose(np.sum(p_list), 1), "Probabilities must sum to 1."

    # Generate a random array of states based on the given probabilities
    life_state = np.random.choice(states, size=(n, m), p=p_list)
    return life_state


def draw_cell_background(x, y, color):
    plt.fill([x - 0.5, x - 0.5, x + 0.5, x + 0.5], [y - 0.5, y + 0.5, y + 0.5, y - 0.5], color=color, alpha=0.5,  edgecolor='black')

def draw_life_state_3(life_state, colors):
    """
    Display the 2D grid of cells with their respective states and colors.
    
    IN:
        life_state (ndarray): The state of the cells in the grid.
        colors (list of str): List of colors corresponding to each state.
    
    OUT: None
    """
    n, m = life_state.shape
    plt.figure(figsize=(m / 2, n / 2))

    # Iterate over each cell in the grid and color it based on its state
    for i in range(n):
        for j in range(m):
            state = life_state[i, j]
            color = colors[state]  # Map the state to a color
            draw_cell_background(j, i, color)  # Draw the cell


    plt.gca().invert_yaxis()  # Invert y-axis so that (0,0) is at the top-left
    plt.axis('off')  # Hide the axes
    plt.show()

# Example usage:
# Define the states and their probabilities
states = [0, 1, 2]
probabilities = [0.3, 0.6, 0.1] 

# Define state colors
state_colors = {
    0: 'gray',  # Removed cells are gray
    1: 'green',  # Susceptible cells are green
    2: 'red',    # Infected cells are red
}

# Initialize the grid
n, m = 20, 20
life_state = init_life_state_3(n, m, probabilities, states)

# Draw the grid
draw_life_state_3(life_state, state_colors)


