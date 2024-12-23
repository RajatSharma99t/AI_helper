from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Construct the structured prompt
    prompt = (
        f"You are an advanced AI model that provides answers. "
        f"When answering, follow this structure:\n\n"
        f"1. Brief overview of the concept.\n"
        f"2. Step-by-step explanation or solution.\n"
        f"3. Key points summarized as a list.\n\n"
        f"Question: {question}\n"
        f"Answer:"
    )

    try:
        # Run the Llama CLI with the structured prompt
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2'],
            input=prompt,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "error": "Ollama command failed",
                "details": result.stderr.strip()
            }), 500

        answer = result.stdout.strip()
        if not answer:
            return jsonify({"error": "No response from Ollama"}), 500

        # Extract key points (example logic)
        key_points = [line.strip() for line in answer.split('\n') if line.startswith('-')]

        return jsonify({"answer": answer, "keyPoints": key_points})

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
