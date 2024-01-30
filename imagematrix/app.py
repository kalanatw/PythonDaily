from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image
import io

app = Flask(__name__)


photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "uploads"
configure_uploads(app, photos)

Base = declarative_base()
engine = create_engine("sqlite:///images.db")
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class ImageData(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    image_matrix = Column(LargeBinary)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and "photo" in request.files:
        photo = request.files["photo"]
        filename = photos.save(photo)
        image_matrix = convert_image_to_matrix(filename)
        save_matrix_to_database(filename, image_matrix)
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/retrieve/<int:image_id>")
def retrieve_image(image_id):
    image_data = session.query(ImageData).filter_by(id=image_id).first()
    image_matrix = image_data.image_matrix
    image = convert_matrix_to_image(image_matrix)
    return send_file(image, mimetype="image/jpeg")

def convert_image_to_matrix(filename):
    image = Image.open(f"uploads/{filename}")
    matrix = list(image.getdata())
    return matrix

def convert_matrix_to_image(matrix):
    image = Image.new("RGB", (100, 100))
    image.putdata(matrix)
    return image

def save_matrix_to_database(name, matrix):
    image_data = ImageData(name=name, image_matrix=matrix)
    session.add(image_data)
    session.commit()

if __name__ == "__main__":
    app.run(debug=True)
