import io
import random as rnd
from copy import deepcopy
from itertools import product

import cairosvg
import svgwrite
from PIL import Image

from tiles import collect_tiles

L = 400
STRIDE = L * 3
TILE_SIZE = L * 5


def define_frame(col, row, max_depth):
    """タイルの位置(座標)を決める
    Args:
        col (int): 列数
        row (int): 行数
        max_depth (int): タイル分割数
    Returns:
        list<list<tuple>>: サイズごとの枠線座標リスト
    """
    coordinates = []

    # 一番大きいタイルを詰める
    coords = []
    tile_size = 2**max_depth
    for x, y in product(range(col), range(row)):
        coords += [(tile_size * x, tile_size * y)]

    # 大きい順にタイルを詰める
    for i in range(max_depth):
        last_coords = coords
        samples = rnd.sample(last_coords, len(last_coords) // (i + 2))
        tile_size = 2**(max_depth - i - 1)

        coords = []
        for x, y in samples:
            last_coords.remove((x, y))
            for j, k in product(range(2), range(2)):
                coords += [(x + tile_size * j, y + tile_size * k)]

        coordinates.append(last_coords)
        # break

    coordinates.append(coords)

    return coordinates


def draw_frame(coords_list, col, row, max_depth):
    """枠線を画像出力
    Args:
        coords_list (list): サイズごとの枠線座標リスト
        col (int): 列数
        row (int): 行数
        max_depth (int): タイル分割数
    """
    W, H = STRIDE * col + L * 2, STRIDE * row + L * 2
    dwg = svgwrite.Drawing(size=(W, H))
    scale = STRIDE / 2**max_depth

    for i, coords in enumerate(coords_list):
        size = STRIDE / 2**i
        for x, y in coords:
            # 正方形を追加
            dwg.add(dwg.rect(
                insert=(x * scale + L, y * scale + L),
                size=(size, size),
                fill='none', stroke='white',
                stroke_width=10,
            ))

    cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                     write_to='frame.png',
                     scale=2000 / W if W > 2000 else 1)


def svg2img(tile, colors, size):
    """色・サイズ調整，型変換
    Args:
        tile (svgwrite.Drawing): svg
        colors (list): 配色
        size (int): 画像サイズ
    Returns:
        PIL.Image: img
    """
    dwg = deepcopy(tile)

    # 色設定
    dwg.add(dwg.style(f'''
            .color-1 {{fill: {colors[0]};}}
            .color-2 {{fill: {colors[1]};}}
        '''))

    # 型変換 (svgwrite.Drawing -> PIL.Image)
    png_bin = cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                               scale=size / 500)
    img = Image.open(io.BytesIO(png_bin))

    # dwg.saveas('tile.svg', pretty=True, indent=2)
    # img.save('tile.png')
    return img


def draw_truchet(coordinates, col, row, max_depth, colors):
    # ベース画像
    W, H = STRIDE * col + L * 2, STRIDE * row + L * 2
    base_img = Image.new(mode='RGBA', size=(W, H), color=(0, 0, 0, 255))
    # タイルリスト
    tiles = collect_tiles()

    scale = round(STRIDE / 2**max_depth)
    for i, coords in enumerate(coordinates):
        size = round(TILE_SIZE / 2**i)
        pad = round(L - L / 2**i)

        for x, y in coords:
            # タイル選択
            tile = rnd.choice(tiles)
            # 色・サイズ調整，型変換
            tile = svg2img(tile, colors if i % 2 else colors[::-1], size)
            # ペースト
            base_img.alpha_composite(tile, (x * scale + pad, y * scale + pad))

    if W > 2000:
        scale = 2000 / W
        base_img = base_img.resize((round(W * scale), round(H * scale)))
    base_img.save('truchet.png')


def main(col=5, row=5, max_depth=4, colors=('white', 'black')):
    coordinates = define_frame(col, row, max_depth)
    draw_frame(coordinates, col, row, max_depth)
    draw_truchet(coordinates, col, row, max_depth, colors)


if __name__ == '__main__':
    main()
