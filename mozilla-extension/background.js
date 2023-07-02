// async function getCurrentTab() {
//   let queryOptions = { active: true, currentWindow: true };
//   let [tab] = await chrome.tabs.query(queryOptions);
//   return tab;
// }
// function getCurrentTab(callback) {
//   let queryOptions = { active: true, lastFocusedWindow: true };
//   chrome.tabs.query(queryOptions, ([tab]) => {
//     if (chrome.runtime.lastError)
//     console.error(chrome.runtime.lastError);
//     // `tab` will either be a `tabs.Tab` instance or `undefined`.
//     callback(tab);
//   });
// }

let urls = [];
let i=0;
function findUrl(url){
  let found;
  for(let i=0;i<url.length;i++){
    let urln=url.substring(0, url.length - i)
    found = urls.find(element => element.title == urln);
    if(found!=undefined){
      break;
    }
  }
  //const found = urls.find(element => element.title == url);
  return found;
}


// chrome.action.onClicked.addListener(async () => { 
//   let dost = await getCurrentTab();
//   chrome.notifications.create('NOTFICATION_ID', {
//     type: 'basic',
//     iconUrl: "hello.png",
//     title: 'notification title',
//     message: dost.url,
//     priority: 2
// })
// })

browser.tabs.onUpdated.addListener(async function(activeInfo,changeInfo,tab) {
    if(findUrl(tab.title) == undefined){
      if(urls.length<10){
        urls[i]=tab;
        i++;
      }
      else{
        if(i==9){
          i=0;
          urls[i]=tab;
        }
        else{
          urls[i]=tab;
          i++;
        }
      }
    }

});

var socket = io.connect('http://127.0.0.1:1337');
socket.on("tst",(argg)=>{
  const url = findUrl(argg); 
  //getCurrentTab((arg)=>{
    socket.emit("test",url?.url); 
  // })    
});

// var socket = io.connect('http://127.0.0.1:8080');
// socket.on("tst",(argg)=>{
//   //const url = findUrl(argg); 
//     socket.emit("sendText",urls);  
// });