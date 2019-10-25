from PIL import Image as Img
from cmath import sin, cos, tan
from math import floor

def is_gaussian_integer(z, epsilon):
    return abs(z.real - round(z.real)) < epsilon and abs(z.imag - round(z.imag)) < epsilon

def grid_sample(width, samples):
    out = []
    radius = int(round(samples / 2))
    ds = width / float(samples)
    for a in range(-radius, radius):
        for b in range(-radius, radius):
            out.append(a*ds + b*1j*ds)
    return out

def oddities(samples, transform, epsilon = 1e-10):
    def predicate(z):
        try:
            out = transform(z)

            return is_gaussian_integer(out, epsilon)
        except:
            return False

    return filter(predicate, samples)

if __name__ == '__main__':
    # In pixels
    imageWidth, imageHeight = 144, 90
    image = Img.new("RGB", (imageWidth, imageHeight))

    # In pixels per flax
    granularity = 1
    # In flax
    width, height = imageWidth/granularity, imageHeight/granularity

    samples = grid_sample(max(width, height), max(imageWidth, imageHeight))

    # @param dim - in flax
    # @param offset - in pixels
    # @return - in pixels
    def to_image_coord(dim, offset):
        return int(round(dim*granularity + offset/2))

    for sample in oddities(samples, lambda z: tan(cos(sin(z)))):
        x = to_image_coord(sample.real, imageWidth)
        y = to_image_coord(sample.imag, imageHeight)
        coord = (x, y)

        if 0 <= x < imageWidth and 0 <= y < imageHeight:
            image.putpixel(coord, (93, 188, 210))

    image.show()
