import cairo, argparse, math, random, os
from PIL import Image

float_gen = lambda a, b: random.uniform(a, b)


def conjure_codename(r, g, b, d_length, d_girth, shaft_type, head_type, tail_type, ball_type, crown_type):
    codename = head_type + str(int(d_length)) + shaft_type + str(int(d_girth)).ljust(3, '0') + \
               tail_type + str(int(r*100)).ljust(2, '0') + ball_type + str(int(g*100)).ljust(2, '0') + \
               crown_type + str(int(b*100)).ljust(2, '0')
    return codename


def write_codename(cr, codename, font_size, thickness, x, y, r, g, b):
    cr.save()
    cr.set_source_rgb(r, g, b)
    cr.set_font_size(font_size)
    cr.select_font_face("monospace",
                      cairo.FONT_SLANT_NORMAL,
                      cairo.FONT_WEIGHT_NORMAL)
    cr.move_to(x, y)
    cr.text_path(codename)
    cr.set_line_width(thickness)
    cr.stroke()
    cr.restore()


def draw_crown(cr, x, y, crown_type, width, height, r, g, b):
    if crown_type == 'N':  # none
        pass
    elif crown_type == 'B':  # bump
        if r > 0.9:
            xr = 1
        else:
            xr = r + 0.1
        if g > 0.9:
            xg = 1
        else:
            xg = g + 0.1
        if b > 0.9:
            xb = 1
        else:
            xb = b + 0.1
        bump = 1
        while width/bump > height:
            bump += 1
        bump -= 1
        jump = width/bump
        iter_hump = 0
        cr.set_source_rgb(xr, xg, xb)
        while iter_hump < bump:
            cr.arc(x+jump/2+(iter_hump*jump), y+height/2, jump/5, 0, 2*math.pi)
            cr.fill()
            iter_hump += 1
        cr.set_source_rgb(r, g, b)
    elif crown_type == 'H':  # heart
        if r > 0.8:
            xr = 1
        else:
            xr = r + 0.2
        if g > 0.8:
            xg = 1
        else:
            xg = g + 0.2
        if b > 0.8:
            xb = 1
        else:
            xb = b + 0.2
        bump = 1
        while width/bump > height:
            bump += 1
        bump -= 1
        jump = width/bump
        iter_hump = 0
        cr.set_source_rgb(xr, xg, xb)
        x0 = 0
        y0 = -0.25
        x1 = 0.2
        y1 = -0.8
        x2 = 1.1
        y2 = -0.2
        x3 = 0
        y3 = 0.5
        while iter_hump < bump:
            cr.save()
            cr.translate(x+jump/2+(iter_hump*jump), y+height/2)
            cr.scale(jump/2, jump/2)
            cr.move_to(x0, y0)
            cr.curve_to(x1, y1, x2, y2, x3, y3)
            cr.curve_to(-x2, y2, -x1, y1, -x0, y0)
            cr.fill()
            cr.restore()
            iter_hump += 1
        cr.set_source_rgb(r, g, b)
    elif crown_type == 'L':  # line
        if r > 0.85:
            xr = 1
        else:
            xr = r + 0.15
        if g > 0.85:
            xg = 1
        else:
            xg = g + 0.15
        if b > 0.85:
            xb = 1
        else:
            xb = b + 0.15
        cr.set_source_rgb(xr, xg, xb)
        repeat = 20
        iter_line = 0
        first = True
        while iter_line < repeat:
            if not first:
                cr.save()
                cr.set_line_width(5)
                cr.move_to(x+(iter_line*(width/repeat)), y + height/4)
                cr.line_to(x+(iter_line*(width/repeat)), y + 3*height/4)
                cr.stroke()
                cr.restore()
            else:
                first = False
            iter_line += 1
        cr.set_source_rgb(r, g, b)


