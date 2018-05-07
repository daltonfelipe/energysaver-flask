from app import mqtt, socketio, app
from app.models.data import Data
from json import loads
from flask_socketio import emit
from flask import send_file
import datetime



def save_data(msg):
    data = Data()
    data.user = msg.get('user')
    data.local = msg.get('local')
    data.device = msg.get('device')
    data.day = msg.get('day')
    data.hour = msg.get('hour')
    data.name_sensor = msg.get('name_sensor')
    data.type_sensor = msg.get('type_sensor')
    data.model_sensor = msg.get('model_sensor')
    data.value = msg.get('value')
    data.save()


@mqtt.on_connect()
def mqtt_on_connect(client, userdata, flags, rc):
    pass
    #mqtt.unsubscribe_all()
    #print('Fazendo subscribe!\n')
    #mqtt.subscribe('Tapajos-IoT')

@mqtt.on_disconnect()
def mqtt_on_disconnect():
    print('\nDesconectando, fazendo unsubscribe!\n')
    mqtt.unsubscribe_all()
    

@mqtt.on_message()
def on_message(client, userdata, message):
    msg = loads(message.payload.decode())
    save_data(msg)
    socketio.emit('received-data',msg)


def create_data_csv(data_query,file):
    with open(file,'w') as data_file:
        data_file.write('user,local,device,day,hour,name_sensor,type_sensor,model_sensor,value\n')
        for data_q in data_query:
            data_file.write('{user},{local},{device},{day},{hour},{name_sensor},{type_sensor},{model_sensor},{value}\n'.format(
                user=data_q.user,
                local=data_q.local,
                device=data_q.device,
                day=data_q.day,
                hour=data_q.hour,
                name_sensor=data_q.name_sensor,
                type_sensor=data_q.type_sensor,
                model_sensor=data_q.model_sensor,
                value=data_q.value
            ))

 
file = 'data.csv'
@app.route('/download/'+file)
def download_data():
    return send_file('/home/dalton/projetos/python/energysaver/%s'%file)