// Mendapatkan referensi ke elemen form dan hasil prediksi
const form = document.getElementById('prediction-form');
const resultContainer = document.getElementById('prediction-result');
const resultStatus = document.getElementById('prediction-status');
const errorMessage = document.getElementById('error-message');

// Menangani event submit form
form.addEventListener('submit', function(event) {
    // Mencegah refresh halaman
    event.preventDefault();

    // Menghapus pesan kesalahan sebelumnya
    errorMessage.innerHTML = '';

    // Membuat objek FormData untuk mengumpulkan data form
    const formData = new FormData(this);

    // Mengirim permintaan POST menggunakan Fetch API
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Server error');
        }
    })
    .then(data => {
        // Menangani respons dari server
        if (data.error) {
            // Menampilkan pesan kesalahan jika ada
            errorMessage.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            resultContainer.classList.remove('show');
        } else if (data.prediction) {
            const result = data.prediction.toLowerCase();
            resultStatus.textContent = result;

            // Menghapus kelas warna sebelumnya
            resultStatus.classList.remove('sehat', 'sakit');

            // Menambahkan kelas warna sesuai dengan status
            if (result === 'sehat') {
                resultStatus.classList.add('sehat');
            } else if (result === 'sakit') {
                resultStatus.classList.add('sakit');
            }

            resultContainer.classList.add('show');
        } else {
            throw new Error('Invalid response from server');
        }
    })
    .catch(error => {
        // Menangani error jika terjadi
        console.error('Error:', error);
        // Tambahkan kode untuk menampilkan pesan kesalahan ke pengguna jika diperlukan
    });
});

// Animasi pada hasil prediksi
const prediction = document.querySelector('.prediction');
if (prediction) {
    prediction.addEventListener('mouseover', function() {
        this.classList.add('animate-prediction');
    });

    prediction.addEventListener('mouseout', function() {
        this.classList.remove('animate-prediction');
    });
}
