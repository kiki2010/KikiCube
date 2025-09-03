''' 
02/09/2025
Chiara Catalini
Camera Stream
'''
import eventlet 
eventlet.monkey_patch()
from flask import Flask, render_template, jsonify, Response
from flask_socketio import SocketIO
import cv2
import base64
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
camera.set(cv2.CAP_PROP_FPS, 15)

thread = None
thread_lock = threading.Lock()

def capture_frames():
    print('Capture thread started')
    while True:
        success, frame = camera.read()
        if not success:
            socketio.sleep(0.1)
            continue

        ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if not ret:
            socketio.sleep(0.05)
            continue

        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        socketio.emit('video_frame', jpg_as_text)
        socketio.sleep(0.05)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snapshot')
def snapshot():
    success, frame = camera.read()
    if not success:
        return jsonify({'error': 'no frame'}), 500
    ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
    return Response(buffer.tobytes(), mimetype='image/jpeg')

@socketio.on('connect')
def handle_connect():
    global thread
    print('connected')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(capture_frames)
            print('Background capture task launched')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')