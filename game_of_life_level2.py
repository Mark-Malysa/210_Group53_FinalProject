import numpy as np
import matplotlib.pyplot as plt
import csv
import json

def init_life_state_2(n, m, p):
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
    plt.fill([x-0.5, x-0.5, x+0.5, x+0.5], [y-0.5, y+0.5, y+0.5, y-0.5], color='lightgray', edgecolor='black')


def draw_life_state_2(life_state):
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
                plt.fill([j-0.5, j-0.5, j+0.5, j+0.5], [i-0.5, i+0.5, i+0.5, i-0.5], color='black', edgecolor='black')
    
    # Add axis labels  
    plt.title('Game of Life')
    
    plt.axis('off')
    #add grid
    plt.show()

# Example usage 2.1 (same as for 1.1):
n, m, p = 20, 30, 0.1  # 20 rows, 30 columns, 20% chance of being alive
life_state = init_life_state_2(n, m, p)
draw_life_state_2(life_state)



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


def update_life_state_2(life_state, b1=3, b2=3, d1=2, d2=3, out_life_state=None):
    """
    For each cell, evaluate the update rules specified above to obtain its new state based on custom bounds.
    
    IN: 
        life_state (ndarray): Current state of the grid (n, m).
        b1 (int): Lower bound of the number of neighbors for a dead cell to come to life.
        b2 (int): Upper bound of the number of neighbors for a dead cell to come to life.
        d1 (int): Lower bound of the number of neighbors for an alive cell to continue being alive.
        d2 (int): Upper bound of the number of neighbors for an alive cell to continue being alive.
        out_life_state (ndarray): A pre-allocated array for storing the next state of the cells. 
                                  If None, a new array will be created.
    
    OUT: 
        out_life_state (ndarray): The next state of the grid (n, m).
    """
    # Get the dimensions of the grid
    n, m = life_state.shape
    
    # If out_life_state is None, create a new array with the same shape as life_state
    if out_life_state is None:
        out_life_state = np.zeros_like(life_state)
    
    # Update each cell based on the custom rules
    for i in range(n):
        for j in range(m):
            alive_neighbors = count_neighbors(i, j, life_state)
            #cell is dead, (i,j) = 0
            if life_state[i, j] == 0:
                if b1 <= alive_neighbors <= b2:
                    out_life_state[i, j] = 1  # Cell comes to life
                else:
                    out_life_state[i, j] = 0  # Cell stays dead
            #cell is alive, (i,j) = 1
            else:
                if d1 <= alive_neighbors <= d2:
                    out_life_state[i, j] = 1  # Cell stays alive
                else:
                    out_life_state[i, j] = 0  # Cell dies
    
    # Return the updated grid
    return out_life_state

#test for update_life_state task 2.2 and 2.3
new_life_state = update_life_state_2(life_state)
draw_life_state_2(new_life_state)


def save_to_csv(life_state, filename):
    """
    Save the life_state grid to a CSV file.
    IN: 
        life_state (ndarray): The current state of the grid.
        filename (str): The name of the file to save the grid.
    OUT: None
    """
    np.savetxt(filename, life_state, delimiter=',', fmt='%d')

def save_rules_to_json(rules, filename):
    """
    Save the rules to a JSON file.
    IN:
        rules (dict): The dictionary of rules.
        filename (str): The name of the file to save the rules.
    OUT: None
    """
    with open(filename, 'w') as f:
        json.dump(rules, f, indent=4)

