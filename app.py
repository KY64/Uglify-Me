import os
from flask import Flask, request, redirect, url_for, render_template
from mail import SendMail
from threading import Thread

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024 # Limit file size to 8 MB
app.config["UPLOAD_FOLDER"] = "./static/uploads/"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
password = os.environ['SPICY']

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    if "file" not in request.files:
        return "Please upload an image"
    file = request.files["file"]
    if file.filename == '':
        return "No image found"
    if file and allowed_file(file.filename):
        image_format = file.filename.split('.')[1]
        filename = f"image.{image_format}"
        path = f"static/uploads/image.{image_format}"
        file.save(path)
        os.system(f"./processor/DisplayImage {path}")
        content = {
            "sender_email" : os.environ['SENDER_EMAIL'],
            "receiver_email" : request.form["email"],
            "subject" : "Uglified Photo",
            "body" : "Hey, congratulations for uglifying your photo!! ((:",
            "directory" : "static/uploads/",
            "filename" : "result.jpeg",
            "password" : password
        }
        Thread(target=SendMail, args=(content,)).start()
        return render_template("upload.html", filename="result.jpeg")
    else:
        return "Allowed image types are JPG, JPEG, and PNG"

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'], debug=False)
