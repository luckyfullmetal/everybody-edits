import os
import json
from PIL import Image

def generate_block_data():
    block_data = {}
    assets_dir = "assets"
    
    # Check if the assets directory exists
    if not os.path.exists(assets_dir):
        print(f"Warning: Directory '{assets_dir}' not found.")
        # Write an empty JSON file so the build doesn't fail outright
        with open("BlockData.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
        return

    # Recursively look through all folders and subfolders in 'assets/'
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.lower().endswith(".png"):
                full_path = os.path.join(root, file)
                
                # Create a clean relative path (e.g., "assets/blocks/basic/white.png")
                # and ensure forward slashes are used for cross-platform consistency
                relative_path = os.path.relpath(full_path, ".").replace("\\", "/")
                
                try:
                    img = Image.open(full_path).convert("RGBA")
                    width, height = img.size
                    pixels = []
                    
                    for y in range(height):
                        for x in range(width):
                            r, g, b, a = img.getpixel((x, y))
                            
                            # Optional optimization: Skip fully transparent pixels (alpha == 0)
                            # to keep your JSON file size small and snappy!
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

    # Write out the final data dictionary to BlockData.json
    output_file = "BlockData.json"
    with open(output_file, "w", encoding="utf-8") as f:
        # indent=None keeps the file compact and fast to download over HTTP
        json.dump(block_data, f, indent=None)
        
    print(f"Successfully generated {output_file} containing {len(block_data)} assets.")

if __name__ == "__main__":
    generate_block_data()
