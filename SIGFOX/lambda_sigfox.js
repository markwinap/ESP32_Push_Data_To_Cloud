/*
Author: Marco Martinez
Notes: Receive JSON POST Request from SigFox - This project was dev from Marcos Home
METHOD: POST (JSON File)
{ device: '4D58B1',
  time: '1548295119',
  duplicate: 'false',
  snr: '10.62',
  station: '792D',
  data: '001400140014001400140014',
  avgSnr: '10.60',
  lat: '21.0',
  lng: '-100.0',
  rssi: '-115.00',
  seqNumber: '7',
  results: [ 20, 20, 20, 20, 20, 20 ] }
*/


'use strict';

const AWS = require('aws-sdk');
const cloudwatch = new AWS.CloudWatch({region: 'us-east-1'});

let response = {
    statusCode: 200
};
exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    if(body.hasOwnProperty('data')){
        body.results = getResArr(body.data);
        await addCWMetrics(body).then(res => {
          console.log(res);
        });
        response.body = JSON.stringify(body);
        return response;
    }
    else{
        response.body = JSON.stringify(body);
        return response;
    }
};
async function addCWMetrics(data) {
    for(let i in data.results){
        await cloudWatchAsync({
            MetricData: [{MetricName: 'DieselMonitor', 
            Dimensions: [{ Name: data.device, Value: 'Height'}],
            Timestamp: new Date(getTime(i, data.results.length, data.time)),
            Unit: 'None',
            Value: data.results[i] }], Namespace: 'TCS' });
    } 
    return 'OK';
}

function cloudWatchAsync(params){
    return new Promise((resolve, reject) => {
        cloudwatch.putMetricData(params, function(err, data) {
            if (err){
                console.log(err, err.stack);
                reject('ERROR');
            }
            else{
                resolve(data);
            }
        });
    });
}
function getTime(pos, len, time){
    pos = parseInt(pos, 0);
    time = parseInt(time, 0);
    let newpos = len  - (pos + 1);
    let d = 0;
    if((len - 1) == pos){
        d = time;
    }
    else{
        d = time - ((newpos) * (2 * 60));
    }
    return d * 1000;
}
function getResArr(str){
    let arr = [];
    let count = 0;
    for(let i in str){
      count++;
      if(count == 4){
        arr.push(parseInt(`0x${str[i - 3]}${str[i - 2]}${str[i - 1]}${str[i]}`));
        count = 0;
      }
    }
    return arr;
  }