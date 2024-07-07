document.querySelector('form').onsubmit = async function(e) {
    e.preventDefault();
    const form = new FormData(this);
    const response = await fetch('/predict', {
        method: 'POST',
        body: form
    });
    const result = await response.json();
    if (result.error) {
        document.getElementById('result').innerHTML = `<p>${result.error}</p>`;
    } else {
        document.getElementById('result').innerHTML = `
            <h2>Prediction Result</h2>
            <p><strong>Skin Type:</strong> ${result.skin_type}</p>
            <p><strong>Recommendation:</strong> ${result.recommendation}</p>
            <h3>Probabilities:</h3>
            <ul>
                ${Object.keys(result.probabilities).map(skinType => `
                    <li>${skinType}: ${(result.probabilities[skinType] * 100).toFixed(2)}%</li>
                `).join('')}
            </ul>
        `;
    }
}
