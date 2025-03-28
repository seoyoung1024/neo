var express = require('express');
var mysql = require('mysql');
const env = require('dotenv').config({ path: "../../.env" });
var app = express();

var connection = mysql.createConnection({
    host: process.env.host,
    user: process.env.user,
    password: process.env.password,
    database: process.env.database
});

connection.connect(function (err) {
    if (!err) {
        console.error('Database is connected!!\n\n');
    } else {
        console.log('Error connectiong Database!\n\n');
    }
});

app.get('/', function (req, res) {
    connection.query('select * from st_info', function (err, rows, fields) {
        connection.end();
        if (err) {
            res.send(rews);
            console.log("The solution is :", rows);
        }else{
            console.log("Error while performing Query.");
        }
    })
})

app.listen(8000, function () {
    console.log("8000 Port : Server Started!!!!");
})