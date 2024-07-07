# Dokumentasi Proyek: URTABIRSURYA

## Daftar Isi
- [Deskripsi Proyek](#deskripsi-proyek)
- [Struktur Proyek](#struktur-proyek)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Persyaratan](#persyaratan)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Struktur Proyek Rinci](#struktur-proyek-rinci)
- [Lisensi](#lisensi)

---

## Deskripsi Proyek

**URTABIRSURYA** adalah aplikasi berbasis web yang memungkinkan pengguna untuk mengunggah gambar kulit mereka untuk memprediksi jenis kulit dan mendapatkan rekomendasi produk sunscreen yang sesuai. Aplikasi ini memanfaatkan model pembelajaran mesin untuk klasifikasi jenis kulit dan memberikan saran berdasarkan jenis kulit yang terdeteksi.

---

## Struktur Proyek

```
URTABIRSURYA/
│
├── app.py                 # File utama aplikasi Flask
├── model/
│   └── skin_type_model_baru.h5   # Model pembelajaran mesin
├── static/
│   └── css/
│       └── style.css      # Gaya CSS
├── templates/
│   └── home.html          # Template HTML untuk halaman utama
└── javascript/
    └── main.js            # Script JavaScript untuk interaksi frontend
```

---

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman backend.
- **Flask**: Framework web untuk Python.
- **TensorFlow**: Framework pembelajaran mesin untuk model klasifikasi gambar.
- **HTML/CSS**: Untuk membuat halaman web dan styling.
- **JavaScript**: Untuk interaksi dan pengolahan frontend.

---

## Persyaratan

Pastikan Anda memiliki perangkat lunak berikut yang terpasang pada sistem Anda:

- Python 3.x
- Flask
- TensorFlow
- Browser Web (misalnya Google Chrome, Firefox)

---

## Instalasi

1. **Clone Repository**
   ```bash
   git clone https://github.com/user/repository.git
   cd URTABIRSURYA
   ```

2. **Pasang Dependensi**
   ```bash
   pip install Flask tensorflow
   ```

3. **Menjalankan Aplikasi**
   ```bash
   python app.py
   ```

4. **Akses Aplikasi**
   Buka browser dan navigasikan ke `http://localhost:5001`.

---

## Penggunaan

1. **Buka Aplikasi**: Akses halaman utama di `http://localhost:5001`.
2. **Unggah Gambar**: Klik "Pilih gambar" untuk memilih file gambar dari komputer Anda.
3. **Prediksi**: Klik "Unggah dan Prediksi" untuk mengunggah gambar dan mendapatkan hasil prediksi serta rekomendasi produk sunscreen.

---

## Struktur Proyek Rinci

### `app.py`
File utama aplikasi Flask yang menangani routing dan logika prediksi.

**Kode Utama:**
```python
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
```

### `home.html`
Template HTML untuk halaman utama aplikasi.

**Kode Utama:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URTABIRSURYA</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <script src="javascript/main.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="logo">
        <h1>SELAMAT DATANG DI YOUR TABIRSURYA</h1>
        <p>Unggah gambar untuk memprediksi jenis kulit Anda dan dapatkan rekomendasi jenis sunscreen</p>
        <form method="POST" action="/hasil prediksi" enctype="multipart/form-data">
            <div class="file-input">
                <label for="file">Pilih gambar</label>
                <input type="file" name="file" id="file" accept="image/*" required>
            </div>
            <input type="submit" value="Unggah dan Prediksi">
        </form>
        <div class="result" id="result">
            <h2>Hasil Prediksi</h2>
            <p>Jenis kulit: Normal</p>
            <p>Rekomendasi: </p>
        </div>
    </div>
</body>
</html>
```

### `style.css`
File gaya untuk mengatur tampilan halaman.

**Kode Utama:**
```css
body {
    font-family: 'Montserrat', sans-serif;
    background: linear-gradient(135deg, #f3e6f7 25%, #e9e1f2 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    color: #333;
}

.container {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    max-width: 400px;
    text-align: center;
    position: relative;
}

.logo {
    width: 100px;
    position: absolute;
    top: -90px;
    left: calc(50% - 55px); /* Adjust position based on logo width */
    border-radius: 50%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: white;
    padding: 10px;
}

h1 {
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 20px;
    color: #6a1b9a;
}

p {
    margin: 0 0 20px;
    font-size: 16px

;
    color: #777;
}

.file-input {
    margin-bottom: 20px;
}

.file-input label {
    display: block;
    font-size: 16px;
    margin-bottom: 10px;
    font-weight: 600;
    color: #6a1b9a;
}

input[type="file"] {
    border: 2px solid #ddd;
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
    border-radius: 10px;
    font-size: 14px;
}

input[type="submit"] {
    background-color: #6a1b9a;
    color: white;
    border: none;
    padding: 12px 25px;
    font-size: 16px;
    border-radius: 25px;
    cursor: pointer;
    transition: background-color 0.3s;
}

input[type="submit"]:hover {
    background-color: #4a148c;
}

.result {
    margin-top: 20px;
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.result h2 {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 10px;
    color: #6a1b9a;
}

.result p {
    font-size: 16px;
    color: #555;
}
```

### `main.js`
Script JavaScript untuk menangani pengiriman formulir dan menampilkan hasil.

**Kode Utama:**
```javascript
document.querySelector('form').onsubmit = async function(e) {
    e.preventDefault();
    const form = new FormData(this);
    const response = await fetch('/hasil prediksi', {
        method: 'POST',
        body: form
    });
    const result = await response.json();
    if (result.error) {
        document.getElementById('result').innerHTML = `<p>${result.error}</p>`;
    } else {
        document.getElementById('result').innerHTML = `
            <h2>Hasil Prediksi</h2>
            <p><strong>Jenis Kulit:</strong> ${result.skin_type}</p>
            <p><strong>Rekomendasi:</strong> ${result.recommendation}</p>
            <h3>Probabilitas:</h3>
            <ul>
                ${Object.keys(result.probabilities).map(skinType => `
                    <li>${skinType}: ${(result.probabilities[skinType] * 100).toFixed(2)}%</li>
                `).join('')}
            </ul>
        `;
    }
}
```

---

## Lisensi

Proyek ini dilisensikan di bawah lisensi [MIT License](LICENSE).

---

Jika ada pertanyaan atau butuh bantuan lebih lanjut, jangan ragu untuk menghubungi saya.
