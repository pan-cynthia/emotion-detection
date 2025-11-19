import { useRef, useState } from "react";
import Webcam from "react-webcam";
import "./style.css";

function App() {
  const webcamRef = useRef(null);
  const [prediction, setPrediction] = useState(null);
  const [confidence, setConfidence] = useState(null);

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:5000";

  const predictEmotion = async () => {
    const image = webcamRef.current.getScreenshot();
    const response = await fetch(`${BACKEND_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image }),
    });
    const data = await response.json();
    setPrediction(data.emotion);
    setConfidence(data.confidence);
  };

  return (
    <div className='container'>
      <h1 className='title'>Emotion Detection</h1>
      <Webcam
        ref={webcamRef}
        screenshotFormat='image/jpeg'
        videoConstraints={{ width: 320, height: 240 }}
      />
      <button className='btn' onClick={predictEmotion}>
        Capture!
      </button>
      {prediction && (
        <p>
          Detected Emotion: {prediction}, Confidence: {confidence}
        </p>
      )}
    </div>
  );
}

export default App;
