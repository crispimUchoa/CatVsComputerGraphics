import math
from pygame.surface import Surface

color_type = str | tuple[int, int, int]
coord_type = tuple[int, int]

def set_pixel(surface: Surface, xy: coord_type, color: color_type):
    x, y = xy
    if 0 <= 0 < surface.get_width() and 0 <= y < surface.get_height():
        surface.set_at((x,y), color)

def read_pixel(surface: Surface, xy: coord_type):
    return surface.get_at(xy)

def draw_dda_line(surface: Surface, xy0: coord_type, xy1: coord_type, color:color_type):
    x0, y0 = xy0
    x1, y1 = xy1
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))

    if steps > 0:
        x_inc = dx / steps
        y_inc = dy / steps

        x = x0
        y = y0

        for _ in range(steps + 1):
            set_pixel(surface, (round(x), round(y)), color)
            x += x_inc
            y += y_inc

def draw_bressenham_line(surface: Surface, xy0: coord_type, xy1: coord_type, color:color_type):
    x0, y0 = xy0
    x1, y1 = xy1
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            set_pixel(surface, (y, x), color)
        else:
            set_pixel(surface, (x, y), color)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def draw_naive_line(surface: Surface, xy0: coord_type, xy1: coord_type, color:color_type):
    x0, y0 = xy0
    x1, y1 = xy1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0

    if dx == 0:
        return
    
    m = (y1 - y0) / dx
    b = y0 - m*x0

    for x in range(x0, x1 + 1):
        y = m*x + b
        set_pixel(surface, (x, y), color)

def draw_polygon(surface: Surface, vertices: list[coord_type], color: color_type):
    num_v = len(vertices)

    if num_v < 3:
        return

    for i in range(num_v):
        x0, y0 = vertices[i]
        x1, y1 = vertices[(i+1) % num_v]

        draw_bressenham_line(surface, (int(x0), int(y0)), (int(x1), int(y1)), color)

def plot8(surface: Surface, xyc: coord_type, xy: coord_type, color):
    xc, yc = xyc
    x, y = xy
    set_pixel(surface, (xc + x, yc + y), color)
    set_pixel(surface, (xc - x, yc + y), color)
    set_pixel(surface, (xc + x, yc - y), color)
    set_pixel(surface, (xc - x, yc - y), color)

    set_pixel(surface, (xc + y, yc + x), color)
    set_pixel(surface, (xc - y, yc + x), color)
    set_pixel(surface, (xc + y, yc - x), color)
    set_pixel(surface, (xc - y, yc - x), color)

def plot4(surface: Surface, xyc: coord_type, xy: coord_type, color):
    xc, yc = xyc
    x, y = xy

    set_pixel(surface, (xc + x, yc + y), color)
    set_pixel(surface, (xc + x, yc - y), color)
    set_pixel(surface, (xc - x, yc + y), color)
    set_pixel(surface, (xc - x, yc - y), color)



def draw_circle(surface: Surface, center: coord_type, r: int, color: color_type):
    x = 0
    y = r
    d = 1 - r
    
    incE = 2*x + 3
    incSE = 2*(x - y) + 5
    plot8(surface, center, (x, y), color)

    while x < y:
        if d < 0:
            d+= incE
        else:
            d+= incSE
            y -=1
        x+=1
        plot8(surface, center, (x, y), color)

def draw_elipse(surface: Surface, center: coord_type, a: int, b: int, color: color_type):
    a2, b2 = a*a, b*b
    x = 0
    y = b

    dx = 2*x*b2
    dy = 2*y*a2

    d1 = b2 + ( (-1)*b + 1/4)*(a2)
    
    plot4(surface, center, (x, y), color)
    while dx < dy:
        plot4(surface, center, (x, y), color)
        x+=1
        dx += 2 * b2
        if d1 < 0:
            d1 += dx + b2
        else:
            y -= 1
            dy -= 2 * a2
            d1 += dx - dy + a2
            
    d2 = b2 * (x + 1/2)**2 + a2*(y - 1)**2 - a2*b2

    while y >= 0:
        plot4(surface, center, (x, y), color)
        y -= 1
        dy -= 2 * a2

        if d2 > 0:
            d2 += a2 - dy
        else:
            x+=1
            dx += 2*b2
            d2 += dx - dy + a2




def flood_fill(surface: Surface, xy: coord_type, fill_color: color_type, border_color: color_type):
    width = surface.get_width()
    height = surface.get_height()

    stack = [xy, ]

    while stack:
        x, y = stack.pop()

        if not (0 <= x < width and 0 <= y < height):
            continue

        current_color = read_pixel(surface, (x, y))[:3]

        if current_color == border_color or current_color == fill_color:
            continue

        set_pixel(surface, (x, y), fill_color)
        
        stack.append((x + 1, y))
        stack.append((x - 1, y))
        stack.append((x, y + 1))
        stack.append((x, y - 1))

