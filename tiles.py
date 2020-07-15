import cairosvg
import svgwrite

N_TYPES = 7  # タイル種類数
N_ROTATIONS = (2, 2, 1, 1, 1, 4, 4)  # 各種類の回転数


def create_tile(type_num, rotate_num):
    """タイル作成
    Args:
        type_num (int): 種類番号
        rotate_num (int): 90°回転の回数, 0~3
    Returns:
        svgwrite.Drawing
    """
    dwg = svgwrite.Drawing(size=(500, 500))

    g1 = dwg.g(class_='color-1')
    g1.add(dwg.rect(insert=(100, 100), size=(300, 300)))
    g1.add(dwg.circle(center=(100, 100), r=100))
    g1.add(dwg.circle(center=(100, 400), r=100))
    g1.add(dwg.circle(center=(400, 100), r=100))
    g1.add(dwg.circle(center=(400, 400), r=100))
    dwg.add(g1)

    g2 = dwg.g(class_='color-2')
    if type_num == 0:
        g2.add(dwg.path(
            d='M 200 100\n\
            A 50 50 0 0 1 300 100\n\
            A 200 200 0 0 1 100 300\n\
            A 50 50 0 0 1 100 200\n\
            A 100 100 0 0 0 200 100\n\
            Z'
        ))
        g2.add(dwg.path(
            d='M 400 200\n\
            A 50 50 0 0 1 400 300\n\
            A 100 100 0 0 0 300 400\n\
            A 50 50 0 0 1 200 400\n\
            A 200 200 0 0 1 400 200\n\
            Z'
        ))

    elif type_num == 1:
        g2.add(dwg.circle(center=(250, 100), r=50))
        g2.add(dwg.circle(center=(250, 400), r=50))
        g2.add(dwg.path(
            d='M 100 200\n\
            L 400 200\n\
            A 50 50 0 0 1 400 300\n\
            L 100 300\n\
            A 50 50 0 0 1 100 200\n\
            Z'
        ))

    elif type_num == 2:
        g2.add(dwg.circle(center=(250, 100), r=50))
        g2.add(dwg.circle(center=(100, 250), r=50))
        g2.add(dwg.circle(center=(400, 250), r=50))
        g2.add(dwg.circle(center=(250, 400), r=50))

    elif type_num == 3:
        g2.add(dwg.path(
            d='M 200 100\n\
            A 50 50 0 0 1 300 100\n\
            A 100 100 0 0 0 400 200\n\
            A 50 50 0 0 1 400 300\n\
            A 100 100 0 0 0 300 400\n\
            A 50 50 0 0 1 200 400\n\
            A 100 100 0 0 0 100 300\n\
            A 50 50 0 0 1 100 200\n\
            A 100 100 0 0 0 200 100\n\
            Z'
        ))

    elif type_num == 4:
        g2.add(dwg.path(
            d='M 100 200\n\
            L 400 200\n\
            A 50 50 0 0 1 400 300\n\
            L 100 300\n\
            A 50 50 0 0 1 100 200\n\
            Z'
        ))
        g2.add(dwg.path(
            d='M 200 100\n\
            L 200 400\n\
            A 50 50 0 0 0 300 400\n\
            L 300 100\n\
            A 50 50 0 0 0 200 100\n\
            Z'
        ))

    elif type_num == 5:
        g2.add(dwg.path(
            d='M 200 100\n\
            A 50 50 0 0 1 300 100\n\
            A 200 200 0 0 1 100 300\n\
            A 50 50 0 0 1 100 200\n\
            A 100 100 0 0 0 200 100\n\
            Z'
        ))
        g2.add(dwg.circle(center=(400, 250), r=50))
        g2.add(dwg.circle(center=(250, 400), r=50))

    elif type_num == 6:
        g2.add(dwg.path(
            d='M 200 100\n\
            A 50 50 0 0 1 300 100\n\
            A 100 100 0 0 0 400 200\n\
            A 50 50 0 0 1 400 300\n\
            L 100 300\n\
            A 50 50 0 0 1 100 200\n\
            A 100 100 0 0 0 200 100\n\
            Z'
        ))
        g2.add(dwg.circle(center=(250, 400), r=50))

    dwg.add(g2)

    # 回転
    if rotate_num:
        deg = 90 * rotate_num
        dwg.add(dwg.style(f'''
            .color-2 {{transform: rotate({deg},250,250)}}
        '''))

    return dwg


def collect_tiles():
    """全タイルを生成，リスト化
    Returns:
        list<svgwrite.Drawing>: タイルのリスト
    """
    tiles = []
    for type_num in range(N_TYPES):
        for rotate_num in range(N_ROTATIONS[type_num]):
            tiles.append(create_tile(type_num, rotate_num))

    return tiles


if __name__ == '__main__':
    tiles = collect_tiles()

    import os
    os.makedirs('tiles', exist_ok=True)
    for i, tile in enumerate(tiles):
        tile.add(tile.style('''
            .color-1 {fill: white;}
            .color-2 {fill: black;}
        '''))
        cairosvg.svg2png(tile.tostring().encode('utf-8'),
                         write_to=f'tiles/tile_{i}.png')
