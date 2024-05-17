import ds from 'downstream';

const TILE_ID_PREFIX = "0xe5a62ffc";
const TILE_DEFAULT_COLOR = "#7777FF";
const ZONE_ID = 1;

const PAINT_DEFS = [
    {coords: [ZONE_ID, -1, 2, -1], color: "#ff1ed6" },
    {coords: [ZONE_ID, -1, -2, 3], color: "#ff1ed6" },
    {coords: [ZONE_ID, 3, -2, -1], color: "#ff1ed6" },
    {coords: [ZONE_ID, 2, -1, -1], color: "#ffc877" },
    {coords: [ZONE_ID, 1, 0, -1],  color: "#ffc877" },
    {coords: [ZONE_ID, 0, 1, -1],  color: "#ffc877" },
    {coords: [ZONE_ID, -1, 1, 0],  color: "#ffc877" },
    {coords: [ZONE_ID, -1, 0, 1],  color: "#ffc877" },
    {coords: [ZONE_ID, -1, -1, 2], color: "#ffc877" },
    {coords: [ZONE_ID, 0, -2, 2],  color: "#ffc877" },
    {coords: [ZONE_ID, 1, -2, 1],  color: "#ffc877" },
    {coords: [ZONE_ID, 2, -2, 0],  color: "#ffc877" }
];

const PAINT_TILES = PAINT_DEFS.map(def => Tile.fromCoords(def.coords, def.color));
const PAINT_STATE_OBJECTS = PAINT_TILES.map(tile => tile.getStateObject('color'));

console.log(PAINT_STATE_OBJECTS)

export default async function update(state) {
    const state_diff = {
        version: 1,
        map: [
            {
                type: "tile",
                key: "color",
                id: getTileIdFromCoords([1, 0, 0, 0]),
                value: "#ffc877"
            }
        ],
        components: []
    }

    //state_diff['map'] = PAINT_STATE_OBJECTS;

    return state_diff;
}

class Tile {
    static DEFAULT_STATE_KEYS = ['type', 'id']

    constructor(id, color = TILE_DEFAULT_COLOR, coords = null) {
        this.type = "tile";
        this.id = id;
        this.color = color;

        this.coords = coords || getTileCoordsFromId(id);
    }

    static fromCoords(coords, color = TILE_DEFAULT_COLOR) {
        const id = getTileIdFromCoords(coords)
        
        return new Tile(id, color, coords)
    }

    // A generic representation of the Tile object with a targeted state key/value
    getStateObject(state_key) {
        const stateObject = {};
        
        DEFAULT_STATE_KEYS.forEach(key => {
            stateObject[key] = this[key];
        });

        stateObject['key']   = state_key
        stateObject['value'] = this[state_key]

        return stateObject;
    }
}

// Convert hexadecimal to signed decimal
function hexToSignedDecimal(hex) {
    if (hex.startsWith("0x")) {
        hex = hex.substr(2);
    }

    let num = parseInt(hex, 16);
    let bits = hex.length * 4;
    let maxVal = Math.pow(2, bits);

    // Check if the highest bit is set (negative number)
    if (num >= maxVal / 2) {
        num -= maxVal;
    }

    return num;
}

// Get tile coordinates from hexadecimal coordinates
function getTileCoords(coords) {
    return [
        hexToSignedDecimal(coords[0]),
        hexToSignedDecimal(coords[1]),
        hexToSignedDecimal(coords[2]),
        hexToSignedDecimal(coords[3]),
    ];
}

// Calculate distance between two tiles
function distance(tileCoords, nextTile) {
    return Math.max(
        Math.abs(tileCoords[0] - nextTile[0]),
        Math.abs(tileCoords[1] - nextTile[1]),
        Math.abs(tileCoords[2] - nextTile[2]),
    );
}

// Convert an integer to a 16-bit hexadecimal string
function toInt16Hex(value) {
    return ('0000'+toTwos(value, 16).toString(16)).slice(-4)
}

const BN_0 = BigInt(0);
const BN_1 = BigInt(1);

// Convert a two's complement binary representation to a BigInt
function fromTwos(n, w) {
    let value = BigInt(n);
    let width = BigInt(w);
    if (value >> (width - BN_1)) {
        const mask = (BN_1 << width) - BN_1;
        return -(((~value) & mask) + BN_1);
    }
    return value;
}

// Convert a BigInt to a two's complement binary representation
function toTwos(_value, _width) {
    let value = BigInt(_value);
    let width = BigInt(_width);
    const limit = (BN_1 << (width - BN_1));
    if (value < BN_0) {
        value = -value;
        const mask = (BN_1 << width) - BN_1;
        return ((~value) & mask) + BN_1;
    }
    return value;
}

// Get tile ID from coordinates
function getTileIdFromCoords(coords) {
    const z = toInt16Hex(coords[0]);
    const q = toInt16Hex(coords[1]);
    const r = toInt16Hex(coords[2]);
    const s = toInt16Hex(coords[3]);
    return `${TILE_ID_PREFIX}000000000000000000000000${z}${q}${r}${s}`;
}

// Decode a tile ID into its q, r, s hexagonal coordinates
function getTileCoordsFromId(tileId) {
    const coords = [...tileId]
        .slice(2)
        .reduce((bs, b, idx) => {
            if (idx % 4 === 0) {
                bs.push('0x');
            }
            bs[bs.length - 1] += b;
            return bs;
        }, [])
        .map((n) => Number(fromTwos(n, 16)))
        .slice(-4);
    if (coords.length !== 4) {
        throw new Error(`failed to get z,q,r,s from tile id ${tileId}`);
    }
    return coords;
};

function logState(state) {
    console.log('State sent to plugin:', state);
}