def scanline_fill(surface: Surface, vertices: list[coord_type], fill_color: color_type):
    # Encontra Y minimo e máximo
    ys = [p[1] for p in vertices]
    y_min = int(min(ys))
    y_max = int(max(ys))

    n = len(vertices)

    for y in range(y_min, y_max):
        intersections_x = []

        for i in range(n):
            x0, y0 = vertices[i]
            x1, y1 = vertices[(i + 1) % n]

            #Ignora arestas horizontais
            if y0 == y1:
                continue

            #Garante y0 < y1
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0

            #Regra Ymin <= y < Ymax
            if y < y0 or y >= y1:
                continue

            #Calcula interseção
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            intersections_x.append(x)

        # Ordena interseções
        intersections_x.sort()

        # Preenche entre pares
        for i in range(0, len(intersections_x), 2):
            if i + 1 < len(intersections_x):
                x_start = int(round(intersections_x[i]))
                x_end = int(round(intersections_x[i + 1]))

                for x in range(x_start, x_end + 1):
                    set_pixel(surface, (x, y), fill_color)

def scanline_elipses(surface: Surface, center: coord_type, a: int, b:int, fill_color: color_type):
    xc, yc = center

    for y in range(-b, b + 1):
        v = 1 - (y*y)/(b*b)
        if v < 0:
            continue
        x = int(a * math.sqrt(v))

        for xi in range(-x, x + 1):
            set_pixel(surface, (xc + xi, yc + y), fill_color)

## TRANSFORMAÇÕES
def identity():
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

def translation(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1],
    ]

def scale(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1],
    ]

def rotation(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1],
    ]

def multiply_matrix(a, b):
    r = [[0] *3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r[i][j] +=a[i][k] * b[k][j]
    
    return r

# Composição de transformações
def create_transform():
    return identity()

def transform(m, vertices):
    new = []
    for x,y in vertices:
        v = [x, y, 1]
        x_new = m[0][0]*v[0] + m[0][1]*v[1] + m[0][2]
        y_new = m[1][0]*v[0] + m[1][1]*v[1] + m[1][2]
        new.append((x_new, y_new))

    return new

#Janela -> Viewport
def window_viewport(window, viewport):
    Wxmin, Wymin, Wxmax, Wymax = window
    Vxmin, Vymin, Vxmax, Vymax = viewport

    sx = (Vxmax - Vxmin) / (Wxmax - Wxmin)
    sy = (Vymax - Vymin) / (Wymax - Wymin)

    m = identity()

    m = multiply_matrix(translation(-Wxmin, -Wymin), m)
 
    m = multiply_matrix(scale(sx, sy), m)

    m = multiply_matrix(translation(Vxmin, Vymin), m)

    return m

#####################################

# CLIPPING

#####################################
INSIDE  = 0
LEFT    = 1
RIGHT   = 2
BOTTOM  = 4
TOP     = 8


def region_code(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE

    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    elif y < ymin: code |= TOP
    elif y > ymax: code |= BOTTOM

    return code

def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    c0 = region_code(x0, y0, xmin, ymin, xmax, ymax)
    c1 = region_code(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (c0 | c1):
            return True, x0, y0, x1, y1
    
        if c0 & c1:
            return False, None, None, None, None
        
        c_out = c0 if c0 else c1

        if c_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif c_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif c_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif c_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        if c_out == c0:
            x0, y0 = x, y
            c0 = region_code(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = region_code(x1, y1, xmin, ymin, xmax, ymax)


def scanline_texture(surface: Surface, vertices, uvs, texture):
    n = len(vertices)
    tex_w, tex_h = texture.get_width(), texture.get_height()
    ys = [p[1] for p in vertices]

    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max):
        inter = []

        for i in range(n):
            x0, y0 = vertices[i]
            x1, y1 = vertices[(i+1) % n]

            u0, v0 = uvs[i]
            u1, v1 = uvs[(i+1) % n]

            if y0 == y1:
                continue

            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                u0, v0, u1, v1 = u1, v1, u0, v0

            if y < y0 or y >= y1:
                continue

            t = (y - y0) / (y1 - y0)

            x = x0 + t * (x1 - x0)
            u = u0 + t * (u1 - u0)
            v = v0 + t * (v1 - v0)

            inter.append((x, u, v))

        inter.sort(key=lambda i:i[0])

        for i in range(0, len(inter), 2):
            if i + 1 >= len(inter):
                continue

            x_start, u_start, v_start = inter[i]
            x_end, u_end, v_end = inter[i + 1]

            if x_start == x_end:
                continue

            for x in range(int(x_start), int(x_end) + 1):
                t = (x - x_start) / (x_end - x_start)

                u = u_start + t * (u_end - u_start)
                v = v_start + t * (v_end - v_start)

                tx = int(u * (tex_w - 1))
                ty = int(v * (tex_h - 1))

                if 0 <= tx < tex_w and 0 <= ty < tex_h:
                    color = texture.get_at((tx, ty))
                    set_pixel(surface, (x, y), color)
