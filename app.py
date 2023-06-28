from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'  # Folder untuk menyimpan file yang diunggah
ALLOWED_EXTENSIONS = {'csv'}  # Ekstensi file yang diizinkan

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    # Fungsi untuk memeriksa apakah ekstensi file yang diunggah valid.
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # Route untuk halaman utama
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Route untuk melakukan prediksi
    gula_darah = float(request.form['gula_darah'])
    kolesterol = float(request.form['kolesterol'])
    asam_urat = float(request.form['asam_urat'])

    if 'dataset' not in request.files:
        return jsonify({'error': 'Tidak ada file dataset yang diunggah.'})

    file = request.files['dataset']
    if file.filename == '':
        return jsonify({'error': 'Nama file dataset kosong.'})

    if not allowed_file(file.filename):
        return jsonify({'error': 'Ekstensi file dataset tidak valid. Harap unggah file CSV.'})

    filename = secure_filename(file.filename)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    uploaded_dataset = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), delimiter=";")
    X = uploaded_dataset.iloc[:, 1:4].values
    y = uploaded_dataset.iloc[:, 4].values

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)

    prediction = knn.predict([[gula_darah, kolesterol, asam_urat]])

    result = 'Sehat' if prediction[0] == 'sehat' else 'Sakit'

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'prediction': result})


if __name__ == '__main__':
    app.run(debug=True)
