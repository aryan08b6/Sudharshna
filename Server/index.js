const {MongoClient} = require('mongodb');
const express = require('express');

const app = express()
const url = 'mongodb://127.0.0.1:27017';
const client = new MongoClient(url)
const dbName = 'logs';

let db;
async function main(){
    await client.connect();
    console.log("Connected  Succesfully")
    db = client.db(dbName)
}

main();

app.use(express.json())

app.listen(5000, ()=>{
    console.log("Server Running");
})

app.get('/', (req, res)=>{
    res.end("<a href='/page1'>Added Logs</a> <a href=/page2>Anomalies</a>")
})

app.get('/page1', (req, res)=>{
    res.end("Karta Hun Isse Abhi")
})

app.get('/page2', (req, res)=>{
    res.end("Karta Hun Isse Abhi")
})

app.get('/timeGap', async (req, res) => {
    console.log("Received Request")
    const locationId = req.query.LOCATIONID;
    const collection = db.collection('Gaps')
    const findResult = await collection.find({gapType:"logUpdateGap", locationId:{ $eq: locationId }}).toArray();
    const timeGap = findResult.gap;
    console.log(findResult)
  
    res.json(1);
  });

app.post('/logPush', async (req, res) => {
    const jsonData = req.body;
    res.sendStatus(200);
  });

app.post('/timeUpdate', async (req, res) => {
    const jsonData = req.body;
    res.sendStatus(200);
  });

app.get('/time', async (req, res) => {
    const param = req.query.PARAM;
    const locationId = req.query.LOCATIONID;
    const systemId = req.query.SYSTEMID;
    const collection = db.collection('UpdateTimes')
    res.end();
  });

  

