import os
import re

folder = "media/products"

for filename in os.listdir(folder):
    # Match names like 'choco-swirl-cupcake_llaewg.jpg'
    match = re.match(r"^(.*?)(_[a-z0-9]+)?(\.\w+)$", filename)
    if match:
        new_name = match.group(1) + match.group(3)
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")
