import argparse
import yaml

def represent_list(dumper, data):
    """
    A custom representer for YAML that forces lists to be dumped in inline style.
    
    This function modifies the default behavior of the YAML dumper for lists,
    ensuring that they are represented in a compact, inline format. This is particularly
    useful for ensuring compatibility with parsers that require a specific YAML format.
    Parameters:
    dumper (yaml.Dumper): The YAML dumper instance.
    data (list): The list to be dumped in YAML format.
    Returns:
    yaml.Node: A YAML node representing the sequence in flow style.
    """

    return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

def generate_hex_grid(radius, truncate):
    """
    Generates a hexagonal grid with a specified radius.
    Parameters:
    radius (int): The radius of the hexagonal grid, where radius >= 0.
    Returns:
    list: A list of dictionaries representing each hex tile.
    """
    grid = []
    # Loop through each possible value of r within the hexagonal grid
    for r in range(-radius, radius + 1):
        # Determine the start and end q values for the current row
        q_start = max(-radius, -radius - r)
        q_end = min(radius, radius - r)
        row = []
        for q in range(q_start, q_end + 1):
            # Calculate s such that the sum of q, r, and s equals 0
            s = -q - r

            if truncate and q == radius or r == radius or s == radius:
                continue

            # Tile data besides the location is constant: Downstream treats
            # "biome" as either "DISCOVERED" (draw) or "UNDISCOVERED" (ignore)
            tile = {
                "kind": "Tile",
                "spec": {
                    "location": [ q, r, s ],
                    "biome": "DISCOVERED"
                }
            }
            row.append(tile)
        grid.extend(row)
    return grid

def main():
    """
    Outputs the hex grid to a YAML file.
    """
    parser = argparse.ArgumentParser(description="Generate a hexagonal grid for Downstream Game by Playmint.")
    parser.add_argument("--radius", type=int, default=0, help="Radius of the hexagonal grid. Must be non-negative.")
    parser.add_argument("--output", type=str, default="map.yaml", help="Output YAML file name.")
    parser.add_argument("--truncate", type=int, default=0, help="Truncate the upper range of the signed integer boundary.")

    args = parser.parse_args()

    # Ensure the radius is non-negative
    if args.radius < 0:
        parser.error("Radius must be non-negative.")
        exit(1)

    grid = generate_hex_grid(args.radius, args.truncate)

    print(len(grid))
    
    with open(args.output, "w") as file:
        for item in grid:
            yaml.dump(item, file, explicit_start=True, default_flow_style=None, sort_keys=False)

if __name__ == "__main__":
    main()
