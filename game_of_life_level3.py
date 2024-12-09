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
n, m = 10, 10
life_state = init_life_state_3(n, m, probabilities, states)

# Draw the grid
#uncomment to see the grid and test the above functions
#draw_life_state_3(life_state, state_colors)

#helper function that returns the number of neighbors that match the given type
def get_neighbors(life_state, i, j, n, m, type):
    neighbors_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    count_of_type = 0;
    for di, dj in neighbors_offsets:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < m:
            if life_state[ni, nj] == type:
                count_of_type += 1
    return count_of_type

#helper function that uses the probabilities to decide which state to return
def handle_probabilities_rule(rule, current_state = 0):
    dict_of_probs = {}
    prev_value = 0
    for prob in rule:
        dict_of_probs[prob['then']["turn_to"] ] = prev_value + prob['value']

    #sort the probabilities in ascending order based on value
    dict_of_probs = {k: v for k, v in sorted(dict_of_probs.items())}
    #make it so that each value is the sum of all previous values
    for turn_to, prob in dict_of_probs.items():
        dict_of_probs[turn_to] = prob + prev_value
        prev_value = prob+prev_value

    random_value = random.uniform(0, 1)
    for ret, prob in dict_of_probs.items():
        if random_value < prob:
            return ret
    
    return "error"

def update_life_state_3(life_state, rules_dict, out_life_state=None):
    """
    Update the grid based on the rules specified for each state (could be any arbitrary state and rule).
    
    IN: 
        life_state (ndarray): 2D array representing the current state of the cells.
        rules_dict (dict): The dictionary containing the rules for updating the cells.
        out_life_state (ndarray, optional): 2D array to store the next state. If None, a new array is created.
        
    OUT: 
        ndarray: The updated 2D array representing the next state of the cells.
    """
    n, m = life_state.shape  # Get the grid dimensions
    
    if out_life_state is None:
        out_life_state = np.copy(life_state)  # Initialize the output state with the current state

    # Iterate over each cell in the grid
    for i in range(n):
        for j in range(m):
            current_state = life_state[i, j]  # Current state of the cell
            # Get the rules for the current state of the cell
            if current_state in rules_dict:  # Check if the current state is in the rules_dict:
                rules = rules_dict[current_state]
                for rule in rules:
                    # Handle neighbor-based transitions (if applicable)
                    if 'neighbor_to' in rule:
                        curr_rule = rule['neighbor_to']
                        curr_rule_if = curr_rule['if']
                        curr_rule_then = curr_rule['then']
                        #checks if the number of neighbors is within the range
                        neighbors = get_neighbors(life_state, i, j, n, m, current_state)
                        if neighbors >= curr_rule_if[0]['at_least'] and neighbors <= curr_rule_if[0]['at_most']:
                            curr_rule = curr_rule_then
                            # Handle probability-based transitions in neighbor-based transitions
                            if 'probability' in curr_rule:
                                probabilitys = curr_rule['probability']
                                out_life_state[i, j] = handle_probabilities_rule(probabilitys ,current_state)
                            # Handle turn-to transitions in neighbor-based transitions
                            elif 'turn_to' in curr_rule:
                                out_life_state[i, j] = curr_rule['turn_to']
                    # Handle probability-based transitions
                    elif 'probability' in rule:
                        probabilitys = rule['probability']
                        out_life_state[i, j] = handle_probabilities_rule(probabilitys)
                    # Handle turn-to transitions
                    elif 'turn_to' in rule:
                        out_life_state[i, j] = rule['turn_to']
                        
    #returns the updated life_state
    return out_life_state

