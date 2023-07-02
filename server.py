import socketio
import time
from aiohttp import web
from engineio.async_drivers import aiohttp
sio = socketio.AsyncServer(async_mode='aiohttp',cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


@sio.on('connect')
async def connect(sid, environ):
    print('connect ', sid)
      
@sio.on('pyts')
async def my_custom_event(sid,data2):
    print(data2)
    await sio.emit("tst",data2)


@sio.on('test')
async def my_custom_event(sid, data1):
    print(data1)
    if data1 != None:
        await sio.emit('mymessage',data1)
    else:
        await sio.emit('mymessage',"")             

def run():    
    web.run_app(app,host='127.0.0.1',port=1337)
