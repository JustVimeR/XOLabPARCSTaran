import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, send_file

app = Flask(__name__)

worker_urls = [
    os.getenv("WORKER1_URL", "http://worker1:5000"),
    os.getenv("WORKER2_URL", "http://worker2:5000")
]

def split_range(xmin, xmax, num_parts):
    step = (xmax - xmin) / num_parts
    return [(xmin + i * step, xmin + (i + 1) * step) for i in range(num_parts)]

def generate_image():
    width, height = 800, 800
    max_iter = 256
    ymin, ymax = -1.5, 1.5
    x_parts = split_range(-2.0, 1.0, len(worker_urls))

    results = []
    for i, (xmin, xmax) in enumerate(x_parts):
        payload = {
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "width": width // len(worker_urls),
            "height": height,
            "max_iter": max_iter
        }
        print(f"🔁 Sending task to {worker_urls[i]}")
        r = requests.post(f"{worker_urls[i]}/compute", json=payload, timeout=30)
        r.raise_for_status()
        results.append(np.array(r.json()))

    full_image = np.hstack(results)
    plt.imshow(full_image, cmap='hot')
    plt.axis('off')
    plt.savefig("mandelbrot.png", dpi=300)
    print("✅ Image saved as mandelbrot.png")

@app.route('/')
def index():
    return 'Go to /mandelbrot.png to see the result.'

@app.route('/mandelbrot.png')
def serve_image():
    if not os.path.exists("mandelbrot.png"):
        generate_image()
    return send_file("mandelbrot.png", mimetype='image/png')

if __name__ == '__main__':
    generate_image()
    app.run(host='0.0.0.0', port=5050)
