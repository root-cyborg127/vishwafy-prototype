from flask import Flask, render_template, request, jsonify
import subprocess
import threading 
import os
import threading
import time
import Sleep
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from flask import redirect, url_for
from flask import render_template_string


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    # Start SpotDL in a separate thread
    threading.Thread(target=start_spotdl, args=(url,)).start()
    sleep(1)
    # Redirect to the downloading page
    return redirect(url_for('downloading_page'))

def start_spotdl(url):
    global log_queue, download_lock
    with download_lock:
        log_queue = []  # Clear previous logs
    process = subprocess.Popen(['spotdl', url, '-o', download_directory], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        with download_lock:
            log_queue.append(line)
    process.wait()
    if process.returncode == 0:
        # Successful download
        # Redirect to the downloading page
        return redirect(url_for('downloading_page'))
    else:
        # Failed download
        error_message = result[1].strip() if result[1] else result[0].strip()
        return redirect(url_for('error_page', error_message=error_message))

# Assuming you have the routes defined for downloading_page and error_page
@app.route('/downloading_page')
def downloading_page():
    # Render the downloading page with animations
    return render_template('downloading_page.html')

@app.route('/error_page')
def error_page():
    # Render the error page
    return render_template('error_page.html')
if __name__ == '__main__':
    app.run(debug=True)
