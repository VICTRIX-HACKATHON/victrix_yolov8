from flask import Flask, render_template, request, jsonify, url_for
from ultralytics import YOLO
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'Trained Model', 'best.pt')
model = YOLO(model_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Handle both JSON (base64 image) and form-data (file upload)
    if request.is_json:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        # Remove header if present
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        import base64
        import io
        image_bytes = base64.b64decode(image_data)
        npimg = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        filename = 'captured.png'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        cv2.imwrite(filepath, img)
    else:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            img = cv2.imread(filepath)
        else:
            return jsonify({'error': 'File type not allowed'}), 400

    results = model.predict(img)
    detections = []
    # Defensive: check if results is not empty and has boxes
    for r in results:
        # Use getattr for compatibility
        names = getattr(r, 'names', getattr(model, 'names', []))
        if hasattr(r, 'boxes') and r.boxes is not None:
            for box in r.boxes:
                cls_idx = int(box.cls)
                label = names[cls_idx] if names and cls_idx < len(names) else str(cls_idx)
                conf = float(box.conf) if hasattr(box, 'conf') else 0.0
                bbox = box.xyxy[0].tolist() if hasattr(box, 'xyxy') else []
                detections.append({
                    'label': label,
                    'confidence': round(conf * 100, 2),
                    'bbox': bbox
                })

    return jsonify({
        'original': url_for('static', filename=f"uploads/{filename}"),
        'results': detections
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)




