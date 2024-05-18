import argparse
import random
import subprocess
import time
import yaml

valid_coordinates = []
private_key = None

def parse_tiles(yaml_file):
    with open(yaml_file, 'r') as file:
        documents = file.read()

    tiles = documents.split('---')
    coordinates = []

    for tile in tiles:
        if tile.strip():
            data = yaml.safe_load(tile)
            if data['kind'] == 'Tile':
                location = data['spec']['location']
                coordinates.append(tuple(location))

    return coordinates

def random_sleep():
    sleep_time = random.uniform(0.1, 1.0)
    time.sleep(sleep_time)
    print(f"Slept for {sleep_time:.2f} seconds.")

def run_command(command):
    try:
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

def demo_000_randomwalk():
    global valid_coordinates
    goto_coordinate("[1, 0, 0, 0]")
    current_coord = (0, 0, 0)

    while True:
        dim_to_modify = random.randint(0, 2)
        movement_step = random.randint(-1, 1)
        new_coords = list(current_coord)
        new_coords[dim_to_modify] += movement_step

        if dim_to_modify == 0:
            new_coords[1] -= movement_step
        elif dim_to_modify == 1:
            new_coords[2] -= movement_step
        else:
            new_coords[0] -= movement_step

        if sum(new_coords) != 0:
            new_coords[2] = -new_coords[0] - new_coords[1]

        new_coords = tuple(new_coords)
        if new_coords not in valid_coordinates:
            print(f"Out of bounds: {new_coords}")
        else:
            print(f"Moving to: {new_coords} from {current_coord}")

        current_coord = new_coords
        coord_str = f"[1, {current_coord[0]}, {current_coord[1]}, {current_coord[2]}]"
        goto_coordinate(coord_str)
        random_sleep()

def demo_001_pathfinding():
    coords = parse_tiles('./demos/001-Pathfinding/Pathing.yml')
    starting_coord = coords[0]
    
    goto_coordinate(f"[1, {starting_coord[0]}, {starting_coord[1]}, {starting_coord[2]}]")
    
    idx = 1
    while True:
        next_coord = coords[idx]
        next_coord_str = f"[1, {next_coord[0]}, {next_coord[1]}, {next_coord[2]}]"
        
        goto_coordinate(next_coord_str)
    
        idx = (idx + 1) % len(coords)
        
    # Placeholder for simple pathfinding demo logic
    print("Running Simple Pathfinding demo...")

def main():
    global valid_coordinates
    global private_key

    parser = argparse.ArgumentParser(description='Process some tiles.')
    parser.add_argument('-k', '--key', required=True, help='Private key for authentication')
    parser.add_argument('-d', '--demo', required=True, choices=['0', '1'], help='Demo id to run')

    args = parser.parse_args()
    private_key = args.key

    print("Loading available tile coordinates...")
    valid_coordinates = parse_tiles('Tiles.yaml')

    if args.demo == '0':
        print("Starting Demo 000: Random Walk...")
        demo_000_randomwalk()
    elif args.demo == '1':
        print("Starting Demo 001: Simple Pathfinding...")
        demo_001_pathfinding()
    else:
        print("Invalid demo id provided.")

if __name__ == "__main__":
    main()