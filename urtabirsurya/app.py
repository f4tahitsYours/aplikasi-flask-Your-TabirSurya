from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import tempfile
import logging

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Memuat model klasifikasi gambar tanpa compile
image_model = load_model(r'C:\Users\user\Documents\urtabirsurya\model\skin_type_model_baru.h5', compile=False)

# Compile ulang model dengan optimizer yang kompatibel
image_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# List rekomendasi jenis kulit
recommendations = {
    'kering': 'Gunakan sunscreen dengan sifat melembabkan.',
    'berminyak': 'Gunakan sunscreen yang bebas minyak dan non-komedogenik.',
    'normal': 'Gunakan sunscreen spektrum luas yang cocok untuk semua jenis kulit.'
}

# Dimensi gambar
IMG_HEIGHT = 299
IMG_WIDTH = 299

# Fungsi untuk pra-pemrosesan gambar
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    x = img_to_array(img) / 255.0
    x = np.expand_dims(x, axis=0)
    return x

# Halaman utama untuk uji API
@app.route('/')
def home():
    return render_template('home.html')

# Rute untuk ngurusin prediksi jenis kulit sama rekomendasi produk
@app.route('/hasil prediksi', methods=['POST'])
def predict_skin_type_and_recommend():
    try:
        file = request.files.get('file')
        if file and file.filename != '':
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                file_path = tmp_file.name
                file.save(file_path)

            try:
                # Pra-pemrosesan gambar
                image_tensor = preprocess_image(file_path)

                # Prediksi jenis kulit
                predictions = image_model.predict(image_tensor)
                skin_type_index = np.argmax(predictions, axis=1)[0]
                skin_types = ['berminyak', 'kering', 'normal']
                skin_type = skin_types[skin_type_index]

                # Rekomendasi produk
                recommendation = recommendations[skin_type]

                # Probability for each skin type
                probabilities = {skin_types[i]: float(predictions[0][i]) for i in range(len(skin_types))}

                return jsonify({
                    'skin_type': skin_type,
                    'probabilities': probabilities,
                    'recommendation': recommendation
                })

            finally:
                os.remove(file_path)
        else:
            return jsonify({'error': 'No image uploaded for prediction.'}), 400

    except Exception as e:
        logging.error(f"Error in skin type prediction: {e}")
        return jsonify({'error': 'Error in skin type prediction'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)