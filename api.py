from flask import Flask, request, jsonify, send_from_directory
from main import Main

app = Flask(__name__, static_folder="public", static_url_path="/")

@app.route('/')
def index():
    return send_from_directory("public", "index.html")

@app.route('/<path:path>')
def static_file(path):
    return send_from_directory("public", path)

biomera = Main()

@app.route('/ask', methods=['POST'])
def message():
    content = request.get_json()
    if not content or 'message' not in content:
        return jsonify({'error': 'No JSON entry'}), 400
    
    if len(content["message"]) < 2:
        return jsonify({'error': 'Message too short'}), 400
    
    if len(content["message"]) > 1000:
        return jsonify({'error': 'Message too long'}), 400

    response = biomera.query("user", content["message"])

    return jsonify({
        "input": content["message"],
        "response": response,
    }), 201

@app.route('/files', methods=["GET"])
def files():
    files = biomera.executor.list_files()
    return jsonify(files), 200

@app.route('/reset', methods=["POST"])
def reset():
    try:
        biomera = Main()
        return jsonify({
            "message": "BIOMERA has been reset.",
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
        }), 500

if __name__ == '__main__':
    app.run(debug=True)