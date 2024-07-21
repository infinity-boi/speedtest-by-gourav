from flask import Flask, render_template, Response
import json
import time
import speedtest
app = Flask(__name__)


def generate_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()

    # Ping
    ping = st.results.ping
    yield f"data:{json.dumps({'type': 'ping', 'value': ping})}\n\n"
    time.sleep(1)

    # Download speed
    download_speed = st.download()
    yield f"data:{json.dumps({'type': 'download', 'value': download_speed / 1_000_000})}\n\n"
    time.sleep(1)

    # Upload speed
    upload_speed = st.upload()
    yield f"data:{json.dumps({'type': 'upload', 'value': upload_speed / 1_000_000})}\n\n"

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/speedtest')
def run_speedtest():
    return Response(generate_speedtest(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True)