def draw_tail(cr, x, y, tail_type, rx, ry, rotation, r, g, b, start_angle=0, end_angle=360):
    cr.set_source_rgb(r, g, b)
    if tail_type == 'N':  # none
        pass
    elif tail_type == 'U':  # u-like
        cr.save()
        cr.translate(x, y)
        cr.rotate(rotation * math.pi)
        cr.scale(rx * 0.01, ry * 0.01)
        cr.arc(0, 0, 100, start_angle * math.pi / 180, end_angle * math.pi / 180)
        cr.restore()
        cr.fill()
    elif tail_type == 'T':  # trapezoid
        cr.save()
        cr.move_to(x - rx*20, y)
        cr.line_to(x + rx*2, y - ry)
        cr.line_to(x + rx*2, y + ry)
        cr.fill()
        cr.restore()
    elif tail_type == 'C':  # cone
        cr.save()
        cr.move_to(x - rx*4, y)
        cr.line_to(x + rx*2, y - ry)
        cr.line_to(x + rx*2, y + ry)
        cr.fill()
        cr.restore()
    elif tail_type == 'A':  # arc
        cr.save()
        cr.arc(x, y, ry/1.5, -math.pi/3, math.pi/3)
        cr.set_line_width(ry/4)
        cr.stroke()
        cr.restore()
        cr.save()
        cr.set_line_width(ry/2)
        cr.move_to(x, y)
        cr.line_to(x+ry/1.5, y)
        cr.stroke()
        cr.restore()
    elif tail_type == 'R':  # ring
        cr.save()
        cr.set_line_width(ry/3.5)
        cr.arc(x, y, ry/1.4, 0, 2*math.pi)
        cr.stroke()
        cr.restore()


def draw_shaft(cr, x, y, shaft_type, width, height, r, g, b):
    cr.set_source_rgb(r, g, b)
    if shaft_type == 'S':  # simple
        cr.rectangle(x, y, width, height)
        cr.fill()
    elif shaft_type == 'V':  # vase
        cr.rectangle(x, y, width, height)
        cr.fill()
        cr.save()
        cr.move_to(x, y)
        cr.curve_to(x+width/3, y+height/2, x+2*width/3, y-height/2, x+width, y)
        cr.move_to(x+width, y+height)
        cr.curve_to(x+2*width/3, y+height+height/2, x+width/3, y+height-height/2, x, y+height)
        cr.fill()
        cr.restore()
    elif shaft_type == 'H':  # hump
        cr.rectangle(x, y, width, height)
        cr.fill()
        hump = 1
        while width/hump > height:
            hump += 1
        hump -= 1
        jump = width/hump
        iter_hump = 0
        while iter_hump < hump:
            cr.arc(x+jump/2+(iter_hump*jump), y+height/2, jump/2, 0, 2*math.pi)
            cr.fill()
            iter_hump += 1
    elif shaft_type == 'T':  # thorn
        cr.rectangle(x, y, width, height)
        cr.fill()
        repeat = 10
        iter_thorn = 0
        first, last = True, False
        while iter_thorn < repeat:
            if not first and not last:
                draw_thorn_upward(cr, x+(iter_thorn*(width/repeat)), y, width/repeat, height/4)
            else:
                first = False
            if repeat - iter_thorn < 2:
                last = True
            iter_thorn += 1
    elif shaft_type == 'X':  # x
        cr.rectangle(x, y, width, height)
        cr.fill()
        bump = 1
        while width/bump > height:
            bump += 1
        bump -= 1
        jump = width/bump
        iter_hump = 0
        first, last = True, False
        c_y = y+height/2
        c_s = jump/2
        while iter_hump < bump:
            if not first and not last:
                c_x = x+jump/2+(iter_hump*jump)
                cr.save()
                cr.set_line_width(c_s/1.5)
                cr.move_to(c_x+c_s, c_y+c_s)
                cr.line_to(c_x-c_s, c_y-c_s)
                cr.stroke()
                cr.restore()
                if bump - iter_hump == 2:
                    last = True
            else:
                first = False
            iter_hump += 1
    elif shaft_type == 'Q':  # x + h
        cr.rectangle(x, y, width, height)
        cr.fill()
        hump = 1
        while width/hump > height:
            hump += 1
        hump -= 1
        jump = width/hump
        iter_hump = 0
        while iter_hump < hump:
            cr.arc(x+jump/2+(iter_hump*jump), y+height/2, jump/2, 0, 2*math.pi)
            cr.fill()
            iter_hump += 1
        bump = 1
        while width/bump > height:
            bump += 1
        bump -= 1
        jump = width/bump
        iter_hump = 0
        first, last = True, False
        c_y = y+height/2
        c_s = jump/2
        while iter_hump < bump:
            if not first and not last:
                c_x = x+jump/2+(iter_hump*jump)
                cr.save()
                cr.set_line_width(c_s/1.5)
                cr.move_to(c_x+c_s, c_y+c_s)
                cr.line_to(c_x-c_s, c_y-c_s)
                cr.stroke()
                cr.restore()
                if bump - iter_hump == 2:
                    last = True
            else:
                first = False
            iter_hump += 1


