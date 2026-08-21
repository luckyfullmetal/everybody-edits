import os
from PIL import Image

assets_dir = "assets/blocks/basic"
output_lua = "BlockData.lua"

block_data = {}

if os.path.exists(assets_dir):
    for filename in os.listdir(assets_dir):
        if filename.lower().endswith(".png"):
            name = os.path.splitext(filename)[0]
            img_path = os.path.join(assets_dir, filename)
            
            with Image.open(img_path).convert("RGBA") as img:
                width, height = img.size
                pixels = img.load()
                
                pixel_list = []
                for y in range(height):
                    for x in range(width):
                        r, g, b, a = pixels[x, y]
                        # If the pixel is not fully transparent, record it
                        if a > 0:
                            pixel_list.append({
                                "x": x,
                                "y": y,
                                "r": r,
                                "g": g,
                                "b": b
                            })
                
                block_data[name] = pixel_list

# Write out a Luau module file
with open(output_lua, "w") as f:
    f.write("return {\n")
    for block_name, data in block_data.items():
        f.write(f'\t["{block_name}"] = {{\n')
        for p in data:
            f.write(f'\t\t{{x = {p["x"]}, y = {p["y"]}, r = {p["r"]}, g = {p["g"]}, b = {p["b"]}}},\n')
        f.write("\t},\n")
    f.write("}\n")

print("BlockData.lua generated successfully!")
