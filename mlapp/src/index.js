import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import path from 'path';

const app = express();

app.use(cors()); //middleware

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname+'/index.html'));
});

app.get('/about', (req, res) => {
  res.sendFile(path.join(__dirname+'/about.html'));
})

app.get('/edgar', (req, res) => {
  res.sendFile(path.join(__dirname+'/edgar.html'));
})


app.listen(process.env.PORT, () => {
  console.log(`Example app listening on port ${process.env.PORT}!`)
});
