import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'path';
import upload from 'express-fileupload';
import bodyParser from 'body-parser'
import fs from 'fs';

const app = express();

app.use(cors()); //middleware
app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({extended: true}));
app.use(upload())

var directoryPath = path.join(__dirname, 'upload');


app.get('/', (req, res) => {
  var myData = [];
  fs.readdir(directoryPath, function (err, files) {
    //handling error
    if (err) {
        return console.log('Unable to scan directory: ' + err);
    } 
    //listing all files using forEach
    files.forEach(function (file) {
        // Do whatever you want to do with the file
        myData.push(file);
    });
    res.render('index.ejs', {myData});
  });
});

app.get('/about', (req, res) => {
  res.render('aboutUs.ejs');
})

app.get('/edgar', (req, res) => {
  res.render('aboutEdgar.ejs');
})

app.get('/upload', (req, res) => {
  res.render('upload.ejs');
})

app.post('/upload', (req, res) => {
  if (req.files) {
    var file = req.files.filename,
      filename = file.name;
    file.mv('./src/upload/'+filename, (err) => {
      if(err) {
        console.log(err);
        res.send("The file failed to upload");
      }
      else {
        res.render('upload.ejs');
      }
    })
  }
})

app.listen(process.env.PORT, () => {
  console.log(`Example app listening on port ${process.env.PORT}!`)
});
