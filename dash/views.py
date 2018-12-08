from django.shortcuts import render, HttpResponse, redirect
import _thread
import threading
from scapy.all import *
from urllib import request as ex_request
from datetime import datetime
from .models import *

time_last_sent = None
current_lambda = ""

# Create your views here.
def index(request):
    context = { 
        "projects" : Project.objects.all(),
        "bound_ep" : current_lambda
    }
    return render(request, "dash/index.html", context)

def add_project(request):
    Project.objects.create(name = request.POST['proj_name'], lambda_ep = request.POST['new_ep'])
    return redirect('/')

def test_ep(request, p_id):
    p = Project.objects.get(id = p_id)
    try:
        ex_request.urlopen(p.lambda_ep)
    except:
        print("Error when accessing URL. Lambda Side.")
    return redirect('/')

def bind_ep(request, p_id):
    global current_lambda
    current_lambda = Project.objects.get(id = p_id).lambda_ep
    return redirect('/')

def delete_ep(request, p_id):
    Project.objects.get(id = p_id).delete()
    return redirect('/')

################## Utilities ##################

# Starts separate thread to listen on network
def run_listener():
    print("Waiting for Signal")
    sniff(prn=arp_monitor_callback, filter="arp", store=0)

# listener, looking for mac address of button
def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2):
        if pkt.sprintf("%ARP.hwsrc%") == "38:f7:3d:74:cd:60":
            if time_last_sent == None:
                call_lambda() 
                return "First one worked"
            time_since = (datetime.now() - time_last_sent).total_seconds()
            if int(time_since) > 5:
                call_lambda()
                return "WORKED"
            else:
                print("Too many")

# triggers the lamda function when called by the listener
def call_lambda():
    global time_last_sent
    global current_lambda
    if current_lambda != "":
        time_last_sent = datetime.now()
        print("Calling Lambda: ", current_lambda)
        try:
            ex_request.urlopen(current_lambda)
        except:
            print("Double check your url")
    else:
        print("Need to assign Lambda first. Add a team")

thread = threading.Thread(target = run_listener)
thread.start()