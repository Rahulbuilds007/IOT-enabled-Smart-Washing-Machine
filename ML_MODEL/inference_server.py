# inference_server.py
# Run this SEPARATELY: python inference_server.py
# It listens on http://localhost:5001

from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from torchvision import transforms
from PIL import Image
import cv2
import numpy as np
import base64
import io
from model import StainLevelModel

app = Flask(__name__)
CORS(app)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_PATH = "stain_model.pth"

# --- Load model once at startup ---
model = StainLevelModel(num_classes=6).to(DEVICE)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model.eval()
print(f"✅ Model loaded on {DEVICE}")

img_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
mask_tf = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def generate_mask(cv2_frame):
    """Auto-generate stain mask via HSV thresholding."""
    hsv = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2HSV)
    lower = np.array([10, 40, 40])
    upper = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Accepts a base64-encoded image, runs the stain model, returns:
    {
        level: int (0-5),
        confidence: float,
        probabilities: [float x6],
        label: str
    }
    """
    try:
        data = request.json
        img_b64 = data['image']  # base64 string

        # Decode base64 → numpy array
        img_bytes = base64.b64decode(img_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        cv2_frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if cv2_frame is None:
            return jsonify({'error': 'Could not decode image'}), 400

        # Generate mask
        mask_np = generate_mask(cv2_frame)

        # Convert to PIL
        rgb_frame = cv2.cvtColor(cv2_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        pil_mask = Image.fromarray(mask_np)

        # Preprocess
        img_tensor = img_tf(pil_img)
        mask_tensor = mask_tf(pil_mask)
        mask_tensor = (mask_tensor > 0.5).float()

        input_tensor = torch.cat([img_tensor * mask_tensor, mask_tensor], dim=0)
        input_tensor = input_tensor.unsqueeze(0).to(DEVICE)

        # Inference
        with torch.no_grad():
            output = model(input_tensor)
            probs = torch.nn.functional.softmax(output[0], dim=0)
            level = torch.argmax(probs).item()
            confidence = probs[level].item()

        LABELS = ["Clean", "Very Light", "Light", "Medium", "Heavy", "Extreme"]

        return jsonify({
            'level': level,
            'confidence': round(confidence * 100, 1),
            'probabilities': [round(p.item() * 100, 1) for p in probs],
            'label': LABELS[level]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'device': DEVICE})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)