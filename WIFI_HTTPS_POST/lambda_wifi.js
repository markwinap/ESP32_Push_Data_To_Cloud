'use strict';

const AWS = require('aws-sdk');
const cloudwatch = new AWS.CloudWatch({region: 'us-east-1'});

let response = {
    statusCode: 200
};
exports.handler = async (event) => {
    let body = strArr(event.body);
    console.log(body)
    await addCWMetrics(body).then(res => {
      console.log(res);
    });
    response.body = JSON.stringify(body);
    return response;
};
async function addCWMetrics(data) {
    for(let i in data){
        await cloudWatchAsync({
            MetricData: [{MetricName: 'DieselMonitor', 
            Dimensions: [{ Name: 'Pycom', Value: 'Height'}],
            Timestamp: new Date(getTime(i, data.length, new Date().getTime())),
            Unit: 'None',
            Value: data[i] }], Namespace: 'TCS' });
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
        d = time - ((newpos) * 10000);
    }
    return d;
}
 function strArr(str){
  let res = [];
  str = str.slice(0, -1);
  let arr = str.split(',');
  for(let i in arr){
    res.push(parseInt(arr[i]));
  }
  return res;
}