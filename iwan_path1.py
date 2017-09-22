from flask import Flask, render_template, request, escape
from netmiko import ConnectHandler
import time 

def config_push(domain,type_traffic,preferred_path):
	ip = domain
	cisco_3945 = {'device_type':'cisco_ios_telnet','ip':ip,'username':'admin','password':'cisco'}
	net_connect = ConnectHandler(**cisco_3945)
	net_connect.config_mode()
	time.sleep(1)
	prompt = net_connect.find_prompt()
	print(prompt)
	if (type_traffic == 'http'):
		class_command = "class  " + type_traffic + " sequence 10"
	elif(type_traffic == 'voice'):
		class_command = "class  " + type_traffic + " sequence 20"
	elif(type_traffic == 'video'):
		class_command = "class  " + type_traffic + " sequence 30"
	print (class_command)
	if (preferred_path == 'mpls'):
		path_command = "path-preference mpls fallback inet"
	else:
		path_command = "path-preference inet fallback mpls"
	print (path_command)
	print ()
	config_commands = ['domain IWAN','vrf default','master hub',class_command,path_command]
	output1 = net_connect.send_config_set(config_commands)
	print (output1)
	time.sleep(2)
	output = net_connect.send_command("show run")
	print (output)
	return "Success"


app = Flask(__name__)
@app.route('/entry')
def request_page() -> 'html':
	return render_template('entry1.html',the_title="IWAN Path Change")

@app.route('/result', methods = ['POST','GET'])
def do_change() -> 'html':
    domain_ip = request.form['domain_ip']
    traffic_class = request.form['traffic_class']
    preferred_path = request.form['preferred_path']
    title = 'Submitting changes successfully:'
    final_output = config_push(domain_ip,traffic_class,preferred_path)
    return render_template('results1.html',the_title=title,traffic_class=traffic_class,preferred_path=preferred_path)

if __name__ == '__main__':
    app.run(debug=True)
