"""Create the Session 5 SYNTHETIC images sample.
 
NOT real traffic data and NOT the official IDD release. The 'objects' are
coloured rectangles drawn exactly where the annotation boxes are, so you can
see that the boxes are read correctly.
 
Run from the project root:  python make_sample_idd.py
Creates:
  data/idd/images/traffic_001.jpg
  data/idd/images/traffic_002.jpg
  data/idd/images/traffic_003.jpg
  data/idd/annotations/instances.json
"""
import json
from pathlib import Path
 
from PIL import Image, ImageDraw
 
root = Path(__file__).resolve().parent
image_dir = root / "data" / "idd" / "images"
ann_dir = root / "data" / "idd" / "annotations"
image_dir.mkdir(parents=True, exist_ok=True)
ann_dir.mkdir(parents=True, exist_ok=True)
 
categories = [
    {"id": 1, "name": "car",        "supercategory": "vehicle"},
    {"id": 2, "name": "motorcycle", "supercategory": "vehicle"},
    {"id": 3, "name": "pedestrian", "supercategory": "person"},
    {"id": 4, "name": "bus",        "supercategory": "vehicle"},
    {"id": 5, "name": "truck",      "supercategory": "vehicle"},
]
images = [
    {"id": 1, "file_name": "traffic_001.jpg", "width": 1280, "height": 720},
    {"id": 2, "file_name": "traffic_002.jpg", "width": 1280, "height": 720},
    {"id": 3, "file_name": "traffic_003.jpg", "width": 1280, "height": 720},
    {"id": 4, "file_name": "traffic_004.jpg", "width": 1280, "height": 720},
]
# bbox = [x, y, width, height], x and y = top-left corner, in pixels
annotations = [
    {"id": 1, "image_id": 1, "category_id": 1, "bbox": [100, 180, 260, 150], "area": 39000,  "iscrowd": 0},
    {"id": 2, "image_id": 1, "category_id": 3, "bbox": [500, 200,  60, 160], "area":  9600,  "iscrowd": 0},
    {"id": 3, "image_id": 1, "category_id": 2, "bbox": [700, 300, 120, 140], "area": 16800,  "iscrowd": 0},
    {"id": 4, "image_id": 2, "category_id": 4, "bbox": [200, 150, 400, 300], "area": 120000, "iscrowd": 0},
    {"id": 5, "image_id": 2, "category_id": 5, "bbox": [800, 250, 300, 200], "area":  60000, "iscrowd": 0},
    {"id": 6, "image_id": 3, "category_id": 1, "bbox": [100, 180, 260, 150], "area": 39000,  "iscrowd": 0},
    {"id": 7, "image_id": 3, "category_id": 2, "bbox": [700, 300, 120, 140], "area": 16800,  "iscrowd": 0},
    {"id": 8, "image_id": 3, "category_id": 4, "bbox": [200, 150, 400, 300], "area": 120000, "iscrowd": 0},
    {"id": 9, "image_id": 4, "category_id": 1, "bbox": [ 80, 100, 300, 180], "area": 54000,  "iscrowd": 0},
    {"id":10, "image_id": 4, "category_id": 3, "bbox": [450, 200,  70, 180], "area": 12600,  "iscrowd": 0},
    {"id":11, "image_id": 4, "category_id": 5, "bbox": [700, 180, 350, 220], "area": 77000,  "iscrowd": 0},
    {"id":12, "image_id": 4, "category_id": 2, "bbox": [300, 420, 130, 160], "area": 20800,  "iscrowd": 0},
]
 
fill = {1: (112, 110, 190),   # car        — blue-purple
        2: ( 95, 185, 105),   # motorcycle — green
        3: (185, 148,  70),   # pedestrian — golden brown
        4: (200, 120, 120),   # bus        — red
        5: (150, 150, 150)}   # truck      — grey

for info in images:
    canvas = Image.new("RGB", (info["width"], info["height"]), (225, 225, 225))
    draw = ImageDraw.Draw(canvas)
    for a in annotations:
        if a["image_id"] == info["id"]:
            x, y, w, h = a["bbox"]
            colour = fill.get(a["category_id"], (100, 100, 100))
            draw.rectangle([x, y, x + w, y + h], fill=colour, outline=(0, 0, 0), width=2)
    out_path = image_dir / info["file_name"]
    canvas.save(out_path)
    print("Saved", out_path)

coco = {"images": images, "categories": categories, "annotations": annotations}
json_path = ann_dir / "instances.json"
json_path.write_text(json.dumps(coco, indent=2))
print("Saved", json_path)
print("Done — 3 images and instances.json created.")
