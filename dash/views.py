from django.shortcuts import render, HttpResponse, redirect
import _thread
import threading
from scapy.all import *
from urllib import request as ex_request
from datetime import datetime
from .models import *

BUTTON_MAC = "38:f7:3d:74:cd:60"
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

# Starts separate thread to listen on network, while not blocking requests
def run_listener():
    print("Waiting for Signal")
    sniff(prn=arp_monitor_callback, filter="arp", store=0)

# listener, looking for mac address of specific Dash button
# Easiest way to get MAC is to use WireShark and look for Amazon in the name of Source
def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2):
        if pkt.sprintf("%ARP.hwsrc%") == BUTTON_MAC:
            if time_last_sent == None:
                call_lambda() 
                return "Initial contact"
            # Debouncing in order to avoid accidental Spam - Button sometimes pings network twice
            time_since = (datetime.now() - time_last_sent).total_seconds()
            if int(time_since) > 5:
                call_lambda()
                return "WORKED"
            else:
                print("Too many requests")

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
            print("Lamba Error")
    else:
        print("Need to assign Lambda first. Add a team")

thread = threading.Thread(target = run_listener)
thread.start()