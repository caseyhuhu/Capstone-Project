import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'path';
import upload from 'express-fileupload';
import bodyParser from 'body-parser'
import fs from 'fs';
const app = express();
import {spawn} from 'child_process';

app.use(cors()); //middleware
app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended: true}));
app.use(upload())
app.use(express.static(__dirname + '/public'));

var directoryPath = path.join(__dirname, 'upload');
var rnnPath = path.join(__dirname, 'RNN.py');
var scraperPath = path.join(__dirname, 'scraper.py');
var clusterpath = path.join(__dirname, 'kMeans.py');

app.get('/', (req, res) => {
  var myData = [];
  var stockPrice;
  fs.readdir(directoryPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    files.forEach(function (file) {
        myData.push(file);
    });
    res.render('index.ejs', {myData, stockPrice});
  });
});

app.post('/', (req, res) => {
  var myData = [];
  fs.readdir(directoryPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    files.forEach(function (file) {
        myData.push(file);
    });
  });
  var output;
  var obj;
  
  var stockPrice = [];
  var process = spawn('python3', [rnnPath, req.body.symbol]); 
  process.stdout.on('data', function(data) {
    output = data.toString(); 
  });
  process.on('exit', () => {
    stockPrice.push(output);
    res.render('index.ejs', {myData, stockPrice});
  });
});


app.get('/about', (req, res) => {
  res.render('aboutUs.ejs');
})

app.get('/edgar', (req, res) => {
  res.render('edgar.ejs');
})

app.get('/clustering', (req, res) => {
  res.render('clustering.ejs');
})

app.post('/clustering', (req, res) => {
  var process = spawn('python3', [clusterpath]);
  process.stdout.on('data', function(data) { 
    console.log(data.toString());
  }); 
  process.on('exit', () => {
    res.render('clustering.ejs');
  });
})

app.post('/scraping', (req, res) => {
  var process = spawn('python3', [scraperPath, req.body.symbol]); 
  process.stdout.on('data', function(data) { 
    console.log(data.toString());
  }); 
  process.on('exit', () => {
    res.render('clustering.ejs');
  });
})

app.get('/upload', (req, res) => {
  var myData = [];
  fs.readdir(directoryPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    files.forEach(function (file) {
        myData.indexOf(file) === -1 ? myData.push(file) : null;
      });
    res.render('upload.ejs', {myData});
  });
})

app.post('/upload', (req, res) => {
  if (req.files) {
    var file = req.files.filename,
      filename = file.name;
    // if (path.extname(filename) != '.csv') {
    //   res.end();
    // }
    file.mv('./src/upload/'+filename, (err) => {
      if(err) {
        console.log(err);
        res.send("The file failed to upload");
      }
      else {
          var myData = [];
          fs.readdir(directoryPath, function (err, files) {
          if (err) {
              return console.log('Unable to scan directory: ' + err);
          } 
          files.forEach(function (file) {
              myData.indexOf(file) === -1 ? myData.push(file) : null;
          });
          res.render('upload.ejs', {myData});
        });      
      }
    })
  }
})

app.post('/reset', (req, res) => {
  fs.copyFile(__dirname+'/clusters_original.txt', __dirname+'/clusters.txt', (err) => {
  if (err) throw err;
  console.log('source.txt was copied to destination.txt');
  });
  fs.copyFile(__dirname+'/Stock_data_original.csv', __dirname+'/Stock_data.csv', (err) => {
    if (err) throw err;
  console.log('Stock_data_original.csv was copied to Stock_data.csv');
  });
});

app.listen(3000, () => {
  console.log('Example app listening on port 3000')
});
