import sys

# Constants
TILE_ID_PREFIX = "0xe5a62ffc"

def to_int16_hex(value):
    # Convert an integer to a 16-bit hexadecimal string
    return '{:04x}'.format(value & 0xFFFF)

def to_twos(value, width):
    # Convert a decimal integer to a two's complement hexadecimal string
    if value < 0:
        value = (1 << width) + value
    return value

def from_twos(value, width):
    # Convert a two's complement hexadecimal string to a decimal integer
    if value >= (1 << (width - 1)):
        value -= (1 << width)
    return value

def get_tile_id_from_coords(coords):
    # Get tile ID from coordinates
    z, q, r, s = map(lambda x: to_int16_hex(to_twos(x, 16)), coords)
    return f"{TILE_ID_PREFIX}000000000000000000000000{z}{q}{r}{s}"
'''
def get_tile_coords_from_id(tile_id):
    # Decode a tile ID into its q, r, s hexagonal coordinates
    tile_id = tile_id[len(TILE_ID_PREFIX):]
    coords = [tile_id[i:i+4] for i in range(0, len(tile_id), 4)]
    return [from_twos(int(coord, 16), 16) for coord in coords]
'''
def get_tile_coords_from_id(tile_id):
    # Remove the prefix and unnecessary zeros used for padding
    effective_hex = tile_id[len(TILE_ID_PREFIX):]
    # Since we have padded with 24 zeros, remove them
    effective_hex = effective_hex[24:]
    coords = [effective_hex[i:i+4] for i in range(0, len(effective_hex), 4)]
    return [from_twos(int(coord, 16), 16) for coord in coords]

def main():
    # Main execution function
    if len(sys.argv) != 2 or (sys.argv[1] != 'encode' and sys.argv[1] != 'decode'):
        print('Usage: python script.py <encode|decode>')
        return

    if sys.argv[1] == 'encode':
        test_coords = [1, -1, -2, 3]  # z, q, r, s
        tile_id = get_tile_id_from_coords(test_coords)
        print(f"Encoded Tile ID: {tile_id}")
    else:
        tile_id = '0xe5a62ffc0000000000000000000000000001ffff00000001'
        coords = get_tile_coords_from_id(tile_id)
        print(f"Decoded Coordinates: [{', '.join(map(str, coords))}]")

if __name__ == "__main__":
    main()
