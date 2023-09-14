import express from "express"
import mongoose from "mongoose";

const app = express();

app.use(express.json())

mongoose.connect("mongodb://127.0.0.1:27017/", {
    dbName: "Logs",
}).then(()=>console.log("Connected")).catch(console.log("Error"));

const schema = new mongoose.Schema({
    eventID: String,
    event_time: String,
    event_level: String,
    event_category: String,
    event_data: String,
    CompName: String,
    ReservedFlags: String
});
const appCollection = mongoose.model("Application_Logs", schema);

app.post("/applogs", async (req,res) =>{
    console.log("receiving")
    await appCollection.create(req.body);
    res.status(200);
});

app.get("/", (req, res) => {
    res.end("<h1>This Site is Working I Guess</h1>")
});

app.listen(5000, ()=>{
    console.log("Connected");
})
