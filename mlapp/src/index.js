import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'path';
import upload from "express-fileupload";

const app = express();

app.use(cors()); //middleware

app.get('/', (req, res) => {
  res.render('index.ejs');
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

app.post('/', (req, res) => {
  if (req.files) {
    var file = req.files.fileName,
      filename = req.file.name;
    file.mv('./upload'+filename, (err) => {
      if(err) {
        console.log(err);
        res.send("error occured");
      }
      else {
        res.send("Done");
      }
    })
  }
})



app.listen(process.env.PORT, () => {
  console.log(`Example app listening on port ${process.env.PORT}!`)
});
