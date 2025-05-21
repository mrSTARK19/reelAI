import React, { useState } from 'react';
import './App.css';

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleVideoChange = (e) => {
    setVideoFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!videoFile) {
      setMessage("Please select a video.");
      return;
    }

    setLoading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('video', videoFile);

    try {
      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      setMessage(data.valid ? "✅ Video is clean" : "❌ Contains nudity upload failed");
    } catch (err) {
      setMessage("Upload failed. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Nudity Detection</h2>

        <div className="upload-box">
          <input
            type="file"
            accept="video/*"
            onChange={handleVideoChange}
            id="videoInput"
            hidden
          />
          <label htmlFor="videoInput" className="upload-label">
            {videoFile ? videoFile.name : "Click or drag a video to upload"}
          </label>
        </div>

        <button onClick={handleUpload} className="upload-btn" disabled={loading}>
          {loading ? "Analyzing..." : "Upload"}
        </button>

        {message && <div className="result">{message}</div>}
      </div>
    </div>
  );
}

export default App;
