from flask import Flask, render_template, request, Response
from flask_uploads import UploadSet, configure_uploads, IMAGES
from ocrmodel import ocr
from camera import VideoCamera
import cv2

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)


@app.route('/')
def hello_world():
    return upload()


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        file_name = photos.save(request.files['photo'])
        path = 'uploads/{}'.format(file_name)
        print("path : ", path)
        return ocr(path)
    return render_template('index.html')


# Face detection code

@app.route('/recog')
def index():
    return render_template('face_detection.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed_url')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop', methods=['POST', 'GET'])
def stop():
    if request.method == 'POST':
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True)
