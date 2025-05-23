import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from ragpipeline import RAGPipeline

app = Flask(__name__)
CORS(app)

MODEL_PATH = "model/tinyllama-1.1b-chat-v1.0.Q5_K_M.gguf"


rag = RAGPipeline(model_path=MODEL_PATH)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    ext = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        file.save(tmp.name)
        try:
            chunk_count = rag.process_file(tmp.name)
            return jsonify({"message": f"File uploaded and processed, {chunk_count} chunks created."})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            os.unlink(tmp.name)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = rag.query(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
