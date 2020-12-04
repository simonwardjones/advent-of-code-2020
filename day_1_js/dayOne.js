import fs from 'fs'
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const dayOneDataFile = '/dayOneData.txt'



function findPair(data, target) {
    /* find pair in data that sum to target */
    let numberOne, numberTwo;
    for (let i = 0, len = data.length; i < len - 1; i++) {
        for (let j = i + 1; j < len; j++) {
            if (data[i] + data[j] == target) {
                [numberOne, numberTwo] = [data[i], data[j]]
            }
        }
    }
    return [numberOne, numberTwo]
}

function findTriple(data, target) {
    /* find triple in data that sum to target */
    for (let i = 0, len = data.length; i < len; i++) {
        const searchData = [...data]
        // remove the current data point then use find pair
        searchData.splice(i, 1)
        const numberOne = data[i]
        const pairTarget = (target - numberOne)

        const [numberTwo, numberThree] = findPair(searchData, pairTarget)
        if (numberTwo !== undefined) {
            console.log([numberOne, numberTwo, numberThree])
            return [numberOne, numberTwo, numberThree]
        }

    }
}

// console.log(findPair([1, 2, 3], 4))
// findPair([1,2,3],10)
// findTriple([1,2,7,3],6)



const loadData = () => new Promise((resolve, reject) => {
    fs.readFile(__dirname + dayOneDataFile, 'utf8', function (err, data) {
        if (err) {
            reject(err)
        } else {
            const rawData = data.split('\n').map(parseFloat)
            resolve(rawData)
        }
    })
})

// loadData().then((s) => 3).catch(err=>console.log('Error loading data: ',err))

function partOne() {
    console.log('Advent of code - day 1 - part 1 - finding numbers summing to target in list')
    loadData().then((rawData) => {
        const target = 2020

        // console.log(rawData);
        let numberOne, numberTwo
        [numberOne, numberTwo] = findPair(rawData, target)

        // console.log(numberOne, numberTwo)
        console.log(`The resulting product is ${numberOne * numberTwo}`)
        return [numberOne, numberTwo]
    })

}

function partTwo() {
    console.log('Advent of code - day 1 - part 2 - finding numbers summing to target in list')
    loadData().then(rawData => {
        const target = 2020

        // console.log(rawData);
        let numberOne, numberTwo, numberThree
        [numberOne, numberTwo, numberThree] = findTriple(rawData, target)

        // console.log(numberOne, numberTwo)
        console.log(`The resulting product is ${numberOne * numberTwo * numberThree}`)
        return [numberOne, numberTwo, numberThree]
    })
}

partOne()
partTwo()