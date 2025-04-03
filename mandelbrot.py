# mandelbrot.py
import numpy as np

def mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    result = np.zeros((height, width), dtype=np.uint8)
    for ix in range(width):
        for iy in range(height):
            x = xmin + (xmax - xmin) * ix / width
            y = ymin + (ymax - ymin) * iy / height
            c = complex(x, y)
            z = 0
            count = 0
            while abs(z) <= 2 and count < max_iter:
                z = z*z + c
                count += 1
            result[iy, ix] = int(255 * count / max_iter)
    return result.tolist()
