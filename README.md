# Paddy Disease Classification Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-repo/paddy-disease-classification)

A comprehensive dataset of paddy (rice) leaf images for disease classification, collected and organized for computer vision and deep learning research in agricultural applications.

**Project page**: `https://www.kaggle.com/competitions/paddy-disease-classification`

## TL;DR

- **Task**: Classification, Object Detection
- **Modality**: RGB
- **Platform**: Ground/Field
- **Real/Synthetic**: Real
- **Images**: 10,407 paddy leaf images across 10 categories (normal, bacterial_leaf_blight, bacterial_leaf_streak, bacterial_panicle_blight, blast, brown_spot, dead_heart, downy_mildew, hispa, tungro)
- **Resolution**: Variable (typically 480×640 pixels or larger)
- **Annotations**: CSV (per-image), COCO JSON (generated)
- **License**: CC BY 4.0
- **Citation**: see below

## Table of Contents

- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

**Original dataset**: `https://www.kaggle.com/competitions/paddy-disease-classification`

This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.

**Local license file**: See `LICENSE` in the root directory.

## Dataset Structure

```
paddy_disease_classification/
├── paddies/                          # Main category directory
│   ├── normal/                        # Normal/healthy subcategory
│   │   ├── csv/                       # CSV annotation files (per-image)
│   │   ├── json/                      # JSON annotation files (per-image)
│   │   ├── images/                    # Image files
│   │   └── sets/                      # Dataset split files
│   │       ├── train.txt              # Training set image list
│   │       ├── val.txt                # Validation set image list
│   │       ├── test.txt               # Test set image list
│   │       ├── all.txt                # All images list
│   │       └── train_val.txt          # Train+val images list
│   ├── bacterial_leaf_blight/         # Bacterial leaf blight subcategory
│   │   └── ...                       # Same structure as normal
│   ├── bacterial_leaf_streak/          # Bacterial leaf streak subcategory
│   │   └── ...                       # Same structure as normal
│   ├── bacterial_panicle_blight/      # Bacterial panicle blight subcategory
│   │   └── ...                       # Same structure as normal
│   ├── blast/                          # Blast subcategory
│   │   └── ...                       # Same structure as normal
│   ├── brown_spot/                     # Brown spot subcategory
│   │   └── ...                       # Same structure as normal
│   ├── dead_heart/                     # Dead heart subcategory
│   │   └── ...                       # Same structure as normal
│   ├── downy_mildew/                   # Downy mildew subcategory
│   │   └── ...                       # Same structure as normal
│   ├── hispa/                          # Hispa subcategory
│   │   └── ...                       # Same structure as normal
│   ├── tungro/                         # Tungro subcategory
│   │   └── ...                       # Same structure as normal
│   └── labelmap.json                  # Label mapping file
│
├── annotations/                       # COCO format JSON files (generated)
│   ├── normal_instances_train.json
│   ├── normal_instances_val.json
│   ├── normal_instances_test.json
│   ├── bacterial_leaf_blight_instances_*.json
│   ├── bacterial_leaf_streak_instances_*.json
│   ├── bacterial_panicle_blight_instances_*.json
│   ├── blast_instances_*.json
│   ├── brown_spot_instances_*.json
│   ├── dead_heart_instances_*.json
│   ├── downy_mildew_instances_*.json
│   ├── hispa_instances_*.json
│   ├── tungro_instances_*.json
│   └── combined_instances_*.json      # Combined multi-category files
│
├── scripts/                           # Utility scripts
│   ├── reorganize_dataset.py          # Reorganize dataset to standard structure
│   ├── create_splits.py                # Create dataset split files
│   ├── convert_to_coco.py              # Convert CSV to COCO format
│   └── generate_coco_annotations.py   # Original COCO annotation generator
│
├── data/                              # Data directory
│   └── origin/                        # Original data (preserved)
│       ├── train_images/              # Original training images
│       ├── test_images/               # Original test images
│       ├── train.csv                  # Original training CSV
│       └── sample_submission.csv      # Sample submission CSV
│
├── LICENSE                            # License file
├── README.md                          # This file
└── requirements.txt                   # Python dependencies
```

Splits provided via `paddies/{subcategory}/sets/*.txt`. List image basenames (no extension). If missing, all images are used.

## Sample Images

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Normal</strong></td>
    <td>
      <img src="paddies/normal/images/100002.jpg" alt="Normal paddy leaf" width="260"/>
      <div align="center"><code>paddies/normal/images/100002.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Bacterial Leaf Blight</strong></td>
    <td>
      <img src="paddies/bacterial_leaf_blight/images/100330.jpg" alt="Bacterial leaf blight" width="260"/>
      <div align="center"><code>paddies/bacterial_leaf_blight/images/100330.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Blast</strong></td>
    <td>
      <img src="paddies/blast/images/100001.jpg" alt="Blast disease" width="260"/>
      <div align="center"><code>paddies/blast/images/100001.jpg</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

### CSV Format

Each image has a corresponding CSV annotation file in `paddies/{subcategory}/csv/{image_name}.csv`:

```csv
#item,x,y,width,height,label
0,0,0,480,640,1
```

For classification tasks, the annotation uses a full-image bounding box `[0, 0, image_width, image_height]` with the category ID as the label.

### COCO Format

The dataset can be converted to COCO format using `scripts/convert_to_coco.py`. Example COCO JSON structure:

