import cairosvg


def svg_to_png(svg_file_path:str, png_file_path=None):
    assert svg_file_path.endswith(".svg")

    if png_file_path is None:
        png_file_path = svg_file_path[:-4] + ".png"
    
    # 将 SVG 文件转换为 PNG 文件
    cairosvg.svg2png(
        url=svg_file_path,         # 输入 SVG 文件路径
        write_to=png_file_path     # 输出 PNG 文件路径
    )
