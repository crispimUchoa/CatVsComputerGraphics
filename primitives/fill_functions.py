from primitives.draw_functions import *
import math

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

def fill_elipses(surface: Surface, center: coord_type, a: int, b:int, fill_color: color_type):
    xc, yc = center

    for y in range(-b, b + 1):
        v = 1 - (y*y)/(b*b)
        if v < 0:
            continue
        x = int(a * math.sqrt(v))

        for xi in range(-x, x + 1):
            set_pixel(surface, (xc + xi, yc + y), fill_color)

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