```json
{
  "info": {
    "year": 2025,
    "version": "1.0",
    "description": "Paddy Disease Classification normal train split",
    "url": ""
  },
  "images": [
    {
      "id": 1234567890,
      "file_name": "normal/images/100002.jpg",
      "width": 480,
      "height": 640
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1234567890,
      "category_id": 1,
      "bbox": [0, 0, 480, 640],
      "area": 307200,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "normal",
      "supercategory": "paddy_disease"
    }
  ]
}
```

### Label Maps

Label mapping is defined in `paddies/labelmap.json`:

```json
[
  {"object_id": 0, "label_id": 0, "keyboard_shortcut": "0", "object_name": "background"},
  {"object_id": 1, "label_id": 1, "keyboard_shortcut": "1", "object_name": "normal"},
  {"object_id": 2, "label_id": 2, "keyboard_shortcut": "2", "object_name": "bacterial_leaf_blight"},
  ...
]
```

## Stats and Splits

### Image Statistics

| Category | Total Images | Train | Val | Test |
|----------|-------------|-------|-----|------|
| normal | 1,764 | 1,234 | 264 | 266 |
| bacterial_leaf_blight | 479 | 335 | 71 | 73 |
| bacterial_leaf_streak | 380 | 266 | 57 | 57 |
| bacterial_panicle_blight | 337 | 235 | 50 | 52 |
| blast | 1,738 | 1,216 | 260 | 262 |
| brown_spot | 965 | 675 | 144 | 146 |
| dead_heart | 1,442 | 1,009 | 216 | 217 |
| downy_mildew | 620 | 434 | 93 | 93 |
| hispa | 1,594 | 1,115 | 239 | 240 |
| tungro | 1,088 | 761 | 163 | 164 |
| **Total** | **10,407** | **7,280** | **1,557** | **1,570** |

Splits provided via `paddies/{subcategory}/sets/*.txt`. You may define your own splits by editing those files.

## Quick Start

### Convert to COCO Format

```bash
python scripts/convert_to_coco.py --root . --out annotations \
    --categories normal bacterial_leaf_blight blast \
    --splits train val test --combined
```

### Load with COCO API

```python
from pycocotools.coco import COCO

# Load COCO annotation file
coco = COCO('annotations/normal_instances_train.json')

# Get image IDs
img_ids = coco.getImgIds()

# Load image info
img_info = coco.loadImgs(img_ids[0])[0]

# Load annotations
ann_ids = coco.getAnnIds(imgIds=img_ids[0])
anns = coco.loadAnns(ann_ids)
```

### Dependencies

**Required**:
- Pillow>=9.5

**Optional** (for COCO API):
- pycocotools>=2.0.7

Install with:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

### Evaluation Metrics

- **Classification**: Accuracy, Precision, Recall, F1-score
- **Detection**: mAP@[.50:.95], mAP@0.5, mAP@0.75

### Baselines

*Baseline results will be added here as they become available.*

## Datasheet (Data Card)

### Motivation

This dataset was created to support research in automated paddy disease detection and classification using computer vision and deep learning techniques. Early detection of diseases in paddy crops is crucial for maintaining crop yield and quality.

### Composition

The dataset contains 10,407 high-resolution images of paddy leaves across 10 categories:
- **Normal**: Healthy paddy leaves
- **Bacterial Leaf Blight**: Caused by Xanthomonas oryzae
- **Bacterial Leaf Streak**: Caused by Xanthomonas oryzae pv. oryzicola
- **Bacterial Panicle Blight**: Caused by Burkholderia glumae
- **Blast**: Caused by Magnaporthe oryzae
- **Brown Spot**: Caused by Bipolaris oryzae
- **Dead Heart**: Caused by stem borers
- **Downy Mildew**: Caused by Sclerophthora macrospora
- **Hispa**: Caused by Dicladispa armigera
- **Tungro**: Caused by rice tungro virus

### Collection Process

Images were collected from various sources and annotated for disease classification. The dataset includes images of different paddy varieties and growth stages.

### Preprocessing

- Images are organized by disease category
- Each image has corresponding CSV and JSON annotation files
- Full-image bounding boxes are used for classification tasks
- Dataset is split into train/val/test sets (70%/15%/15%)

### Distribution

The dataset is distributed under CC BY 4.0 license. Original data can be accessed through Kaggle competition.

### Maintenance

The dataset is maintained by the community. Issues and contributions are welcome.

## Known Issues and Caveats

1. **Image Format**: Images are primarily in JPEG format with variable resolutions
2. **Annotation Format**: For classification tasks, full-image bounding boxes are used
3. **Class Imbalance**: Some categories have significantly more images than others (e.g., normal: 1,764 vs bacterial_panicle_blight: 337)
4. **Coordinate System**: Bounding boxes use `[x, y, width, height]` format with origin at top-left corner

## License

This dataset is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

Check the original dataset terms and cite appropriately.

See `LICENSE` file for full license text.

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{paddy_disease_classification_2025,
  title={Paddy Disease Classification Dataset},
  author={Kaggle},
  year={2025},
  url={https://www.kaggle.com/competitions/paddy-disease-classification},
  license={CC BY 4.0}
}
```

## Changelog

- **V1.0.0** (2025-12-10): Initial standardized structure and COCO conversion utility
  - Reorganized dataset to standardized structure
  - Created CSV and JSON annotation files
  - Generated dataset splits (train/val/test)
  - Added conversion scripts

## Contact

- **Maintainers**: [Your name/team]
- **Original Authors**: Kaggle Community
- **Source**: `https://www.kaggle.com/competitions/paddy-disease-classification`
