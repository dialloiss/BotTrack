var app = require('http').createServer(handler).listen(1337);
var io = require('socket.io').listen(app);
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
function handler(req,res){
    console.log(req.url);
    res.writeHead(200, {'Content-Type':'text/plain'});
    res.end('Hello Node\n You are really really awesome!');
}

io.sockets.on('connection',function(socket){    
    console.log("sdafasdf")
    socket.on("pyts",(requ)=>{
      console.log(requ)
      io.sockets.emit("tst",requ);
    })
    socket.on("test",(data)=>{
      console.log(data)
      io.sockets.emit('mymessage',data);
  })
}); 

