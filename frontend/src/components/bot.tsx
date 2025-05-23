
import React, { useState } from "react";
import "./styles.css";

function Bot() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false); // Loader state

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setUploadMessage("");
      setAnswer("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5010/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setUploadMessage(res.ok ? data.message : `Error: ${data.error}`);
    } catch {
      setUploadMessage("Upload failed, please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleQuery = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("http://localhost:5010/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setAnswer(res.ok ? data.answer : `Error: ${data.error}`);
    } catch {
      setAnswer("Query failed, please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{height:'90vh'}}>
      <h1>Q/A Bot</h1>

      <div className="upload-section">
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload} className="upload-btn">Upload</button>
        {uploadMessage && <p className="message">{uploadMessage}</p>}
      </div>

      <div className="query-box">
        <input
          type="text"
          placeholder="Enter your question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button onClick={handleQuery} className="ask-btn">Ask</button>
      </div>

      {loading && (
        <div className="loader-container">
          <div className="spinner"></div>
          <p>Processing, please wait...</p>
        </div>
      )}

      <div className="chat-container">
        {question && (
          <div className="chat-bubble user-question">
            <strong>You:</strong> {question}
          </div>
        )}
        {answer && (
          <div className="chat-bubble bot-answer">
            <strong>Bot:</strong> {answer}
          </div>
        )}
      </div>
    </div>
  );
}

export default Bot;
