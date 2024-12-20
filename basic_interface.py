import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.pyplot as plt
import csv

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


#given function from the assignment to draw the cell colors
#modified to display the grid
def draw_cell_background(x, y):
    plt.fill([x-0.5, x-0.5, x+0.5, x+0.5], [y-0.5, y+0.5, y+0.5, y-0.5], color='lightgray', edgecolor='black')


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
                plt.fill([j-0.5, j-0.5, j+0.5, j+0.5], [i-0.5, i+0.5, i+0.5, i-0.5], color='black', edgecolor='black')
    
    # Add axis labels  
    plt.title('Game of Life')
    
    plt.axis('off')
    #add grid
    plt.show()


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


#test for update_life_state task 1.2 and 1.3
# new_life_state = update_life_state_1(life_state)
# draw_life_state_1(new_life_state)

#helper function that saves the life_state grid to a CSV file
def save_to_csv(life_state, filename):
    """
    Save the life_state grid to a CSV file.
    IN: 
        life_state (ndarray): The current state of the grid.
        filename (str): The name of the file to save the grid.
    OUT: None
    """
    # Save the grid to a CSV file with '1' for alive cells and '0' for dead cells
    np.savetxt(filename, life_state, delimiter=',', fmt='%d')


def play_game_of_life_1():
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
    life_state = init_life_state_1(n, m, p)
    
    # ask the user for the number of iterations
    num_iterations = int(input("Enter the number of iterations to run (must be an integer): "))
    #input check
    while not isinstance(num_iterations, int):
        num_iterations = int(input("Invalid input for iterations. Please enter an integer."))

    # Display the initial grid
    draw_life_state_1(life_state)
    # Update the grid and display it at each iteration
    for iteration in range(num_iterations):
        print(f"Iteration {iteration + 1}:")
        life_state = update_life_state_1(life_state)  # Update the grid
        draw_life_state_1(life_state)  # Display the grid after update
        
    # Ask the user if they want to continue updating
    while True:
        continue_update = input("Do you want to continue updating the grid? (yes/no): ").strip().lower()
        if continue_update == 'yes':
            num_iterations = int(input("How many more iterations would you like to run? "))
            # Display the grid initially
            draw_life_state_1(life_state) 
            for iteration in range(num_iterations):
                print(f"Iteration {iteration + 1}:")
                life_state = update_life_state_1(life_state)  # Update the grid
                draw_life_state_1(life_state) 
        elif continue_update == 'no':
            break
        else:
            print("Invalid input:")
    
    #Ask the user if they want to save the initial and final configurations to a CSV file
    while True:
        save_config = input("Do you want to save the initial and final configurations as CSV files? (yes/no): ").strip().lower()
        if save_config == 'yes':
            #Ask the user for the filename
            initial_filename = input("Enter a filename to save the initial state (e.g., initial_state.csv): ")
            final_filename = input("Enter a filename to save the final state (e.g., final_state.csv): ")
            
            # Save the initial and final configurations
            save_to_csv(life_state, final_filename)  # Save the final state
            save_to_csv(init_life_state_1(n, m, p), initial_filename)  # Save the initial state
            print(f"Initial and final configurations saved as {initial_filename} and {final_filename}.")
            break
        elif save_config == 'no':
            break
        else:
            print("Invalid input:")

# Example usage 1.4:
#This will prompt the user to interact with the game of life.
#play_game_of_life_1()

# Your existing functions from the Game of Life script (init_life_state_1, draw_life_state_1, etc.) go here...
# I've removed them from this example for brevity, but make sure to include all those definitions here

# Function to start the Game of Life simulation based on the inputs from the user interface
def start_game_of_life():
    try:
        # Get the grid size and probability from the user inputs
        n = int(entry_rows.get())
        m = int(entry_columns.get())
        p = float(entry_probability.get())
        num_iterations = int(entry_iterations.get())

        if not (0 <= p <= 1):
            raise ValueError("Probability must be between 0 and 1.")
        
        # Initialize the game grid
        life_state = init_life_state_1(n, m, p)
        
        # Show the initial state
        draw_life_state_1(life_state)
        
        # Run the iterations
        for iteration in range(num_iterations):
            time.sleep(0.5)  # Pause between iterations to see the progression
            print(f"Iteration {iteration + 1}:")
            life_state = update_life_state_1(life_state)  # Update the grid
            draw_life_state_1(life_state)  # Display the grid after update
        
        # Optionally save the final state to CSV
        save_final_state = messagebox.askyesno("Save State", "Would you like to save the final state to a CSV file?")
        if save_final_state:
            filename = simpledialog.askstring("Save File", "Enter a filename (e.g., final_state.csv):")
            save_to_csv(life_state, filename)
            messagebox.showinfo("Saved", f"Final state saved as {filename}.")
    
    except ValueError as e:
        messagebox.showerror("Invalid Input", f"Error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Main Tkinter window
root = tk.Tk()
root.title("Conway's Game of Life")

# Create labels, entry fields, and buttons
label_rows = tk.Label(root, text="Number of rows:")
label_rows.grid(row=0, column=0, padx=10, pady=5)

entry_rows = tk.Entry(root)
entry_rows.grid(row=0, column=1, padx=10, pady=5)

label_columns = tk.Label(root, text="Number of columns:")
label_columns.grid(row=1, column=0, padx=10, pady=5)

entry_columns = tk.Entry(root)
entry_columns.grid(row=1, column=1, padx=10, pady=5)

label_probability = tk.Label(root, text="Probability of cell being alive (0-1):")
label_probability.grid(row=2, column=0, padx=10, pady=5)

entry_probability = tk.Entry(root)
entry_probability.grid(row=2, column=1, padx=10, pady=5)

label_iterations = tk.Label(root, text="Number of iterations:")
label_iterations.grid(row=3, column=0, padx=10, pady=5)

entry_iterations = tk.Entry(root)
entry_iterations.grid(row=3, column=1, padx=10, pady=5)

# Start button to run the simulation
start_button = tk.Button(root, text="Start Simulation", command=start_game_of_life)
start_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

# Exit button to close the application
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Run the Tkinter event loop
root.mainloop()
