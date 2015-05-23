var request = require('request');
var express = require('express');

exports.askDriver = function(req, res) {
    request.post('http://textbelt.com/text').form({
        number: req.query.number,
        message: "Would you be able to drive a patient from " + req.query.fromaddress + " to " + req.query.toaddress + " at " + req.query.time + "? Please send a message saying YES or NO to: 12064306832"
    });
    res.status(200);
    res.send({status: true});
}

exports.parseMessage = function(req, res) {
    if(req.query.text && req.query.text.toLowerCase() == "yes") {
        //forward req.query.msisdn
        res.send({status: true});
    }
    res.status(200);
    res.send({status: false});
}

exports.createNewResident = function(req, res) {

}

exports.createNewDriver = function(req, res) {

}

exports.logUserIn = function(req, res) {

}
