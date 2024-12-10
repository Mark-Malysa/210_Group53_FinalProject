import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
import time

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
