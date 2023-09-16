const {MongoClient} = require('mongodb');
const express = require('express');
const { spawn } = require('child_process');


const app = express()
const url = 'mongodb://127.0.0.1:27017';
const client = new MongoClient(url)
const dbName = 'Logs';

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

app.get('/time', async (req, res) => {
  console.log("Received Request")
  const param = req.query.PARAM;
  const locationId = req.query.LOCATIONID;
  const systemId = req.query.SYSTEMID;
  const collection = db.collection('UpdateTimes')
  const findResult = await collection.find({SYSTEMID:systemId, locationId:{ $eq: locationId }}).toArray();
  res.json(findResult);
});



app.get('/timeGap', async (req, res) => {
    console.log("Received Request")
    const locationId = req.query.LOCATIONID;
    const collection = db.collection('Gaps')
    const findResult = await collection.find({gapType:"logUpdateGap", locationId:{ $eq: locationId }}).toArray();
    const timeGap = findResult.gap;
    console.log(findResult)
    res.json(timeGap);
  });

app.post('/logPush', async (req, res) => {
    const jsonData = req.body;
    appLogs = JSON.parse(jsonData.Application)
    secLogs = JSON.parse(jsonData.Security)
    sysLogs = JSON.parse(jsonData.System)
    setLogs = JSON.parse(jsonData.Setup)
    forLogs = JSON.parse(jsonData.ForwardedEvents)
    const appLog = db.collection('ApplicationLogs')
    const secLog = db.collection('SecurityLogs')
    const sysLog = db.collection('SystemLogs')
    const setLog = db.collection('SetupLogs')
    const forLog = db.collection('ForwardedEvents')
    await appLog.insertMany(appLogs)
    await secLog.insertMany(secLogs)
    await sysLog.insertMany(sysLogs)
    await setLog.insertMany(setLogs)
    await forLog.insertMany(forLogs)
    const pythonProcess = spawn('python', ['--arg1=SYSTEMID', '--arg2=LOCATIONID']);
    const output = await pythonProcess.stdout.read();
    const addAnomalies = (output) =>{
      console.log("Added Anomalies to MongoDB")
    }
    addAnomalies(output)
    res.sendStatus(200);
  });

app.post('/timeUpdate', async (req, res) => {
    const jsonData = req.body;
    db.UpdateTimes.updateOne({SYSTEMID: jsonData.SYSTEMID, LOCATIONID: jsonData.LOCATIONID, Time: {$set : {Time: jsonData.Time}}})
    res.sendStatus(200);
  });
