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
var uploadPath = path.join(__dirname, 'csv_combiner.py')

app.get('/', (req, res) => {
  var stockPrice;
  res.render('index.ejs', {stockPrice});
});

app.post('/', (req, res) => {
  var output;
  var obj;

  fs.copyFile(__dirname+'/clusters_original.txt', __dirname+'/clusters.txt', (err) => {
    if (err) throw err;
    console.log('source.txt was copied to destination.txt');
  });
  fs.copyFile(__dirname+'/Stock_data_original.csv', __dirname+'/Stock_data.csv', (err) => {
    if (err) throw err;
    console.log('Stock_data_original.csv was copied to Stock_data.csv');
  });

  var stockPrice = [];
  var process = spawn('python3', [scraperPath, 'Combined_data_user_input.csv']);  //scraping process
  process.stdout.on('data', function(data) {
    output = data.toString(); 
  });
  process.on('exit', () => {
    console.log('scraped combined user input')
  });

  var process = spawn('python3', [clusterpath]); //clustering process
  process.stdout.on('data', function(data) { 
    console.log(data.toString());
  }); 
  process.on('exit', () => {
    console.log('clustered data');
  });
  var process = spawn('python3', [rnnPath, req.body.symbol]); //rnn process
  console.log('spawned')
  process.stdout.on('data', function(data) {
    output = data.toString(); 
  });
  process.on('exit', () => {
    stockPrice.push(output);
    res.render('index.ejs', {stockPrice});
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
  console.log(req.body);
  if (req.files) {
    var file = req.files.filename,
      filename = file.name;
    file.mv('./src/upload/'+filename, (err) => {
      if(err) {
        console.log(err);
      }
    });
    var process = spawn('python3', [uploadPath, filename]); 
    process.stdout.on('data', function(data) { 
      console.log(data.toString());
    }); 
    process.on('exit', () => {
      res.render('upload.ejs');
    });  
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
  res.render('clustering.ejs');
});

app.listen(3000, () => {
  console.log('Example app listening on port 3000')
});
