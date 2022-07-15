from datetime import datetime
import time
from flask import Flask, Response, render_template, request, redirect
import containers

app = Flask(__name__,static_folder='assets',template_folder='pages')

global console_output  
console_output = 'ADG_DOCKER_ENGINE : Awaiting Jobs'

@app.route('/')
def index():
    return render_template('dashboard.html',title='Dashboard')

@app.route('/apps')
def apps():
    return 'oh no im still on construction'

@app.route('/deployimage',methods=['POST'])
def deployimage():
    if request.data:
        data = request.get_json()
        if data:
            imagename = data['DockerImage']
            imageport = data['PortNumberOfImage']
            labport =  data['PortNumberToBeDeployed']
            global console_output
            output = containers.RunContainer(imagename,imageport,labport)
            console_output = str(output)
            return output
            

@app.route('/vm')
def vm():
    return 'oh no im still on construction'

@app.route('/killcontainer',methods=['POST'])
def killcontainer():
      if request.data:
            data = request.get_json()
            containerid = data['containerid']       
            global console_output       
            console_output = str(containers.KillContainer(containerid))
            return dict(console_output)

@app.route('/console_feed')
def console_feed():
    def generate():
            global console_output         
            yield datetime.now().strftime("%Y.%m.%d|%H:%M:%S") +" | "+console_output
    return Response(generate(), mimetype='text') 


@app.route('/runcontainer',methods=['POST'])
def runcontainer():
        if request.data:
                data = request.get_json()
                imagename = data['imagename']
                imageport = data['imageport']
                labport = data['labport']
                global console_output  
                console_output = str(containers.RunContainer(imagename,imageport,labport))
                return dict(console_output)



@app.route('/docker')
def docker():
    return render_template('docker.html',title='Docker',containers=containers.ShowRunningContainers())

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)    
    