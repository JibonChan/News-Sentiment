//jshint esversion:6

const express = require("express");
const bodyParser = require("body-parser");
const {spawn} = require('child_process');

// Global Variable
var SEARCH_HISTORY = [];
var SEARCH_RESULT = "";

const app = express();
app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static("public"));



app.get("/", function(req, res){
    res.render('home', {search_result: SEARCH_RESULT, search_query: SEARCH_HISTORY[SEARCH_HISTORY.length -1]});
});
app.post("/", function(req, res){
    let query = req.body.query;
    if ((SEARCH_HISTORY.includes(query)) === false) {
        SEARCH_HISTORY.push(query);
        // spawn new child process to call the python script
        const use_python = __dirname + '/pytEnv/bin/python';
        const script_name = __dirname + '/python_scrapper/actual-crawler.py'
        const python = spawn(use_python, [script_name, query]);
        // collect data from script
        python.stdout.on('data', function (data) 
        {
            console.log('Pipe data from python script ...');
            dataToSend = data.toString();
            SEARCH_RESULT = data;
        });
        // in close event we are sure that stream from child process is closed
        python.on('close', (code) => 
        {
            console.log(`child process close all stdio with code ${code}`);
            res.redirect('/');
        });
    }
    console.log('New Query: ', SEARCH_HISTORY);
    
});

app.listen(3000, function() {
    console.log("Server started and listening on port 3000...");
});