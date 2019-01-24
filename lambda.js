exports.handler = (event, context, callback) => {
    let body = JSON.parse(event.body);
    body.results = getResArr(body.data);
    // TODO implement
    const response = {
        statusCode: 200,
        body: JSON.stringify(body),
    };
    callback(null, response);
};
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