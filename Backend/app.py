from flask import Flask, request, jsonify
import cv2
import os
from nudenet import NudeDetector
import tempfile
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

elements = [
    'FEMALE_GENITALIA_EXPOSED',
    'FEMALE_BREAST_EXPOSED',
    'BUTTOCKS_EXPOSED',
    'MALE_GENITALIA_EXPOSED',
    'ANUS_EXPOSED'
]

@app.route('/upload', methods=['POST'])
def upload_video():
    file = request.files.get('video')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save uploaded file temporarily
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_path = temp.name
    file.save(temp_path)
    temp.close()  # Close the file so it's not locked

    # Analyze the video
    ncount = analyse_vid(temp_path)

    try:
        os.unlink(temp_path)  # Remove temp file after use
    except Exception as e:
        print(f"Could not delete temp file: {e}")

    is_valid = ncount == 0
    return jsonify({"valid": is_valid})

def analyse_vid(video_path):
    vid = cv2.VideoCapture(video_path)
    ls = []
    while True:
        flag, frame = vid.read()
        if flag:
            frame = cv2.resize(frame, (500, 500))
            ls.append(frame)
        else:
            break
    vid.release()

    detector = NudeDetector()
    ncount = 0

    for frame in ls:
        res = detector.detect(frame)
        for detection in res:
            if 'class' in detection and 'score' in detection:
                if detection['class'] in elements and detection['score'] >= 0.40:
                    ncount += 1
                    return ncount  # Stop early on first detection
    return ncount

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
