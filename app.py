from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import paramiko
import subprocess
import select
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(request.form['host'], username=request.form['username'], password=request.form['password'])
    # return "We are connected to %s" %host
    # transport = ssh.get_transport()
    # channel = transport.open_session()
    # channel.exec_command(request.form['command'])
    stdin, stdout, stderr = ssh.exec_command(request.form['command'])
    # exit_status = stdout.channel.recv_exit_status()
    return stdout.read().strip("")

    ssh.close()
    

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
