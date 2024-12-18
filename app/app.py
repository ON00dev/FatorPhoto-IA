from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from PIL import Image, ImageEnhance
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from functools import wraps
import jwt
from datetime import datetime, timedelta

# Configurações do aplicativo
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_jwt_secret_key'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Habilitar CORS
CORS(app)

# Funções auxiliares para autenticação JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Remova o prefixo "Bearer " do token
            if token.startswith("Bearer "):
                token = token[7:]
            print(f"Token recebido: {token}")  # Log do token recebido
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(f"Token decodificado: {data}")  # Log do conteúdo do token
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'error': 'Token is invalid'}), 401

        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400

    # Usuário fixo para teste
    if auth['username'] == 'admin' and auth['password'] == 'password':
        token = jwt.encode({
            'user': auth['username'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

class ImageFilterAI:
    def __init__(self):
        pass

    def analyze_image(self, image_path):
        """
        Analyzes an image to extract its key filtering parameters.
        """
        image = cv2.imread(image_path)
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Extract basic metrics
        brightness = np.mean(image)  # Average pixel intensity
        contrast = image.std()      # Standard deviation of pixel intensity

        # Saturation and Hue analysis
        saturation = image_hsv[:, :, 1].mean()
        hue = image_hsv[:, :, 0].mean()

        # Shadow and Highlight Analysis
        shadow_level = np.percentile(image, 5)  # Approximation of shadow level
        highlight_level = np.percentile(image, 95)  # Approximation of highlights

        return {
            'brightness': brightness,
            'contrast': contrast,
            'saturation': saturation,
            'hue': hue,
            'shadow_level': shadow_level,
            'highlight_level': highlight_level
        }

    def apply_filters(self, image_path, filters):
        """
        Apply extracted filters to a target image.
        """
        image = Image.open(image_path)

        # Apply brightness adjustment
        if 'brightness' in filters:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(filters['brightness'] / 128)  # Normalize to range 0-2

        # Apply contrast adjustment
        if 'contrast' in filters:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(filters['contrast'] / 64)  # Normalize to range 0-2

        # Apply saturation adjustment
        if 'saturation' in filters:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(filters['saturation'] / 64)  # Normalize to range 0-2

        return image

ai = ImageFilterAI()

@app.route('/analyze', methods=['POST'])
@token_required
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    try:
        filters = ai.analyze_image(image_path)
        return jsonify(filters)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apply', methods=['POST'])
@token_required
def apply_filters():
    if 'source_image' not in request.files or 'target_image' not in request.files:
        return jsonify({"error": "Source and target image files are required"}), 400

    source_file = request.files['source_image']
    target_file = request.files['target_image']

    source_filename = secure_filename(source_file.filename)
    target_filename = secure_filename(target_file.filename)

    source_path = os.path.join(app.config['UPLOAD_FOLDER'], source_filename)
    target_path = os.path.join(app.config['UPLOAD_FOLDER'], target_filename)

    source_file.save(source_path)
    target_file.save(target_path)

    try:
        filters = ai.analyze_image(source_path)
        adjusted_image = ai.apply_filters(target_path, filters)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"adjusted_{target_filename}")
        adjusted_image.save(output_path)

        return jsonify({"output_image": output_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
