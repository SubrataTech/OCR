from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from ocrmodel import ocr

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


if __name__ == '__main__':
    app.run(debug=True)
