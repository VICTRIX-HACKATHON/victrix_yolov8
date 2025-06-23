# -*- coding: utf-8 -*-
"""
Code used for training and evaluation to set benchmark results

"""

!nvidia-smi

from google.colab import drive
drive.mount('/content/gdrive')

!cp /content/drive/MyDrive/data /content

!pip install ultralytics
!pip install seaborn

from ultralytics import YOLO

model = YOLO("yolov8s.pt")

# Train the model using config.yaml file
model.train(data="/content/gdrive/MyDrive/yolo_params.yaml", epochs=60, imgsz=640, batch=16)

!yolo detect predict model=runs/detect/train/weights/best.pt source=/content/gdrive/MyDrive/data/test/images save=True

import glob
from IPython.display import Image, display
for image_path in glob.glob(f'/content/runs/detect/predict/*.jpg')[:10]:
  display(Image(filename=image_path, height=400))
  print('\n')

metrics = model.val()
print(metrics.box.map)   # mAP@0.5
print(metrics.box.map50) # mAP@0.5
print(metrics.box.map75) # mAP@0.75
print(metrics.box.maps)  # Per-class mAPs

from ultralytics import YOLO

# Load your trained model
model = YOLO("runs/detect/train/weights/best.pt")
# Evaluate on the test set
metrics = model.val(split='test', data='/content/gdrive/MyDrive/yolo_params.yaml')

# Print test mAP values
print("mAP50:", metrics.box.map50)
print("mAP50-95:", metrics.box.map)
print("Per-class mAPs:", metrics.box.maps)

#Using Test-Time Augmentation (TTA) to improve performance during prediction:
model.val(augment=True)
