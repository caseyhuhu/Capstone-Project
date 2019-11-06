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

var directoryPath = path.join(__dirname, 'upload');
var pythonPath = path.join(__dirname, 'RNN.py');

app.get('/', (req, res) => {
  var myData = [];
  fs.readdir(directoryPath, function (err, files) {
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    files.forEach(function (file) {
        myData.push(file);
    });
    res.render('index.ejs', {myData});
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
  var process = spawn('python3', [pythonPath]); 
  process.stdout.on('data', function(data) { 
    console.log(data.toString());
  }) 
  res.send('RMSE Value:')
});

app.get('/about', (req, res) => {
  res.render('aboutUs.ejs');
})

app.get('/edgar', (req, res) => {
  res.render('aboutEdgar.ejs');
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

app.listen(3000, () => {
  console.log('Example app listening on port 3000')
});
