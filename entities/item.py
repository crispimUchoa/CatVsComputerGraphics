from primitives.transform_functions import create_transform, multiply_matrix, scale, transform, translation


class Item:
    def __init__(self, position, name, w, h, texture):
        self.position = position
        self.name = name
        self.w = w
        self.h = h
        self.texture = texture
        self.is_in_inventory = False

        self.uv = [
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)
        ]
        x, y = self.position
        self.vertices = [
            (x, y),
            (x + self.w, y),
            (x + self.w, y + self.h),
            (x, y+ self.h),

        ]


    # Aplica transformações da animação dos items e retorna seus vertices transformados -------------
    def draw_sprite(self, s, var_ty):
        if self.is_in_inventory:
            return
        
        cx = sum([p[0] for p in self.vertices ])/ len(self.vertices)
        cy = sum([p[1] for p in self.vertices]) / len(self.vertices)

        m = create_transform()
        m = multiply_matrix(translation(-cx, -cy), m)
        m = multiply_matrix(scale(s, s), m)
        m = multiply_matrix(translation(cx, cy), m)
        m = multiply_matrix(translation(0, var_ty), m)

        item_sprite = transform(m, self.vertices)

        return item_sprite

    # Verifica se o player consegue pegar o item pela posição ------------------------------
    def can_get(self, x, y):
        if self.is_in_inventory:
            return False
        px, py = self.position
        return (px-4 <= x <= px +4 + self.w) and (py - 4<= y <= py +4 +self.h)