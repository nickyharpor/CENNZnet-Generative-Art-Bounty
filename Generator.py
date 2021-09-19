import cairo, PIL, argparse, math, random
from PIL import Image, ImageDraw

list_of_colors = [(145, 185, 141), (229, 192, 121), (210, 191, 88), (140, 190, 178), (255, 183, 10), (189, 190, 220),
                  (221, 79, 91), (16, 182, 98), (227, 146, 80), (241, 133, 123), (110, 197, 233), (235, 205, 188),
                  (197, 239, 247), (190, 144, 212),
                  (41, 241, 195), (101, 198, 187), (255, 246, 143), (243, 156, 18), (189, 195, 199), (243, 241, 239)]

float_gen = lambda a, b: random.uniform(a, b)

def draw_fill_and_stroke(cr, do_fill, do_stroke, r, g, b):
    cr.save()

    if do_stroke:
        cr.set_source_rgb(r, g, b)
        cr.stroke_preserve()

    if do_fill:
        cr.set_source_rgb(r, g, b)
        cr.fill_preserve()

    cr.restore()


def draw_shaft(cr, x, y, shaft_type, width, height, r, g, b):
    cr.set_source_rgb(r, g, b)
    if shaft_type == 'simple':
        cr.rectangle(x, y, width, height)
        cr.fill()


def draw_head(cr, x, y, head_type, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    if head_type == 'simple':
        cr.arc(x, y, radius, math.pi/2, 3*math.pi/2)
        cr.fill()


def draw_balls(cr, x, y, width, height, scale_x, scale_y, rotation, r, g, b):
    x0 = 0
    y0 = -0.25
    x1 = 0.2
    y1 = -0.8
    x2 = 1.1
    y2 = -0.2
    x3 = 0
    y3 = 0.5

    cr.translate(x, y)
    cr.scale(scale_x, scale_y)
    cr.rotate(rotation*math.pi)

    cr.save()

    cr.scale(width, height)
    cr.move_to(x0, y0)
    cr.curve_to(x1, y1, x2, y2, x3, y3)
    cr.curve_to(-x2, y2, -x1, y1, -x0, y0)

    cr.restore()

    draw_fill_and_stroke(cr, True, False, r, g, b)


def draw_orbit(cr, line, x, y, radius, r, g, b):
    cr.set_line_width(line)
    cr.arc(x, y, radius, 0, 2 * math.pi)
    cr.stroke()


def draw_circle_fill(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2 * math.pi)
    cr.fill()


def draw_border(cr, size, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, height)
    cr.rectangle(0, 0, width, size)
    cr.rectangle(0, height - size, width, size)
    cr.rectangle(width - size, 0, size, height)
    cr.fill()


def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify Width", default=1920, type=int)
    parser.add_argument("--height", help="Specify Height", default=1080, type=int)
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()
    width, height = args.width, args.height

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    # background
    back_r, back_g, back_b = random.random(), random.random(), random.random()
    draw_background(cr, back_r, back_g, back_b, width, height)

    # dildo color
    d_r = random.random()
    d_g = random.random()
    d_b = random.random()
    while abs(d_r - back_r) < 0.1:
        d_r = random.random()
    while abs(d_g - back_g) < 0.1:
        d_g = random.random()
    while abs(d_b - back_b) < 0.1:
        d_b = random.random()

    # dildo size and position
    d_height = 8*width/10
    d_girth = 2*height/10
    d_neck_x = width/10
    d_neck_y = height/10

    # draw dildo
    draw_shaft(cr, d_neck_x, d_neck_y, 'simple', d_height, d_girth, d_r, d_g, d_b)
    draw_head(cr, d_neck_x, d_neck_y+(d_girth/2), 'simple', d_girth/2, d_r, d_g, d_b)
    draw_balls(cr, d_neck_x + d_height - 100, d_neck_y + d_girth, 200, 200, 1, 1, 1, d_r, d_g, d_b)

    ims.write_to_png('Examples/Generative-Space-Flat-' + str(width) + 'w-' + str(height) + 'h.png')

    pil_image = Image.open('Examples/Generative-Space-Flat-' + str(width) + 'w-' + str(height) + 'h.png')
    pixels = pil_image.load()

    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]

            noise = float_gen(1.0 - args.noise, 1.0 + args.noise)
            pixels[i, j] = (int(r * noise), int(g * noise), int(b * noise))
    pil_image.save('Examples/Generative-Space-Texture-' + str(width) + 'w-' + str(height) + 'h.png')


if __name__ == "__main__":
    main()
