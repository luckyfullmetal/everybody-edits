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
                        
                        # Fast iteration over pixel data including the alpha (a) channel
                        for idx, (r, g, b, a) in enumerate(img.getdata()):
                            if a > 0:  # Skips fully invisible pixels
                                pixels.append({
                                    "x": idx % width,
                                    "y": idx // width,
                                    "r": r,
                                    "g": g,
                                    "b": b,
                                    "a": a  # Stored for transparency in Roblox
                                })
                                
                        block_data[rel_path] = pixels
                        print(f"Processed (with transparency): {rel_path}")
                except Exception as e:
                    print(f"Error {full_path}: {e}")

    # Write ultra-compressed JSON for instant loading speed
    with open("BlockData.json", "w", encoding="utf-8") as f:
        json.dump(block_data, f, separators=(',', ':'))
        
    print("BlockData.json generated successfully!")

if __name__ == "__main__":
    main()
