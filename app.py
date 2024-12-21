import subprocess
from flask import Flask, request, jsonify, send_from_directory
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

    try:
        # Run the Ollama CLI and pass the input via stdin
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2'],
            input=question,
            capture_output=True,
            text=True
        )

        # Log command output for debugging
        print("Command:", result.args)
        print("Standard Output:", result.stdout)
        print("Error Output:", result.stderr)

        if result.returncode != 0:
            # Handle CLI errors
            return jsonify({
                "error": "Ollama command failed",
                "details": result.stderr.strip()
            }), 500

        # Parse the output
        answer = result.stdout.strip()
        if not answer:
            return jsonify({"error": "No response from Ollama"}), 500

        return jsonify({"answer": answer})

    except Exception as e:
        # Catch and log unexpected errors
        print("Unexpected error:", e)
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
