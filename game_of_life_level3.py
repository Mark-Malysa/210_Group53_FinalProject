import numpy as np
import matplotlib.pyplot as plt
import csv
import json
import random

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


def update_life_state_3(life_state, rules_dict, out_life_state=None):
    """
    Update the grid based on the rules specified for each state (removed, susceptible, infected).
    
    IN: 
        life_state (ndarray): 2D array representing the current state of the cells.
        rules_dict (dict): The dictionary containing the rules for each state.
        out_life_state (ndarray, optional): 2D array to store the next state. If None, a new array is created.
        
    OUT: 
        ndarray: The updated 2D array representing the next state of the cells.
    """
    
    n, m = life_state.shape  # Get the grid dimensions
    
    if out_life_state is None:
        out_life_state = np.copy(life_state)  # Initialize the output state with the current state
    
    # Define neighbor offsets for the 8 neighboring cells (N, NE, E, SE, S, SW, W, NW)
    neighbors_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for i in range(n):
        for j in range(m):
            current_state = life_state[i, j]  # Current state of the cell

            if current_state == 0:  # Removed cell
                # Removed cells always stay removed (no change)
                continue

            elif current_state == 1:  # Susceptible cell
                # Find infected neighbors
                infected_neighbors = 0
                for di, dj in neighbors_offsets:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m and life_state[ni, nj] == 2:
                        infected_neighbors += 1

                # Apply the susceptible-to-infected rule based on infected neighbors
                susceptible_rule = rules_dict[1][0]['neighbor_to']
                for condition in susceptible_rule['if']:
                    # Check if the number of infected neighbors is within the specified range
                    if condition["at_least"] <= infected_neighbors <= condition["at_most"]:
                        # Apply the probability of getting infected
                        probabilities = rules_dict[1][0]['neighbor_to']['then']['probability']
                        for prob in probabilities:
                            if random.random() < prob['value']:
                                # Update the cell's state based on the probability
                                out_life_state[i, j] = prob['then']['turn_to']
                                break
                        #---comment---

            elif current_state == 2:  # Infected cell
                # Apply the infected-to-removed or infected-to-infected rule based on probabilities
                infected_rule = rules_dict[2][0]['probability']
                for prob in infected_rule:
                    if random.random() < prob['value']:
                        out_life_state[i, j] = prob['then']['turn_to']
                        break
                        #---comment---
                    
    return out_life_state
