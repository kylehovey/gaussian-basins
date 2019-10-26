from PIL import Image as Img
from cmath import sin, cos, tan, exp
from math import floor
from tqdm import tqdm

# Color Scheme
colors = [
    (239, 71, 111),
    (255, 209, 102),
    (17, 138, 178),
    (6, 214, 160),
    (7, 59, 76),
]

def is_gaussian_integer(z, epsilon = 1e-20):
    return (
        abs(z.real - round(z.real)) < epsilon and
        abs(z.imag - round(z.imag)) < epsilon
    )

if __name__ == '__main__':
    transform = lambda z: tan(cos(sin(z)))

    # In pixels
    imageWidth, imageHeight = 1440, 900
    image = Img.new("RGB", (imageWidth, imageHeight))

    granularity = 40 # In pixels per flax
    resolution = 1/float(granularity) # in flax per pixel

    with tqdm(total=imageWidth*imageHeight) as pbar:
        for u in range(imageWidth):
            for v in range(imageHeight):
                real_part = (u - imageWidth*0.5)*resolution
                imag_part = (v - imageHeight*0.5)*resolution

                try:
                    # This could be "infinite", thus the try/except
                    result = transform(real_part + imag_part*1j)

                    if is_gaussian_integer(result, 0):
                        image.putpixel((u, v), colors[4])
                    elif is_gaussian_integer(result, 1e-100):
                        image.putpixel((u, v), colors[3])
                    elif is_gaussian_integer(result, 1e-10):
                        image.putpixel((u, v), colors[2])
                    elif is_gaussian_integer(result, 1e-1):
                        image.putpixel((u, v), colors[1])
                except:
                    image.putpixel((u, v), colors[0])

                pbar.update(1)

    image.show()
