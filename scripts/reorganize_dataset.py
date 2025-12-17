#!/usr/bin/env python3
"""
Reorganize paddy disease classification dataset to standardized structure.
"""

import os
import json
import csv
import shutil
from pathlib import Path
from PIL import Image
import random

# Category mapping: folder name -> label_id
CATEGORIES = [
    "normal",
    "bacterial_leaf_blight",
    "bacterial_leaf_streak",
    "bacterial_panicle_blight",
    "blast",
    "brown_spot",
    "dead_heart",
    "downy_mildew",
    "hispa",
    "tungro"
]

def load_train_csv(train_csv_path):
    """Load train.csv and return a dictionary mapping image_id to label"""
    train_dict = {}
    with open(train_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            train_dict[row['image_id']] = row['label']
    return train_dict

def json_to_csv(json_path, csv_path, category_id):
    """Convert JSON annotation to CSV format"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data.get('images') or not data.get('annotations'):
        return
    
    image_info = data['images'][0]
    annotation = data['annotations'][0]
    
    width = image_info['width']
    height = image_info['height']
    bbox = annotation['bbox']
    
    # CSV format: #item,x,y,width,height,label
    # For classification task, use full image bbox
    with open(csv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['#item', 'x', 'y', 'width', 'height', 'label'])
        writer.writerow([0, bbox[0], bbox[1], bbox[2], bbox[3], category_id])

def reorganize_dataset(root_dir):
    """Reorganize dataset to standardized structure"""
    root = Path(root_dir)
    
    # Create standardized directory structure
    paddies_dir = root / 'paddies'
    paddies_dir.mkdir(exist_ok=True)
    
    # Load train.csv
    train_csv_path = root / 'train.csv'
    train_dict = load_train_csv(train_csv_path)
    print(f"Loaded {len(train_dict)} entries from train.csv")
    
    # Create labelmap.json
    labelmap = [
        {
            "object_id": 0,
            "label_id": 0,
            "keyboard_shortcut": "0",
            "object_name": "background"
        }
    ]
    
    for idx, category in enumerate(CATEGORIES, start=1):
        labelmap.append({
            "object_id": idx,
            "label_id": idx,
            "keyboard_shortcut": str(idx),
            "object_name": category
        })
    
    labelmap_path = paddies_dir / 'labelmap.json'
    with open(labelmap_path, 'w', encoding='utf-8') as f:
        json.dump(labelmap, f, indent=2, ensure_ascii=False)
    print(f"Created {labelmap_path}")
    
    # Process each category
    train_images_dir = root / 'train_images'
    
    for category in CATEGORIES:
        category_dir = train_images_dir / category
        if not category_dir.exists():
            print(f"Warning: {category_dir} does not exist, skipping")
            continue
        
        # Create standardized subcategory directories
        subcategory_dir = paddies_dir / category
        csv_dir = subcategory_dir / 'csv'
        json_dir = subcategory_dir / 'json'
        images_dir = subcategory_dir / 'images'
        sets_dir = subcategory_dir / 'sets'
        
        csv_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)
        sets_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Processing category: {category}")
        
        # Get category ID
        category_id = CATEGORIES.index(category) + 1
        
        # Process images
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            image_files.extend(category_dir.glob(f'*{ext}'))
        
        print(f"  Found {len(image_files)} images")
        
        for img_path in image_files:
            stem = img_path.stem
            
            # Copy image
            dest_img_path = images_dir / img_path.name
            shutil.copy2(img_path, dest_img_path)
            
            # Copy JSON if exists
            json_path = category_dir / f"{stem}.json"
            if json_path.exists():
                dest_json_path = json_dir / json_path.name
                shutil.copy2(json_path, dest_json_path)
                
                # Create CSV from JSON
                csv_path = csv_dir / f"{stem}.csv"
                json_to_csv(json_path, csv_path, category_id)
            else:
                # Create JSON and CSV from image info
                with Image.open(img_path) as img:
                    width, height = img.size
                
                # Create JSON
                image_id = random.randint(1000000000, 9999999999)
                annotation_id = random.randint(1000000000, 9999999999)
                
                json_data = {
                    "info": {
                        "description": "data",
                        "version": "1.0",
                        "year": 2025,
                        "contributor": "search engine",
                        "source": "augmented",
                        "license": {
                            "name": "Creative Commons Attribution 4.0 International",
                            "url": "https://creativecommons.org/licenses/by/4.0/"
                        }
                    },
                    "images": [{
                        "id": image_id,
                        "width": width,
                        "height": height,
                        "file_name": img_path.name,
                        "size": os.path.getsize(img_path),
                        "format": "JPEG",
                        "url": "",
                        "hash": "",
                        "status": "success"
                    }],
                    "annotations": [{
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "segmentation": [],
                        "area": width * height,
                        "bbox": [0, 0, width, height]
                    }],
                    "categories": [{
                        "id": category_id,
                        "name": category,
                        "supercategory": "paddy_disease"
                    }]
                }
                
                dest_json_path = json_dir / f"{stem}.json"
                with open(dest_json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                
                # Create CSV
                csv_path = csv_dir / f"{stem}.csv"
                json_to_csv(dest_json_path, csv_path, category_id)
        
        print(f"  Processed {len(image_files)} images for {category}")
    
    print("\nDataset reorganization completed!")
    print(f"Standardized structure created at: {paddies_dir}")

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    reorganize_dataset(root_dir)





