import os
from PIL import Image

root_assets_dir = "assets"
output_lua = "BlockData.lua"

block_data = {}

if os.path.exists(root_assets_dir):
    # os.walk goes through all subfolders recursively
    for dirpath, _, filenames in os.walk(root_assets_dir):
        for filename in filenames:
            if filename.lower().endswith(".png"):
                # Get the full relative path, e.g., "assets/blocks/basic/white.png"
                full_path = os.path.join(dirpath, filename).replace("\\", "/")
                
                # Optional: lowercase the key to prevent capitalization typos in Roblox
                key_name = full_path.lower()
                
                img_path = os.path.join(dirpath, filename)
                with Image.open(img_path).convert("RGBA") as img:
                    width, height = img.size
                    pixels = img.load()
                    
                    pixel_list = []
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = pixels[x, y]
                            if a > 0:  # If not fully transparent
                                pixel_list.append({
                                    "x": x,
                                    "y": y,
                                    "r": r,
                                    "g": g,
                                    "b": b
                                })
                    
                    block_data[key_name] = pixel_list

# Write out the Luau module file
with open(output_lua, "w") as f:
    f.write("return {\n")
    for path_key, data in block_data.items():
        f.write(f'\t["{path_key}"] = {{\n')
        for p in data:
            f.write(f'\t\t{{x = {p["x"]}, y = {p["y"]}, r = {p["r"]}, g = {p["g"]}, b = {p["b"]}}},\n')
        f.write("\t},\n")
    f.write("}\n")

print("BlockData.lua generated successfully with recursive paths!")
