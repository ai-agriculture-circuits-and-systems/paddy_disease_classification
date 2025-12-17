#!/usr/bin/env python3
"""
Create dataset split files for paddy disease classification dataset.
"""

import os
import random
from pathlib import Path
from collections import defaultdict

# Category list
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

# Split ratios
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def create_splits(root_dir, seed=42):
    """Create dataset split files"""
    root = Path(root_dir)
    paddies_dir = root / 'paddies'
    
    random.seed(seed)
    
    # Collect all images per category
    all_images = defaultdict(list)
    
    for category in CATEGORIES:
        images_dir = paddies_dir / category / 'images'
        if not images_dir.exists():
            continue
        
        # Get all image files
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            for img_path in images_dir.glob(f'*{ext}'):
                all_images[category].append(img_path.stem)
        
        print(f"{category}: {len(all_images[category])} images")
    
    # Create splits for each category
    for category in CATEGORIES:
        if category not in all_images:
            continue
        
        images = all_images[category]
        random.shuffle(images)
        
        total = len(images)
        train_end = int(total * TRAIN_RATIO)
        val_end = train_end + int(total * VAL_RATIO)
        
        train_images = images[:train_end]
        val_images = images[train_end:val_end]
        test_images = images[val_end:]
        
        sets_dir = paddies_dir / category / 'sets'
        sets_dir.mkdir(parents=True, exist_ok=True)
        
        # Write split files
        with open(sets_dir / 'train.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(train_images) + '\n')
        
        with open(sets_dir / 'val.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(val_images) + '\n')
        
        with open(sets_dir / 'test.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_images) + '\n')
        
        with open(sets_dir / 'all.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(images) + '\n')
        
        with open(sets_dir / 'train_val.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(train_images + val_images) + '\n')
        
        print(f"{category}: train={len(train_images)}, val={len(val_images)}, test={len(test_images)}")
    
    print("\nSplit files created successfully!")

if __name__ == "__main__":
    import sys
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 42
    create_splits(root_dir, seed)





