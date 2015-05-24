import json
import threading
import time
import sys
import hashlib
import requests
from bson.json_util import dumps
from gevent.wsgi import WSGIServer
from gevent import sleep as gevent_sleep
from gevent import Greenlet, monkey
from pymongo import MongoClient
from flask_sslify import SSLify
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify, make_response, send_from_directory

monkey.patch_all()

# Flask
app = Flask(__name__)
app.debug = True

# sslify = SSLify(app)

client = MongoClient("mongodb", 2000)
db = client.ets
drivers = db.drivers
clients = db.clients
appointments = db.appointments


def setInterval(interval, times=-1):
    # This will be the actual decorator,
    # with fixed interval and times parameter
    def outer_wrap(function):
        # This will be the function to be
        # called
        def wrap(*args, **kwargs):
            stop = threading.Event()

            # This is another function to be executed
            # in a different thread to simulate setInterval
            def inner_wrap():
                i = 0
                while i != times and not stop.isSet():
                    stop.wait(interval)
                    function(*args, **kwargs)
                    i += 1

            t = threading.Timer(0, inner_wrap)
            t.daemon = True
            t.start()
            return stop
        return wrap
    return outer_wrap


# Site pages
@app.route("/", methods=['GET'])
def index():
    return send_from_directory(".", "index.html")


@app.route("/about.html", methods=['GET'])
def abouthtml():
    return send_from_directory(".", "about.html")


@app.route("/clients.html", methods=['GET'])
def clientshtml():
    return send_from_directory(".", "clients.html")


@app.route("/home.html", methods=['GET'])
def homehtml():
    return send_from_directory(".", "home.html")


@app.route("/managers.html", methods=['GET'])
def managershtml():
    return send_from_directory(".", "managers.html")


@app.route("/signup.html", methods=['GET'])
def signuphtml():
    return send_from_directory(".", "signup.html")


@app.route("/css/main.css", methods=['GET'])
def maincss():
    return send_from_directory("css", "main.css")


@app.route("/js/main.js", methods=['GET'])
def mainjs():
    return send_from_directory("js", "main.js")


@app.route("/login.html", methods=['GET'])
def loginhtml():
    return send_from_directory(".", "login.html")


@app.route("/api/createAppointment", methods=['POST'])
def createAppointment():
    cli_name = request.form.get("cli_name", "")
    str_cli = request.form.get("str_cli", "")
    cit_cli = request.form.get("cit_cli", "")
    sta_cli = request.form.get("sta_cli", "")
    zip_cli = request.form.get("zip_cli", "")
    cli_contact = request.form.get("cli_contact", "")
    # Apartment
    str_apt = request.form.get("str_apt", "")
    cit_apt = request.form.get("cit_apt", "")
    sta_apt = request.form.get("sta_apt", "")
    zip_apt = request.form.get("zip_apt", "")
    time_apt = request.form.get("time_apt", "")

    apt_id = appointments.insert({"street": str_cli, "city": cit_cli, "state": sta_cli, "zip": zip_cli, "time": time_apt})

    if clients.find_one({"cli_name": cli_name}) is None:
        clients.insert({"name": cli_name, "street": str_cli, "city": cit_cli, "state": sta_cli, "zip": zip_cli, "contact": cli_contact})

    driversdata = drivers.find({"active": True})
    print driversdata
    for i in driversdata:
        print i
        print zip_cli
        if  -2 <= int(zip_cli) - int(i['zip']) <= 2:
            print "Sending!"
            askDriver(i['number'], str_cli + " " + cit_cli + " " + sta_cli + " " + zip_cli, str_apt + " " + cit_apt + " " + sta_apt + " " + zip_apt, time_apt)
            i["notifiedFor"] = apt_id
            drivers.update({"_id": i["_id"]}, i)
    return jsonify(status=True)


@app.route("/api/login", methods=['POST'])
def login():
    if request.form.get("email", "") == "ineedhelp@newets.com":
        redirect_to_index = redirect(url_for('index'))
        response = app.make_response(redirect_to_index)
        response.set_cookie('loggedin',value='true')
        return response
    else:
        return redirect(url_for("index"))


@app.route("/api/logout", methods=['GET'])
def logout():
    redirect_to_index = redirect(url_for('index'))
    response = app.make_response(redirect_to_index)
    response.set_cookie('loggedin',value='false')
    return response


@app.route("/api/signup", methods=['POST'])
def signupapi():
    return redirect(url_for("index"))


#@app.route("/api/askDriver", methods=['POST'])
def askDriver(number, fromAddress, toAddress, time):
    message = "Would you be able to drive a patient from " + fromAddress + " to " + toAddress + " at " + time + "? Please send a message saying YES or NO to: 12064306832"
    length = len(message)
    strs = []
    firstmsg = message[:140]
    secondmsg = message[140:length]
    strs.append(firstmsg)
    strs.append(secondmsg)
    for i in strs:
        r = requests.post("http://textbelt.com/text", data={"number": int(number), "message": i})
        print r.text
    return jsonify(status=True)


@app.route("/api/parseMessage", methods=['GET'])
def parseMessage():
    text = request.form.get("text", "")
    if text is not "" and text.lower() is "yes":
        driverYes(request.form.get("msisdn", ""))
        return jsonify(status=True)


def driverYes(number):
    driversdata = drivers.find({"active": True})
    appt = ""
    for i in driversdata:
        if i["number"] == number:
            appt = i["notifiedFor"]
            i["appointment"] = i["notifiedFor"]

    for i in driversdata:
        del i["notifiedFor"]
        drivers.update({"_id": i["_id"]}, i)



if __name__ == "__main__":

    try:
        port_number = int(sys.argv[1])
    except:
        port_number = 8080

    """if app.config['USE_PROXYFIX']:
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)"""

    if not app.debug:
        http_server = WSGIServer(('', port_number), app)
        http_server.serve_forever()
        # app.run(host='0.0.0.0', port=port_number)
    else:
        from werkzeug.serving import run_with_reloader
        # from werkzeug.debug import DebuggedApplication

        @run_with_reloader
        def run_debug_server():
            http_server = WSGIServer(('', port_number), app)
            http_server.serve_forever()

        run_debug_server()
