# worker.py
from flask import Flask, request, jsonify
from mandelbrot import mandelbrot

app = Flask(__name__)

@app.route('/compute', methods=['POST'])
def compute():
    data = request.get_json()
    result = mandelbrot(**data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
