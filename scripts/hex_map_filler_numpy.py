import numpy as np
import yaml
import argparse

def represent_list(dumper, data):
    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

def generate_hex_grid(radius, truncate_signed):
    """
    Generates a hexagonal grid with a specified radius using NumPy for faster computation.
    """
    q_range = np.arange(-radius, radius + 1)
    grid = []
    for r in range(-radius, radius + 1):
        q_start = max(-radius, -radius - r)
        q_end = min(radius, radius - r)
        q_vals = np.arange(q_start, q_end + 1)
        s_vals = -q_vals - r

        row = [{
            "kind": "Tile",
            "spec": {
                "location": [int(q), int(r), int(s)],
                "biome": "DISCOVERED"
            }
        } for q, s in zip(q_vals, s_vals)]
        
        grid.extend(row)
    return grid

def main():
    """
    Outputs the hex grid to a YAML file.
    """
    parser = argparse.ArgumentParser(description="Generate a hexagonal grid for Downstream Game by Playmint.")
    parser.add_argument("--radius", type=int, default=0, help="Radius of the hexagonal grid. Must be non-negative.")
    parser.add_argument("--output", type=str, default="map.yaml", help="Output YAML file name.")
    parser.add_argument("--truncate-signed", type=int, default=0, help="Truncate the top of the signed integer range.")

    args = parser.parse_args()

    # Ensure the radius is non-negative
    if args.radius < 0:
        parser.error("Radius must be non-negative.")
        exit(1)

    grid = generate_hex_grid(args.radius, args.truncate_signed)

    print(len(grid))
    '''
    with open(args.output, "w") as file:
        for item in grid:
            yaml.dump(item, file, explicit_start=True, default_flow_style=None, sort_keys=False)
    '''
if __name__ == "__main__":
    main()
