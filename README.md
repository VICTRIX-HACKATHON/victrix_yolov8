<div align="center">

# 🚀 SpaceBoot

[![YOLOv8](https://img.shields.io/badge/YOLOv8-vision-success)](https://github.com/ultralytics/ultralytics)
[![Flask](https://img.shields.io/badge/Flask-webapp-blue)](https://flask.palletsprojects.com/)
[![Falcon Dataset](https://img.shields.io/badge/Falcon%20Dataset-space%20vision-purple)](#)

</div>

**SpaceBoot** is an AI-powered object detection system that ensures the presence of essential safety equipment in space stations or simulations. Using YOLOv8 and a Falcon space dataset, it identifies critical gear such as fire extinguishers, toolkits, and oxygen cylinders.


##  Features

-  Pre-trained model on Falcon's Space Station Dataset  
-  Fast inference with YOLOv8 architecture  
-  Web interface built with Flask for quick testing  
-  Simple and intuitive UI to upload or click images  


##  Web App Usage

1. Upload an image of a space station environment *(real or simulated)*  
2. Or test with built-in sample images  
3. The model will automatically detect safety equipment  
4. View detection results with bounding boxes and confidence scores  


##  Model Details

- Trained on the **Falcon Space Station Dataset**  
- Detects:
  - 🔧 Toolkits  
  - 🧯 Fire Extinguishers  
  - 🧪 Oxygen Cylinders  
- Built on **YOLOv8**, optimized for high accuracy and speed  
- Lightweight enough for local deployment or edge testing  


##  Tech Stack

- **YOLOv8** – Object Detection
- **Flask** – Web Interface
- **Falcon Dataset** – Annotated images from space station simulations


## Installation

```bash
git clone https://github.com/your-username/spaceboot.git
cd spaceboot
pip install -r requirements.txt


