document.addEventListener('DOMContentLoaded', () => {
    const predictBtn = document.getElementById('predictBtn');
    const imageInput = document.getElementById('imageInput');
    const originalImage = document.getElementById('originalImage');
    const resultsDiv = document.getElementById('detectionResults');

    predictBtn.addEventListener('click', async () => {
        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image first');
            return;
        }

        predictBtn.disabled = true;
        predictBtn.textContent = 'Processing...';
        resultsDiv.innerHTML = '';

        try {
            const formData = new FormData();
            formData.append('file', file);

            originalImage.src = URL.createObjectURL(file);
            originalImage.style.display = 'block';

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const data = await response.json();

            if (data.detections.length > 0) {
                resultsDiv.innerHTML = '<h3>Detected Objects:</h3>';
                data.detections.forEach(det => {
                    const item = document.createElement('div');
                    item.className = 'detection-item';
                    item.innerHTML = `
                        <strong>${det.class}</strong> (${(det.confidence * 100).toFixed(2)}% confidence)
                        <div>Bounding box: [${det.bbox.map(x => x.toFixed(1)).join(', ')}]</div>
                    `;
                    resultsDiv.appendChild(item);
                });
            } else {
                resultsDiv.innerHTML = '<p>No objects detected</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        } finally {
            predictBtn.disabled = false;
            predictBtn.textContent = 'Detect Objects';
        }
    });
});

// The following code is disabled to avoid conflicts with the inline script in index.html
/*
document.addEventListener('DOMContentLoaded', () => {
    const predictBtn = document.getElementById('predictBtn');
    const imageInput = document.getElementById('imageInput');
    const originalImage = document.getElementById('originalImage');
    const resultsDiv = document.getElementById('detectionResults');

    predictBtn.addEventListener('click', async () => {
        const file = imageInput.files[0];
        if (!file) {
            alert('Please select an image first');
            return;
        }

        predictBtn.disabled = true;
        predictBtn.textContent = 'Processing...';
        resultsDiv.innerHTML = '';

        try {
            const formData = new FormData();
            formData.append('file', file);

            originalImage.src = URL.createObjectURL(file);
            originalImage.style.display = 'block';

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const data = await response.json();

            if (data.detections.length > 0) {
                resultsDiv.innerHTML = '<h3>Detected Objects:</h3>';
                data.detections.forEach(det => {
                    const item = document.createElement('div');
                    item.className = 'detection-item';
                    item.innerHTML = `
                        <strong>${det.class}</strong> (${(det.confidence * 100).toFixed(2)}% confidence)
                        <div>Bounding box: [${det.bbox.map(x => x.toFixed(1)).join(', ')}]</div>
                    `;
                    resultsDiv.appendChild(item);
                });
            } else {
                resultsDiv.innerHTML = '<p>No objects detected</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
        } finally {
            predictBtn.disabled = false;
            predictBtn.textContent = 'Detect Objects';
        }
    });
});
*/
