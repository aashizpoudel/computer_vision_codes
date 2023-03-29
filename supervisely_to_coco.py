import os
import json

# Define the paths to the input and output directories
input_dir = '/content/drive/MyDrive/dataset/Bounding_Box_annotation/'
output_file = '/content/drive/MyDrive/dataset/coco.json'
classes  = ['leaf','true_leaf','cotyledon']
# Define the categories of objects in your annotations
categories = [
    {'id': classes.index(item)+1, 'name': item, 'supercategory': 'object'} for item in classes
]

# Initialize the COCO annotation dictionary
coco_ann = {
    'info': {},
    'licenses': [],
    'images': [],
    'annotations': [],
    'categories': categories,
}

# Define a helper function to convert a bounding box annotation
def convert_bbox_annotation(obj, image_id):
    pt1,pt2 = obj['points']['exterior']
    x1,y1 = pt1
    x2,y2 = pt2 
    width = x2-x1 
    height = y2- y1 
    x,y = x1,y1
    return {
        'id': obj['id'],
        'image_id': image_id,
        'category_id': classes.index(obj['classTitle'])+1,
        'segmentation': [],  # not used for bounding boxes
        'area': width * height,
        'bbox': [x, y, width, height],
        'iscrowd': 0,
    }

# Traverse the input directory and convert each annotation file
for file_name in os.listdir(input_dir):
    if file_name.endswith('.json'):
        file_path = os.path.join(input_dir, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Create a new image entry for this file
            image_id = len(coco_ann['images']) + 1
            image_entry = {
                'id': image_id,
                'file_name': file_name[:-5],  # remove '.json' extension
                'height': data['size']['height'],
                'width': data['size']['width'],
            }
            coco_ann['images'].append(image_entry)
        
        # Traverse the annotations in the file and convert each bounding box
            for obj in data['objects']:
                bbox_ann = convert_bbox_annotation(obj, image_id)
                coco_ann['annotations'].append(bbox_ann)

with open(output_file, 'w') as f:
  json.dump(coco_ann, f)
