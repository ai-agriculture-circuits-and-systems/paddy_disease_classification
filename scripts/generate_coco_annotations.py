import os
import json
import random
import time
import csv
from PIL import Image

def generate_unique_id():
    """Generate unique ID: 7 random digits + 3 digit timestamp"""
    random_part = random.randint(1000000, 9999999)
    timestamp_part = int(time.time() * 1000) % 1000
    return int(f"{random_part}{timestamp_part:03d}")

def get_image_info(image_path):
    """Get image information"""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            file_size = os.path.getsize(image_path)
            return width, height, file_size
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return 512, 512, 0

def create_coco_annotation(image_path, category_name, image_id, annotation_id):
    """Create COCO format annotation"""
    width, height, file_size = get_image_info(image_path)
    file_name = os.path.basename(image_path)
    
    # Create image info
    image_info = {
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": file_name,
        "size": file_size,
        "format": "JPEG",
        "url": "",
        "hash": "",
        "status": "success"
    }
    
    # Create annotation info
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": 7,  # Default category ID
        "segmentation": [],
        "area": width * height,
        "bbox": [0, 0, width, height]
    }
    
    # Create category info
    category_info = {
        "id": 7,
        "name": category_name,
        "supercategory": "Paddy Disease"
    }
    
    # Create COCO format JSON
    coco_data = {
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
        "images": [image_info],
        "annotations": [annotation_info],
        "categories": [category_info]
    }
    
    return coco_data

def read_train_csv(root_dir='.'):
    """Read train.csv and return a dictionary mapping image_id to label"""
    train_dict = {}
    train_csv_path = os.path.join(root_dir, 'data', 'origin', 'train.csv')
    try:
        with open(train_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                train_dict[row['image_id']] = row['label']
    except Exception as e:
        print(f"Error reading {train_csv_path}: {e}")
    return train_dict

def read_sample_submission_csv(root_dir='.'):
    """Read sample_submission.csv and return list of image_ids"""
    test_images = []
    sample_submission_path = os.path.join(root_dir, 'data', 'origin', 'sample_submission.csv')
    try:
        with open(sample_submission_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_images.append(row['image_id'])
    except Exception as e:
        print(f"Error reading {sample_submission_path}: {e}")
    return test_images

def process_train_images(root_dir='.'):
    """Process train_images and generate annotations based on train.csv"""
    print("Processing train_images...")
    
    # Read train.csv
    train_dict = read_train_csv(root_dir)
    print(f"Loaded {len(train_dict)} entries from train.csv")
    
    # Process each subfolder in train_images
    train_images_dir = os.path.join(root_dir, 'data', 'origin', 'train_images')
    if not os.path.exists(train_images_dir):
        print(f"Directory {train_images_dir} does not exist")
        return
        
    for category_folder in os.listdir(train_images_dir):
        category_path = os.path.join(train_images_dir, category_folder)
        if os.path.isdir(category_path):
            print(f"Processing category: {category_folder}")
            
            for image_file in os.listdir(category_path):
                if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(category_path, image_file)
                    
                    # Get category from train.csv if available, otherwise use folder name
                    category_name = train_dict.get(image_file, category_folder)
                    
                    # Generate unique IDs
                    image_id = generate_unique_id()
                    annotation_id = generate_unique_id()
                    
                    # Create COCO annotation
                    coco_data = create_coco_annotation(image_path, category_name, image_id, annotation_id)
                    
                    # Save JSON file next to the image
                    json_filename = os.path.splitext(image_file)[0] + '.json'
                    json_path = os.path.join(category_path, json_filename)
                    
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(coco_data, f, indent=2, ensure_ascii=False)
                    
                    print(f"Generated annotation for {image_file}")

def process_test_images(root_dir='.'):
    """Process test_images and generate annotations based on sample_submission.csv"""
    print("Processing test_images...")
    
    # Read sample_submission.csv
    test_images = read_sample_submission_csv(root_dir)
    print(f"Loaded {len(test_images)} entries from sample_submission.csv")
    
    test_images_dir = os.path.join(root_dir, 'data', 'origin', 'test_images')
    if not os.path.exists(test_images_dir):
        print(f"Directory {test_images_dir} does not exist")
        return
        
    for image_file in os.listdir(test_images_dir):
        if image_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(test_images_dir, image_file)
            
            # For test images, we don't have labels, so use a default category
            category_name = "test_image"
            
            # Generate unique IDs
            image_id = generate_unique_id()
            annotation_id = generate_unique_id()
            
            # Create COCO annotation
            coco_data = create_coco_annotation(image_path, category_name, image_id, annotation_id)
            
            # Save JSON file next to the image
            json_filename = os.path.splitext(image_file)[0] + '.json'
            json_path = os.path.join(test_images_dir, json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(coco_data, f, indent=2, ensure_ascii=False)
            
            print(f"Generated annotation for {image_file}")

def main():
    """Main function to generate COCO annotations"""
    import sys
    
    # Get root directory (script directory's parent)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    
    print("Starting COCO annotation generation...")
    print(f"Root directory: {root_dir}")
    
    # Process train images
    process_train_images(root_dir)
    
    # Process test images
    process_test_images(root_dir)
    
    print("COCO annotation generation completed!")

if __name__ == "__main__":
    main() 