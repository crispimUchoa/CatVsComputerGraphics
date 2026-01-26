import math

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