def draw_thorn_upward(cr, x, y, width, height):
    cr.save()
    cr.move_to(x+width/2, y-height)
    cr.line_to(x+width/2, y)
    cr.line_to(x+width, y)
    cr.curve_to(x+3*width/4, y-height/6, x+2*width/3, y-height/4, x+width/2, y-height)
    cr.fill()
    cr.move_to(x+width/2, y-height)
    cr.line_to(x+width/2, y)
    cr.line_to(x, y)
    cr.curve_to(x+width/4, y-height/6, x+width/3, y-height/4, x+width/2, y-height)
    cr.fill()
    cr.restore()


def draw_head(cr, x, y, head_type, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    if head_type == 'R':  # round
        cr.arc(x, y+radius/2, radius/2, math.pi/2, 3*math.pi/2)
        cr.fill()
    elif head_type == 'P':  # pointy
        cr.save()
        cr.move_to(x, y)
        cr.line_to(x, y+radius)
        if x - radius > 20:
            cr.line_to(x-radius, y+radius/2)
        else:
            cr.line_to(x-radius/2, y+radius/2)
        cr.fill()
        cr.restore()
    elif head_type == 'B':  # ball
        cr.save()
        cr.move_to(x, y)
        cr.line_to(x, y+radius)
        cr.line_to(x-radius/2, y+radius/2)
        cr.fill()
        cr.restore()
        cr.arc(x-radius/3, y+radius/2, radius/4, 0, 2*math.pi)
        cr.fill()
    elif head_type == 'G':  # g-shape
        x0 = 0
        y0 = -0.25
        x1 = 0.2
        y1 = -0.8
        x2 = 1.1
        y2 = -0.2
        x3 = 0
        y3 = 0.5
        cr.save()
        cr.set_source_rgb(r, g, b)
        cr.translate(x, y+radius/2)
        cr.rotate(math.pi/2)
        cr.scale(radius*1.2, radius)
        cr.move_to(x0, y0)
        cr.curve_to(x1, y1, x2, y2, x3, y3)
        cr.curve_to(-x2, y2, -x1, y1, -x0, y0)
        cr.fill()
        cr.restore()


def draw_balls(cr, x, y, ball_type, width, height, scale_x, scale_y, rotation, r, g, b):
    if ball_type == 'N':  # none
        pass
    elif ball_type == 'H':  # heart
        x0 = 0
        y0 = -0.25
        x1 = 0.2
        y1 = -0.8
        x2 = 1.1
        y2 = -0.2
        x3 = 0
        y3 = 0.5

        cr.save()
        cr.set_source_rgb(r, g, b)
        cr.translate(x, y)
        cr.scale(scale_x, scale_y)
        cr.rotate(rotation*math.pi)
        cr.scale(width, height)
        cr.move_to(x0, y0)
        cr.curve_to(x1, y1, x2, y2, x3, y3)
        cr.curve_to(-x2, y2, -x1, y1, -x0, y0)
        cr.restore()
        cr.fill()
    elif ball_type == 'S':  # snake
        cr.save()
        x = x + width/2
        cr.move_to(x, y)
        cr.curve_to(x - width/4, y + height/3, x - width/3, y + height/2, x - 3*width/2, y + height/2)
        cr.curve_to(x - 4*width/10, y + height/3, x - 3*width/10, y + height/4, x - width/5, y)
        cr.line_to(x, y)
        cr.close_path()
        cr.fill()
        cr.restore()
    elif ball_type == 'J':  # jingle
        cr.save()
        x = x + width/2
        cr.move_to(x, y)
        cr.curve_to(x - width/4, y + height/3, x - width/3, y + height/2, x - 3*width/2, y + height/2)
        cr.curve_to(x - 4*width/10, y + height/4, x - 3*width/10, y + height/6, x - width/5, y)
        cr.line_to(x, y)
        cr.close_path()
        cr.fill()
        cr.restore()
        cr.arc(x - 3*width/2 + 5, y + height/2, height/10, 0, 2*math.pi)
        cr.fill()


def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", help="Specify Width", default=1200, type=int)
    parser.add_argument("--height", help="Specify Height", default=800, type=int)
    parser.add_argument("-n", "--noise", help="Texture", default=.4, type=float)
    args = parser.parse_args()
    width, height = args.width, args.height

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    # background
    back_r, back_g, back_b = 0.2, 0.2, 0.2
    codename_r, codename_g, codename_b = 0.8, 0.8, 0.8
    draw_background(cr, back_r, back_g, back_b, width, height)

    # dildo color
    d_r = round(random.random(), 2)
    d_g = round(random.random(), 2)
    d_b = round(random.random(), 2)
    while abs(d_r - back_r) < 0.1 or d_r > 0.99:
        d_r = round(random.random(), 2)
    while abs(d_g - back_g) < 0.1 or d_g > 0.99:
        d_g = round(random.random(), 2)
    while abs(d_b - back_b) < 0.1 or d_b > 0.99:
        d_b = round(random.random(), 2)

    # dildo size and position
    d_height = random.randint(width/4, (3*width/4))  # 300 to 900
    d_girth = random.randint(int(d_height/10), int(d_height/3))  # 30 to 300
    d_neck_x = (width - d_height)/2 + 20
    d_neck_y = (2*height/3 - d_girth)/2

    # custom
    shaft_list = ['S', 'V', 'H', 'T', 'X', 'X', 'Q', 'Q', 'Q', 'Q']
    shaft_type = shaft_list[random.randint(0, len(shaft_list)-1)]
    head_list = ['R', 'P', 'B', 'G', 'G']
    head_type = head_list[random.randint(0, len(head_list)-1)]
    tail_list = ['N', 'U', 'T', 'C', 'A', 'R', 'R', 'R', 'R', 'R']
    tail_type = tail_list[random.randint(0, len(tail_list)-1)]
    ball_list = ['N', 'H', 'S', 'J', 'J', 'J']
    ball_type = ball_list[random.randint(0, len(ball_list)-1)]
    crown_list = ['N', 'B', 'H', 'L', 'L', 'L']
    crown_type = crown_list[random.randint(0, len(crown_list)-1)]

    # codename (16 char)
    codename = conjure_codename(d_r, d_g, d_b, d_height, d_girth, shaft_type, head_type, tail_type, ball_type, crown_type)
    write_codename(cr, codename, 110, 4, (width/2)-(8*70), 7*height/8, codename_r, codename_g, codename_b)

    # draw dildo
    draw_shaft(cr, d_neck_x, d_neck_y, shaft_type, d_height, d_girth, d_r, d_g, d_b)
    draw_head(cr, d_neck_x, d_neck_y, head_type, d_girth, d_r, d_g, d_b)
    draw_balls(cr, d_neck_x + d_height - 3*d_girth/4, d_neck_y + d_girth, ball_type, d_girth, d_girth, 1, 1, 1, d_r, d_g, d_b)
    draw_tail(cr, d_neck_x + d_height, d_neck_y + d_girth/2, tail_type, d_height/50, d_girth/1.7, 0, d_r, d_g, d_b)
    draw_crown(cr, d_neck_x, d_neck_y, crown_type, d_height, d_girth, d_r, d_g, d_b)

    ims.write_to_png('Examples/tmp.png')

    pil_image = Image.open('Examples/tmp.png')
    pixels = pil_image.load()

    for i in range(pil_image.size[0]):
        for j in range(pil_image.size[1]):
            r, g, b = pixels[i, j]
            noise = float_gen(1.0 - args.noise, 1.0 + args.noise)
            pixels[i, j] = (int(r * noise), int(g * noise), int(b * noise))

    pil_image.save('Examples/' + codename + '.png')
    os.remove('Examples/tmp.png')


if __name__ == "__main__":
    main()
