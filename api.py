import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask, request, redirect, render_template
import urllib.request


def get_shell_script_output_using_communicate(rawtx, blindingkey):
    session = subprocess.Popen(['./unblind.py', rawtx, blindingkey], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception("Error "+str(stderr))
    return stdout.decode('utf-8')



app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        txid = request.form['txid']
        blindingkey = request.form['blindingkey']
        rawtx = urllib.request.urlopen("https://blockstream.info/liquid/api/tx/"+ txid +"/hex").read()
        print(txid)
        return '<pre>'+get_shell_script_output_using_communicate(rawtx, blindingkey)+'</pre>'   

if __name__ == "__main__":
    app.run(host='0.0.0.0:5000')
