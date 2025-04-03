# master.py
import os
import requests
import numpy as np
import matplotlib.pyplot as plt

# Отримуємо адреси воркерів з ENV
worker_urls = [
    os.getenv("WORKER1_URL", "http://localhost:5001"),
    os.getenv("WORKER2_URL", "http://localhost:5002")
]

def split_range(xmin, xmax, num_parts):
    step = (xmax - xmin) / num_parts
    return [(xmin + i * step, xmin + (i + 1) * step) for i in range(num_parts)]

def main():
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
        try:
            print(f"🔁 Sending task to {worker_urls[i]}: {xmin} to {xmax}")
            r = requests.post(f"{worker_urls[i]}/compute", json=payload, timeout=30)
            r.raise_for_status()
            results.append(np.array(r.json()))
            print(f"✅ Got result from worker {i+1}")
        except Exception as e:
            print(f"❌ Error from worker {i+1}: {e}")
            return

    full_image = np.hstack(results)
    plt.imshow(full_image, cmap='hot')
    plt.axis('off')
    plt.savefig("mandelbrot.png", dpi=300)
    print("✅ Image saved as mandelbrot.png")

if __name__ == '__main__':
    main()
