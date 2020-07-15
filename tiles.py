import cairosvg
import svgwrite

N_TILE_TYPES = (2, 2, 1, 1, 1, 4, 4)  # 各タイルの種類数
# パラメータ(type_num, rotate_num)
TILE_PARAMS = [(i, j)
               for i, n_types in enumerate(N_TILE_TYPES)
               for j in range(n_types)]


class Mover:
    """座標を線形移動"""

    def __init__(self, scale, bias):
        self.scale = scale
        self.bias = bias

    def move(self, x, y):
        bx, by = self.bias
        return (x * self.scale + bx, y * self.scale + by)

    def move_path(self, path):
        bx, by = self.bias
        p = path.split()
        if p[0] in ('M', 'L'):
            p[1] = int(p[1]) * self.scale + bx
            p[2] = int(p[2]) * self.scale + by
        elif p[0] == 'A':
            p[1] = int(p[1]) * self.scale
            p[2] = int(p[2]) * self.scale
            p[-2] = int(p[-2]) * self.scale + bx
            p[-1] = int(p[-1]) * self.scale + by
        return ' '.join(map(str, p))


def add_tile(dwg, type_num, rotate_num, scale=1, pos=(0, 0), swap_color=False):
    m = Mover(scale, pos)

    class_1 = 'color-1' if not swap_color else 'color-2'
    class_2 = 'color-2' if not swap_color else 'color-1'

    g1 = dwg.g(class_=class_1)
    g1.add(dwg.rect(insert=m.move(2, 2), size=(6 * scale,) * 2))
    g1.add(dwg.circle(center=m.move(2, 2), r=2 * scale))
    g1.add(dwg.circle(center=m.move(2, 8), r=2 * scale))
    g1.add(dwg.circle(center=m.move(8, 2), r=2 * scale))
    g1.add(dwg.circle(center=m.move(8, 8), r=2 * scale))
    dwg.add(g1)

    # 回転角度・中心
    deg = 90 * rotate_num
    cx, cy = 5 * scale + pos[0], 5 * scale + pos[1]

    g2 = dwg.g(class_=class_2, transform=f'rotate({deg},{cx},{cy})')
    if type_num == 0:
        g2.add(dwg.path(
            d=m.move_path('M 4 2') +
            m.move_path('A 1 1 0 0 1 6 2') +
            m.move_path('A 4 4 0 0 1 2 6') +
            m.move_path('A 1 1 0 0 1 2 4') +
            m.move_path('A 2 2 0 0 0 4 2') +
            'Z'
        ))
        g2.add(dwg.path(
            d=m.move_path('M 8 4') +
            m.move_path('A 1 1 0 0 1 8 6') +
            m.move_path('A 2 2 0 0 0 6 8') +
            m.move_path('A 1 1 0 0 1 4 8') +
            m.move_path('A 4 4 0 0 1 8 4') +
            'Z'
        ))

    elif type_num == 1:
        g2.add(dwg.circle(center=m.move(5, 2), r=scale))
        g2.add(dwg.circle(center=m.move(5, 8), r=scale))
        g2.add(dwg.path(
            d=m.move_path('M 2 4') +
            m.move_path('L 8 4') +
            m.move_path('A 1 1 0 0 1 8 6') +
            m.move_path('L 2 6') +
            m.move_path('A 1 1 0 0 1 2 4') +
            'Z'
        ))

    elif type_num == 2:
        g2.add(dwg.circle(center=m.move(5, 2), r=scale))
        g2.add(dwg.circle(center=m.move(2, 5), r=scale))
        g2.add(dwg.circle(center=m.move(8, 5), r=scale))
        g2.add(dwg.circle(center=m.move(5, 8), r=scale))

    elif type_num == 3:
        g2.add(dwg.path(
            d=m.move_path('M 4 2') +
            m.move_path('A 1 1 0 0 1 6 2') +
            m.move_path('A 2 2 0 0 0 8 4') +
            m.move_path('A 1 1 0 0 1 8 6') +
            m.move_path('A 2 2 0 0 0 6 8') +
            m.move_path('A 1 1 0 0 1 4 8') +
            m.move_path('A 2 2 0 0 0 2 6') +
            m.move_path('A 1 1 0 0 1 2 4') +
            m.move_path('A 2 2 0 0 0 4 2') +
            'Z'
        ))

    elif type_num == 4:
        g2.add(dwg.path(
            d=m.move_path('M 2 4') +
            m.move_path('L 8 4') +
            m.move_path('A 1 1 0 0 1 8 6') +
            m.move_path('L 2 6') +
            m.move_path('A 1 1 0 0 1 2 4') +
            'Z'
        ))
        g2.add(dwg.path(
            d=m.move_path('M 4 2') +
            m.move_path('L 4 8') +
            m.move_path('A 1 1 0 0 0 6 8') +
            m.move_path('L 6 2') +
            m.move_path('A 1 1 0 0 0 4 2') +
            'Z'
        ))

    elif type_num == 5:
        g2.add(dwg.path(
            d=m.move_path('M 4 2') +
            m.move_path('A 1 1 0 0 1 6 2') +
            m.move_path('A 4 4 0 0 1 2 6') +
            m.move_path('A 1 1 0 0 1 2 4') +
            m.move_path('A 2 2 0 0 0 4 2') +
            'Z'
        ))
        g2.add(dwg.circle(center=m.move(8, 5), r=scale))
        g2.add(dwg.circle(center=m.move(5, 8), r=scale))

    elif type_num == 6:
        g2.add(dwg.path(
            d=m.move_path('M 4 2') +
            m.move_path('A 1 1 0 0 1 6 2') +
            m.move_path('A 2 2 0 0 0 8 4') +
            m.move_path('A 1 1 0 0 1 8 6') +
            m.move_path('L 2 6') +
            m.move_path('A 1 1 0 0 1 2 4') +
            m.move_path('A 2 2 0 0 0 4 2') +
            'Z'
        ))
        g2.add(dwg.circle(center=m.move(5, 8), r=scale))

    dwg.add(g2)


if __name__ == '__main__':
    dwg = svgwrite.Drawing()

    for i, (type_num, rotate_num) in enumerate(TILE_PARAMS):
        add_tile(dwg, type_num, rotate_num,
                 scale=1, pos=(10 * (i % 4), 10 * (i // 4)))

    dwg.add(dwg.style('''
        .color-1 {fill: white;}
        .color-2 {fill: black;}
    '''))
    dwg['width'] = 40
    dwg['height'] = 40
    cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                     write_to='tiles.png', scale=50)
