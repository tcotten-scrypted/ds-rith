import argparse
import random
import subprocess
import time
import yaml

valid_coordinates = []
private_key = None

def parse_tiles(yaml_file):
    # Open the YAML file and load its contents
    with open(yaml_file, 'r') as file:
        documents = file.read()

    # Split the documents on the '---' separator
    tiles = documents.split('---')
    
    # Prepare a list to hold the coordinates
    coordinates = []

    # Process each tile entry
    for tile in tiles:
        if tile.strip():  # Ensure the tile entry is not just whitespace
            # Load the YAML content for this tile
            data = yaml.safe_load(tile)
            if data['kind'] == 'Tile':  # Confirm it's a Tile entry
                location = data['spec']['location']
                coordinates.append(tuple(location))  # Add coordinates as a tuple to the list

    return coordinates

def random_sleep():
    # Generate a random float between 0.1 and 1.0
    sleep_time = random.uniform(0.1, 1.0)

    # Sleep for the generated duration
    time.sleep(sleep_time)
    print(f"Slept for {sleep_time:.2f} seconds.")

def run_command(command):
    # Execute the command
    try:
        # subprocess.run() is recommended as it is easier to use
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("Command output:", result.stdout)
        print("Error (if any):", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error during command execution:", str(e))

def goto_coordinate(coord_str):
    global private_key

    command = [
        'ds', '-k', private_key,
        '-n', 'local', '-z', '1', 'dispatch', 'MOVE_MOBILE_UNIT', coord_str
    ]

    run_command(command)

def autonomy():
    global valid_coordinates

    # First, move the current mobile object attached to the private key to [1, 0, 0, 0]
    goto_coordinate("[1, 0, 0, 0]")

    # Let's run a 250ms - 1 second loop that will 
    current_coord = (0, 0, 0)

    while True:
        # modify current_coord by randomly rolling, these are hex coordinates (q, r, s) so they must sum to 0
        # rolling system: roll between 0 and 2, this is the Q, R, or S dimension to modify
        # rolling system: roll between -1 and 1, this is the movement to make
        # rolling system: modify the affected dimension and its counterpart, solve for 0 to give the third dimension
        # update current_coord
        # create a coord_str variable of format f"[1, {current_coord[0]}, {current_coord[1]}, {current_coord[2]}]"
        # call goto_coordinate(private_key, coord_str)
        # sleep for 100ms to 1 second

        # Randomly choose a dimension to modify (0 = q, 1 = r, 2 = s)
        dim_to_modify = random.randint(0, 2)

        # Random movement step: -1, 0, or 1
        movement_step = random.randint(-1, 1)

        # Calculate the new coordinates ensuring they sum to zero
        new_coords = list(current_coord)
        new_coords[dim_to_modify] += movement_step

        # Adjust the other coordinates to ensure the sum remains zero
        if dim_to_modify == 0:
            # Modify r
            new_coords[1] -= movement_step
        elif dim_to_modify == 1:
            # Modify s
            new_coords[2] -= movement_step
        else:
            # Modify q
            new_coords[0] -= movement_step

        # Make sure the sum of coordinates equals zero
        if sum(new_coords) != 0:
            # If not zero, adjust the last coordinate
            new_coords[2] = -new_coords[0] - new_coords[1]

        new_coords = tuple(new_coords)
        if new_coords not in valid_coordinates:
            print(f"Out of bounds: {new_coords}")
        else:
            print(f"Moving to: {new_coords} from {current_coord}")

        current_coord = new_coords

        # Create a coordinate string for the goto_coordinate function
        coord_str = f"[1, {current_coord[0]}, {current_coord[1]}, {current_coord[2]}]"

        # Call the function to move the NPC
        goto_coordinate(coord_str)

        random_sleep()

def main():
    global valid_coordinates
    global private_key

    parser = argparse.ArgumentParser(description='Process some tiles.')
    # Add private key argument, make it required
    parser.add_argument('-k', '--key', required=True, help='Private key for authentication')

    # Parse arguments
    args = parser.parse_args()

    # Check if the private key is provided (though argparse makes it mandatory)
    if not args.key:
        print("Error: A private key must be provided with -k")
        return

    private_key = args.key

    print("Loading available tile coordinates...")
    valid_coordinates = parse_tiles('Tiles.yaml')

    print("Starting Autonomy Emulator at 5% - Random Walk...")
    autonomy()

if __name__ == "__main__":
    main()
