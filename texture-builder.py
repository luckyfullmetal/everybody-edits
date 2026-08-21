import os
import json
from PIL import Image

def generate_block_data():
    block_data = {}
    assets_dir = "assets"
    
    if not os.path.exists(assets_dir):
        print(f"Warning: Directory '{assets_dir}' not found.")
        with open("BlockData.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
        return

    # Step 1: Physically rename all files and folders inside 'assets/' to lowercase.
    # topdown=False ensures we rename inner files/folders before their parents.
    for root, dirs, files in os.walk(assets_dir, topdown=False):
        for file in files:
            if file.lower().endswith(".png"):
                old_path = os.path.join(root, file)
                new_file = file.lower()
                new_path = os.path.join(root, new_file)
                if old_path != new_path:
                    os.rename(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                    
        for d in dirs:
            old_dir_path = os.path.join(root, d)
            new_dir = d.lower()
            new_dir_path = os.path.join(root, new_dir)
            if old_dir_path != new_dir_path:
                os.rename(old_dir_path, new_dir_path)
                print(f"Renamed directory: {old_dir_path} -> {new_dir_path}")

    # Step 2: Walk through the cleaned assets folder and build the JSON data
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.lower().endswith(".png"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, ".").replace("\\", "/")
                
                try:
                    img = Image.open(full_path).convert("RGBA")
                    width, height = img.size
                    pixels = []
                    
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = img.getpixel((x, y))
                            
                            if a > 0:
                                pixels.append({
                                    "x": x,
                                    "y": y,
                                    "r": r,
                                    "g": g,
                                    "b": b
                                })
                                
                    block_data[relative_path] = pixels
                    print(f"Successfully processed: {relative_path}")
                    
                except Exception as e:
                    print(f"Error processing image {full_path}: {e}")

    output_file = "BlockData.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(block_data, f, indent=None)
        
    print(f"Successfully generated {output_file} containing {len(block_data)} assets.")

if __name__ == "__main__":
    generate_block_data()
