import random as rnd
from itertools import product

import cairosvg
import svgwrite

from tiles import TILE_PARAMS, add_tile


def decide_frame_position(col, row, max_depth):
    """タイルの位置(座標)を決める
    Args:
        col (int): 列数
        row (int): 行数
        max_depth (int): タイル分割数
    Returns:
        list<list<tuple>>: サイズごとの枠線座標リスト
    """
    frame_positions = []

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

        frame_positions.append(last_coords)
        # break

    frame_positions.append(coords)

    return frame_positions


def draw_frame(frame_positions, col, row, max_depth):
    """枠線を画像出力
    Args:
        frame_positions (list): サイズごとの枠線座標リスト
        col (int): 列数
        row (int): 行数
        max_depth (int): タイル分割数
    """
    dwg = svgwrite.Drawing()

    for i, coords in enumerate(frame_positions):
        pad = 2**max_depth * 3
        scale = 2**(max_depth - i)

        for x, y in coords:
            # 正方形を追加
            dwg.add(dwg.rect(
                insert=(x * 6 + pad, y * 6 + pad),
                size=(6 * scale, 6 * scale),
                fill='none', stroke='white',
                stroke_width=0.5,
            ))

    # 範囲設定
    dwg['width'] = (6 * col + 6) * 2**max_depth
    dwg['height'] = (6 * row + 6) * 2**max_depth

    cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                     write_to='frame.png', scale=2000 / dwg['width'])


def draw_truchet(frame_positions, col, row, max_depth, colors):
    dwg = svgwrite.Drawing()

    for i, coords in enumerate(frame_positions):
        pad = 2**max_depth * 3 - 2**(max_depth - i) * 2
        scale = 2**(max_depth - i)

        for x, y in coords:
            type_num, rotate_num = rnd.choice(TILE_PARAMS)
            add_tile(dwg, type_num, rotate_num, scale=scale,
                     pos=(x * 6 + pad, y * 6 + pad), swap_color=i % 2)

    # 範囲設定
    dwg['width'] = (6 * col + 6) * 2**max_depth
    dwg['height'] = (6 * row + 6) * 2**max_depth

    # 色設定
    dwg.add(dwg.style(f'''
        .color-1 {{fill: {colors[0]};}}
        .color-2 {{fill: {colors[1]};}}
    '''))

    cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                     write_to='truchet.png', scale=2000 / dwg['width'])


def main(col=5, row=5, max_depth=5, colors=('white', 'black')):
    frame_positions = decide_frame_position(col, row, max_depth)
    draw_frame(frame_positions, col, row, max_depth)
    draw_truchet(frame_positions, col, row, max_depth, colors)


if __name__ == '__main__':
    main()
