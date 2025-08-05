from PIL import Image, ImageDraw, ImageFont
from random import randint as rnd
from math import sqrt, pi
import numpy as np
import imageio.v2 as imageio

# ========== CONFIG ==========
ascii_path = "./saturn.jpg"
output_video = "animation1.mp4"
font_path = "./hackfont/Hack-Regular.ttf"
font_size = 12
screen_width, screen_height = screen_size = (1920, 1080)
bg_color = (5, 0, 5)
frames = 240
fps = 60

ASCII_CHARS = "@%#*+=-:. "
font = ImageFont.truetype(font_path, font_size)
font_width = font.getlength("0")

def image_to_ascii(path, width=100):
    try:
        image = Image.open(path)
    except Exception as e:
        return f"Error: {e}"

    w, h = image.size
    image = image.resize((width, int(h / w * width * 0.55)))
    image = image.convert("L")

    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255] for pixel in pixels)
    return "\n".join(ascii_str[i:i + width] for i in range(0, len(ascii_str), width))

def generate_background(line_width, line_count):
    return [''.join([str(rnd(0,1)) for _ in range(line_width)]) for _ in range(line_count)]

art = image_to_ascii(ascii_path)
ascii_lines = art.split('\n')
ascii_width = len(ascii_lines[0])
ascii_height = len(ascii_lines)

line_width = int(screen_width / font_width) + 1
line_count = int(screen_height / font_size)

x_start = int(line_width / 2 - ascii_width / 2) * font_width
y_start = int(line_count / 2 - ascii_height / 2) * font_size
x_end = x_start + font_width * ascii_width
y_end = y_start + font_size * ascii_height
total_distance = sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2)

background = generate_background(line_width, line_count)
start_color = (255, 0, 255)    # Magenta
end_color   = (255, 165, 0)    # Orange

bg_img = Image.new('RGB', screen_size, color=bg_color)
bg_draw = ImageDraw.Draw(bg_img)
for y in range(len(background)): bg_draw.text((0, font_size * y), background[y], fill=(30, 30, 30), font=font)

with imageio.get_writer(output_video, fps=fps, codec='libx264') as writer:
    print("starting")
    for frame_idx in range(int(frames/2)+1):
        print(f"Generating frame {frame_idx+1}/{frames}", end='\r')
        img = Image.new('RGB', screen_size, color=bg_color)
        draw = ImageDraw.Draw(img)

        copy = bg_img.copy()
        img.paste(copy, (0,0))

        t = frame_idx / (frames/2 - 1)

        x = x_start
        y = y_start

        for char in art:
            if char not in " \n":
                dt = sqrt((x_end - x) ** 2 + (y_end - y) ** 2) / total_distance

                # Looping gradient scroll:
                mix = dt + t
                if mix >= 1:
                    mix = 1 - (mix % 1)
                
                color = tuple(
                    int(start_color[i] + (end_color[i] - start_color[i]) * mix)
                    for i in range(3)
                )

                draw.rectangle((x, y, x + font_width, y + font_size), fill=bg_color)
                draw.text((x, y), char, fill=color, font=font)
                x += font_width
            elif char == " ":
                x += font_width
            else:
                x = x_start
                y += font_size
        writer.append_data(np.array(img))

    temp = start_color
    start_color = end_color
    end_color = temp

    for frame_idx in range(int(frames/2)):
        print(f"Generating frame {frame_idx+1 + int(frames/2)}/{frames}", end='\r')
        img = Image.new('RGB', screen_size, color=bg_color)
        draw = ImageDraw.Draw(img)

        copy = bg_img.copy()
        img.paste(copy, (0,0))

        t = frame_idx / (frames/2 - 1)

        x = x_start
        y = y_start

        for char in art:
            if char not in " \n":
                dt = sqrt((x_end - x) ** 2 + (y_end - y) ** 2) / total_distance

                # Looping gradient scroll:
                mix = dt + t
                if mix >= 1:
                    mix = 1 - (mix % 1)
                
                color = tuple(
                    int(start_color[i] + (end_color[i] - start_color[i]) * mix)
                    for i in range(3)
                )

                draw.rectangle((x, y, x + font_width, y + font_size), fill=bg_color)
                draw.text((x, y), char, fill=color, font=font)
                x += font_width
            elif char == " ":
                x += font_width
            else:
                x = x_start
                y += font_size
        writer.append_data(np.array(img))
print()