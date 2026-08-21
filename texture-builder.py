import os
import json
from PIL import Image

def main():
    block_data = {}
    assets_dir = "assets"
    
    if not os.path.exists(assets_dir):
        with open("BlockData.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
        return

    for root, _, files in os.walk(assets_dir):
        for file in files:
            if file.lower().endswith(".png"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ".").replace("\\", "/").lower()
                
                try:
                    with Image.open(full_path).convert("RGBA") as img:
                        width, height = img.size
                        pixels = []
                        
                        # Fast linear iteration including alpha ('a')
                        for idx, (r, g, b, a) in enumerate(img.getdata()):
                            if a > 0:
                                pixels.append({
                                    "x": idx % width,
                                    "y": idx // width,
                                    "r": r,
                                    "g": g,
                                    "b": b,
                                    "a": a  # <--- Added alpha channel tracking
                                })
                                
                        block_data[rel_path] = pixels
                        print(f"Processed: {rel_path}")
                except Exception as e:
                    print(f"Error {full_path}: {e}")

    # Write ultra-compressed JSON
    with open("BlockData.json", "w", encoding="utf-8") as f:
        json.dump(block_data, f, separators=(',', ':'))
        
    print("BlockData.json generated successfully!")

if __name__ == "__main__":
    main()
