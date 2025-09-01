import os
from flask import Flask, flash, redirect, request, render_template, session, url_for
from PIL import Image
import numpy as np
import tensorflow as tf

FLAG = os.environ.get("FLAG", "fwectf{fake_flag}")
IMG_HEIGHT, IMG_WIDTH = 224, 224
ORIGINAL_IMAGE_PATH = 'image.jpg'
TARGET_CLASS_ID = 101 
MSE_THRESHOLD = 0.05

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024  # 100KB

def preprocess_image(img):
    img = img.convert('RGB').resize((IMG_HEIGHT, IMG_WIDTH))
    img_array = np.array(img)
    preprocessed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return tf.convert_to_tensor(preprocessed_img, dtype=tf.float32)

original_image = Image.open(ORIGINAL_IMAGE_PATH)
original_image_tensor = preprocess_image(original_image)
model = tf.keras.applications.MobileNetV2(weights="imagenet")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try: 
            file = request.files['file']
            image = Image.open(file.stream)
            image_tensor = preprocess_image(image)
            if image_tensor is None:
                return render_template("login.html")
            
            mse = tf.reduce_mean(tf.square(original_image_tensor - image_tensor))
            if mse.numpy() > MSE_THRESHOLD:
                flash(
                    f"[-] AUTH FAILED (Stage 1): Image is too different from the original.\n"
                    f"    MSE: {mse.numpy():.4f} > Threshold: {MSE_THRESHOLD}\n"
                )
                return render_template("login.html")
            
            prediction = model.predict(np.expand_dims(image_tensor, axis=0), verbose=0)
            predicted_class_id = np.argmax(prediction[0])
            
            if predicted_class_id == TARGET_CLASS_ID:
                session["is_admin"] = True
                return redirect(url_for("index"))
            decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(prediction, top=1)[0]
            predicted_class_name = decoded_preds[0][1]
            flash(
                f"[-] AUTH FAILED (Stage 2): Image was not classified as the target class.\n"
                f"    Predicted as: '{predicted_class_name}' (ID: {predicted_class_id})\n"
            )
        except Exception as e:
            flash(f"Error occured: {e}")
    return render_template("login.html")



@app.route("/")
def index():
    if not session.get("is_admin"):
        return redirect(url_for("login"))
    return render_template("index.html", flag=FLAG)