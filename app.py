from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
import cv2 as cv
import numpy as np
from io import BytesIO
import base64

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

threshold =[]

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''def normalize(values):
    """Normalize the values to be between 0 and 1."""
    max_value = max(values)
    if max_value == 0:
        return values
    return [v / max_value for v in values]
'''

def compare_with_threshold(color_values, thresholded):
    """Compare the color values with the threshold."""
    #scaled_values = color_values.copy()
    #scaled_values[2] = color_values[2] * scaling_factor + bias  # Scale and apply bias to blue color
    print(color_values)
    print(thresholded)
    prob = 0
    if (thresholded[0] - color_values[0]) > 18:
        prob += 0.25
    if (thresholded[1] - color_values[1]) > 18:
        prob += 0.25
    if (thresholded[2] - color_values[2]) > 18:
        prob += 0.5
    if prob >= 0.5:
        return ("Contamination may be there please do not drink")
    if prob < 0.5:
        return ("Clean Water")


'''def calibrate(filename, operation):
    if operation == "0":
            shape = image.shape
            r_dist = []
            b_dist = []
            g_dist = []
            i_dist = []
            for i in range(shape[1]):
                b_val = np.mean(image[:, i][:, 0])
                g_val = np.mean(image[:, i][:, 1])
                r_val = np.mean(image[:, i][:, 2])
                i_val = (r_val + b_val + g_val) / 3

                r_dist.append(r_val)
                g_dist.append(g_val)
                b_dist.append(b_val)
                i_dist.append(i_val)

            r_max = max(r_dist)
            g_max = max(g_dist)
            b_max = max(b_dist)

            threshold=[r_max, g_max, b_max]
            threshold=normalize(threshold)
'''


def process(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")

    image = cv.imread(f"uploads/{filename}")
    scaling_factor = 1.5  # Adjust for blue color
    bias = 20  # Adjust for blue color
    #threshold = []
    text = "None"
    colo=[0,0,0]

    if operation == "1":
        shape = image.shape
        r_dist = []
        b_dist = []
        g_dist = []
        i_dist = []
        for i in range(shape[1]):
            b_val = np.mean(image[:, i][:, 0])
            g_val = np.mean(image[:, i][:, 1])
            r_val = np.mean(image[:, i][:, 2])
            i_val = (r_val + b_val + g_val) / 3

            r_dist.append(r_val)
            g_dist.append(g_val)
            b_dist.append(b_val)
            i_dist.append(i_val)

        r_max = max(r_dist)
        g_max = max(g_dist)
        b_max = max(b_dist)

        global threshold 
        threshold = [r_max, g_max, b_max]
        #threshold = normalize(threshold)

    if operation == "2":
        shape = image.shape
        r_dist = []
        b_dist = []
        g_dist = []
        i_dist = []
        for i in range(shape[1]):
            b_val = np.mean(image[:, i][:, 0])
            g_val = np.mean(image[:, i][:, 1])
            r_val = np.mean(image[:, i][:, 2])
            i_val = (r_val + b_val + g_val) / 3

            r_dist.append(r_val)
            g_dist.append(g_val)
            b_dist.append(b_val)
            i_dist.append(i_val)

        r_max = max(r_dist)
        g_max = max(g_dist)
        b_max = max(b_dist)

        colo = [r_max, g_max, b_max]
        #colo = normalize(colo)
        text = compare_with_threshold(colo, threshold)

        print(colo, threshold)

        '''if max(r_max, g_max, b_max) >= threshold:
            processedText = "The sample does not have impurities."
            print(processedText)
            print(max(r_max, g_max, b_max))
        elif max(r_max, g_max, b_max) < threshold:
            processedText = "The sample has impurities."
            print(processedText)
            print(max(r_max, g_max, b_max))'''

    else:
        print("Default")

    return text, colo, threshold


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/analyse', methods=["GET", "POST"])
def analyse():
    if request.method == 'POST':
        operation = request.form.get("op")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "Error!"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "No File Selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = "Calibrated"
            color = [0,0,0]
            threshol=[0,0,0]
            text, color, threshol = process(filename, operation)
            return render_template("index.html", processedText=text, intensityRed=color[0], intensityGreen=color[1], intensityBlue=color[2],tRed=threshol[0],tGreen=threshol[1], tBlue=threshol[2])

    return render_template("index.html")


app.run(debug=True)
