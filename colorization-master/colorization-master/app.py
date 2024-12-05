from flask import Flask, request, jsonify, render_template, send_file
import os
from werkzeug.utils import secure_filename
from colorizers import eccv16, siggraph17, load_img, preprocess_img, postprocess_tens
import torch
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/outputs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load colorizers
colorizer_eccv16 = eccv16(pretrained=True).eval()
colorizer_siggraph17 = siggraph17(pretrained=True).eval()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform colorization
        img = load_img(filepath)
        tens_l_orig, tens_l_rs = preprocess_img(img, HW=(256, 256))
        out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

        # Save outputs
        eccv16_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{filename}_eccv16.png')
        siggraph17_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{filename}_siggraph17.png')
        plt.imsave(eccv16_path, out_img_eccv16)
        plt.imsave(siggraph17_path, out_img_siggraph17)

        return jsonify({
            'eccv16': eccv16_path,
            'siggraph17': siggraph17_path
        })

if __name__ == '__main__':
    app.run(debug=True)