def play_game_of_life_2():
    """
    Play the game of life by updating the grid based on user input.
    IN: None
    OUT: None
    """

    print("Welcome to the Game of Life!")
    #ask the user for initial state
    n = int(input("Enter the number of rows (must be an integer, e.g., 30): "))
    #input check
    while not isinstance(n, int):
        n = int(input("Invalid input for rows. Please enter an integer."))
    
    m = int(input("Enter the number of columns (must be an integer, e.g., 30): "))
    #input check
    while not isinstance(m, int):
        m = int(input("Invalid input for columns. Please enter an integer."))

    p = float(input("Enter the probability of a cell being alive (must be a decimal number between 0 and 1, e.g., 0.2): "))
    #input check
    while not 0 <= p <= 1 or not isinstance(p, float):
        p = float(input("Invalid input for probability. Please enter a decimal number between 0 and 1."))

    # Initialize the grid
    life_state = init_life_state_2(n, m, p)

    # Step 2: Ask the user for the rules
    print("Enter the custom rules for the Game of Life:")
    b1 = int(input("Enter the lower bound (b1) for a dead cell to come to life (e.g., 3): "))
    #intput check
    while b1 < 0 or not isinstance(b1, int):
        b1 = int(input("Invalid input for b1. Please enter an integer."))
    
    b2 = int(input("Enter the upper bound (b2) for a dead cell to come to life (e.g., 3): "))
    #intput check
    while b2 < 0 or not isinstance(b2, int):
        b2 = int(input("Invalid input for b2. Please enter an integer."))
    
    d1 = int(input("Enter the lower bound (d1) for an alive cell to stay alive (e.g., 2): "))
    #intput check    
    while d1 < 0 or not isinstance(d1, int):
        d1 = int(input("Invalid input for d1. Please enter an integer."))

    d2 = int(input("Enter the upper bound (d2) for an alive cell to stay alive (e.g., 3): "))
    #intput check
    while d2 < 0 or not isinstance(d2, int):
        d2 = int(input("Invalid input for d2. Please enter an integer."))
    
    
    # ask the user for the number of iterations
    num_iterations = int(input("Enter the number of iterations to run (must be an integer): "))
    #input check
    if not isinstance(num_iterations, int):
        num_iterations = int(input("Invalid input for iterations. Please enter an integer."))

    # Display the initial grid
    draw_life_state_2(life_state)

    # Update the grid and display it at each iteration
    for iteration in range(num_iterations):
        print(f"Iteration {iteration + 1}:")
        life_state = update_life_state_2(life_state, b1, b2, d1, d2)
        draw_life_state_2(life_state)
        
    # Ask the user if they want to continue updating
    while True:
        continue_update = input("Do you want to continue updating the grid? (yes/no): ").strip().lower()
        if continue_update == 'yes':
            num_iterations = int(input("How many more iterations would you like to run? "))
            while not isinstance(num_iterations, int):
                num_iterations = int(input("Invalid input for iterations. Please enter an integer."))
            # Display the grid initially
            draw_life_state_2(life_state) 
            for iteration in range(num_iterations):
                print(f"Iteration {iteration + 1}:")
                life_state = update_life_state_2(life_state, b1, b2, d1, d2)  # Update the grid
                draw_life_state_2(life_state) 
        elif continue_update == 'no':
            break
        else:
            print("Invalid input.")
    
    #Ask the user if they want to save the initial and final configurations to a CSV file
    while True:
        save_config = input("Do you want to save the initial and final configurations as CSV files? (yes/no): ").strip().lower()
        if save_config == 'yes':
            #Ask the user for the filename
            initial_filename = input("Enter a filename to save the initial state (e.g., initial_state.csv): ")
            final_filename = input("Enter a filename to save the final state (e.g., final_state.csv): ")
            rules_filename = input("Enter a filename to save the rules (e.g., rules.json): ")

            # Save the initial and final configurations
            save_to_csv(life_state, final_filename)  # Save the final state
            save_to_csv(init_life_state_2(n, m, p), initial_filename)  # Save the initial state
            print(f"Initial and final configurations saved as {initial_filename} and {final_filename}.")
            
            # Save the user-defined rules as a JSON file
            rules = {"b1": b1, "b2": b2, "d1": d1, "d2": d2}
            save_rules_to_json(rules, rules_filename)
            print(f"Rules saved as {rules_filename}.")
            break
        elif save_config == 'no':
            break
        else:
            print("Invalid input.")

#Example usage:
#This will prompt the user to interact with the game of life.
play_game_of_life_2()