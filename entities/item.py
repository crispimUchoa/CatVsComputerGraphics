from primitives.fill_functions import scanline_texture
from primitives.transform_functions import create_transform, multiply_matrix, scale, transform, translation


class Item:
    def __init__(self, position, name, w, h, texture):
        self.position = position
        self.name = name
        self.w = w
        self.h = h
        self.texture = texture

    def draw_sprite(self, surface, s, var_ty):
        x, y = self.position
        vertices = [
            (x, y),
            (x + self.w, y),
            (x + self.w, y + self.h),
            (x, y+ self.h),

        ]
        uv = [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        ]

        cx = sum([p[0] for p in vertices ])/ len(vertices)
        cy = sum([p[1] for p in vertices]) / len(vertices)

        m = create_transform()
        m = multiply_matrix(translation(-cx, -cy), m)
        m = multiply_matrix(scale(s, s), m)
        m = multiply_matrix(translation(cx, cy), m)
        m = multiply_matrix(translation(0, var_ty), m)
        item_sprite = transform(m, vertices)

        scanline_texture(surface, item_sprite, uv, self.texture)

    def can_get(self, x, y):
        px, py = self.position
        return (px <= x <= px + self.w) and (py <= y <= py + self.h)