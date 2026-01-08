
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World!\n');
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
});

const RulesEngine = require("./core/engine")

const ourForm = {
  wakeTime: 300,
  readCode: 1
}
//initiate the engine 
const engine = new RulesEngine()

//call a method to send the data 
const result = engine.receiveForm(ourForm)

//log the response 
console.log("Engine Returned:", result)