# Example usage:
rules = {
    0: [  # Removed cells
        {
            "turn_to": 0  # Always stay removed
        }
    ],
    1: [  # Susceptible cells
        {
            "neighbor_to": {
                "if": [  # Adjacent to at least 1 infected cell (type 2)
                    {
                        "at_least": 1,
                        "at_most": 9,  # Always true
                        "type": 2
                    }
                ],
                "then": {
                    "probability": [  # 25% chance of getting infected and 75% chance of staying susceptible
                        {
                            "value": 0.9,  # Transmission rate 25%
                            "then": {
                                "turn_to": 2  # Turn to infected
                            },
                        },
                        {
                            "value": 0.1,  # Leftover 75%
                            "then": {
                                "turn_to": 1  # Stay susceptible
                            }
                        }
                    ]
                }
            }
        }
    ],
    2: [  # Infected cells
        {  # Infected cells
            "probability": [  # 50% chance of recovering and 50% chance of staying infected
                {
                    "value": 0.5,  # Recovery rate 50%
                    "then": {
                        "turn_to": 0  # Turn to removed
                    }
                },
                {
                    "value": 0.5,  # Leftover 50%
                    "then": {
                        "turn_to": 2  # Stay infected
                    }
                }
            ]
        }
    ]
}

#example usage
#uncomment to see the grid and test the above functions
#updated_state = update_life_state_3(life_state, rules)
#draw_life_state_3(updated_state, state_colors)

def save_state_to_csv(state, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(state)

# Function to load rules from a JSON file
def load_rules_from_json(filename):
    with open(filename, 'r') as file:
        rules = json.load(file)
    return rules

# Main function to run the game
def play_game_of_life_3():
    #Ask the user for initial state parameters
    n = int(input("Enter number of rows: "))
    #input check
    while not isinstance(n, int):
        n = int(input("Invalid input for rows. Please enter an integer."))

    m = int(input("Enter number of columns: "))
    #input check
    while not isinstance(m, int):        
        m = int(input("Invalid input for columns. Please enter an integer."))

    p_list = list(map(float, input("Enter the probabilities for each state (comma separated): ").split(',')))
    #input check
    while not all(0 <= p <= 1 for p in p_list):
        p_list = list(map(float, input("Invalid input for probabilities. Please enter decimal numbers between 0 and 1 (comma separated): ").split(',')))
    
    colors = list(map(str, input("Enter the colors for each state (comma separated): ").split(',')))
    #input check
    while not all(isinstance(color, str) for color in colors):        
        colors = list(map(str, input("Invalid input for colors. Please enter strings (comma separated): ").split(',')))

    states = list(map(int, input("Enter the states (comma separated): ").split(',')))
    #input check
    while not all(isinstance(state, int) for state in states):        
        states = list(map(int, input("Invalid input for states. Please enter integers (comma separated): ").split(',')))

    # Generate the initial life state randomly based on probabilities
    life_state = init_life_state_3(n, m, p_list, states)

    #Ask the user for the rules file (JSON)
    rules_file = input("Enter the JSON file path for the rules: ")
    rules = load_rules_from_json(rules_file)
    rules = {int(key): value for key, value in rules.items()}
    #Ask the user for the number of iterations
    iterations = int(input("Enter the number of iterations: "))

    #Display the initial state
    draw_life_state_3(life_state, colors={state: color for state, color in zip(states, colors)})
    #Display and update the grid for each iteration
    for i in range(iterations):
        print(f"Iteration {i + 1}:")
        life_state = update_life_state_3(life_state, rules)
        draw_life_state_3(life_state, colors={state: color for state, color in zip(states, colors)})

        # Ask user if they want to continue
        continue_game = input("Do you want to continue to the next iteration? (y/n): ")
        if continue_game.lower() != 'y':
            break
    
    #Ask if the user wants to save the initial and final states
    save_choice = input("Do you want to save the initial and final states as CSV files? (y/n): ")
    if save_choice.lower() == 'y':
        initial_filename = input("Enter the filename for the initial state (CSV): ")
        final_filename = input("Enter the filename for the final state (CSV): ")
        save_state_to_csv(life_state, final_filename)
        save_state_to_csv(life_state, initial_filename)  # Assuming user wants to save the same state

    #Ask if the user wants to save the rules
    save_rules_choice = input("Do you want to save the rules as a JSON file? (y/n): ")
    if save_rules_choice.lower() == 'y':
        rules_filename = input("Enter the filename to save the rules as JSON: ")
        with open(rules_filename, 'w') as json_file:
            json.dump(rules, json_file, indent=4)

    print("Game Over.")

play_game_of_life_3()