#!/usr/bin/env node
// Import required libraries
const process = require('process');

// Constants
const TILE_ID_PREFIX = "0xe5a62ffc";

// DONE Convert an integer to a 16-bit hexadecimal string
function toInt16Hex(value) {
    return ('0000'+toTwos(value, 16).toString(16)).slice(-4)
}

// DONE
function getTileIdFromCoords(coords) {
    const z = toInt16Hex(coords[0]);
    const q = toInt16Hex(coords[1]);
    const r = toInt16Hex(coords[2]);
    const s = toInt16Hex(coords[3]);
    return `${TILE_ID_PREFIX}000000000000000000000000${z}${q}${r}${s}`;
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

// Main execution function
function main() {
    const args = process.argv.slice(2);

    if (args.length !== 1 || (args[0] !== 'encode' && args[0] !== 'decode')) {
        console.log('Usage: node script.js <encode|decode>');
        return;
    }

    if (args[0] === 'encode') {
        const testCoords = [1, -32768, 0, 32767]; // z, q, r, s
        const tileId = getTileIdFromCoords(testCoords);
        console.log(`Encoded Tile ID: ${tileId}`);
    } else {
        const tileId = '0xe5a62ffc0000000000000000000000000001ffff00000001';
        const coords = getTileCoordsFromId(tileId);
        console.log(`Decoded Coordinates: [${coords.join(', ')}]`);
    }
}

// Execute the script
main();
