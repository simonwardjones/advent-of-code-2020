import fs from 'fs'
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const dayOneDataFile = '/dayTwentyFourDataSample.txt'


const loadData = () => new Promise((resolve, reject) => {
    fs.readFile(__dirname + dayOneDataFile, 'utf8', function (err, data) {
        if (err) {
            reject(err)
        } else {
            const rawData = data.split('\n')
            resolve(rawData)
        }
    })
})


function get_directions(line) {
    var directions = []
    for (let i = 0; i < line.length; i++) {
        if (['s', 'n'].includes(line[i])) {
            directions.push(line.slice(i, i + 2))
            i += 1
        } else {
            directions.push(line[i])
        }
    }
    return directions
}

class Vector {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    add(other) {
        return new Vector(this.x + other.x, this.y + other.y)
    }

    key() {
        return `${this.x}-${this.y}`
    }
}


function step_direction(direction, from) {
    let step
    switch (direction) {
        case 'e':
            step = new Vector(1, 0)
            break;
        case 'se':
            step = new Vector(0, -1)
            break;
        case 'sw':
            step = new Vector(-1, -1)
            break;
        case 'w':
            step = new Vector(-1, 0)
            break;
        case 'nw':
            step = new Vector(0, 1)
            break;
        case 'ne':
            step = new Vector(1, 1)
            break;
    }
    return from.add(step)
}

function get_tile_from_directions(directions) {
    var current_pos = new Vector(0, 0)
    directions.forEach(direction => {
        current_pos = step_direction(direction, current_pos)
    })
    return current_pos
}

function partOne() {
    console.log('Advent of code - day 24 - part 1 - tile mapping')
    loadData().then((rawData) => {
        console.log(rawData.slice(0, 3))

        var directions = rawData.map(get_directions)
        console.log(directions.slice(0, 3))

        var positions = directions.map(get_tile_from_directions)
        console.log(positions.slice(0, 3))

        var tile_colours = {}
        positions.forEach(vec => {
            // console.log(`Changing ${vec.key()}`)
            if (tile_colours[vec.key()] === undefined) {
                tile_colours[vec.key()] = 1
            }
            else {
                tile_colours[vec.key()] = ((tile_colours[vec.key()] + 1) % 2)
            }
        })
        console.log(tile_colours)
        console.log(Object.values(tile_colours).reduce((x,y) => x+y))

    })
}

partOne()