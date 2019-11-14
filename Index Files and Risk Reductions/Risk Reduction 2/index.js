const ml = require('ml-regression');
const csv = require('csvtojson');
const SLR = ml.SLR;  

const csvFilePath = 'apple.csv'; // Data
let csvData = [],  
    X = [], // Input
    y = []; // Output

let regressionModel;

const readline = require('readline'); 

const rl = readline.createInterface({
    input: process.stdin, 
    output: process.stdout
});

csv()
    .fromFile(csvFilePath)
    .then((jsonObj) => {
        csvData.push(jsonObj);
    })
    .then(() => {
        dressData(); // To get data points from JSON Objects
        performRegression(); 
   });

function performRegression() {
    regressionModel = new SLR(X, y); //Trains the model
    console.log(regressionModel.toString(3));
    predictOutput();
}

function dressData() {
    csvData[0].forEach((row) => {
        X.push(f(row.Ebitda));
        y.push(f(row.EPS));
    });
}

function f(s) {
    return parseFloat(s);
}

function predictOutput() {
    rl.question('Enter input EBITDA for prediction (ctrl-c to exit) : ', (answer) => {
        console.log(`At EBITDA = ${answer}, EPS =  ${regressionModel.predict(parseFloat(answer))}`);
        predictOutput();
    });
}