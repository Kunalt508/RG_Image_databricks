# 🕵️ Deepfake / AI Image Detector — Databricks ML Pipeline

## Project Overview
Binary image classification to detect whether an image is **REAL** or **AI-Generated (FAKE)**
using the CIFAKE dataset and a custom CNN trained on Databricks.

## Dataset
- **CIFAKE** — 60,000 REAL + 60,000 FAKE images
- Source: Kaggle (birdy654/cifake-real-and-ai-generated-synthetic-images)

## ML Lifecycle Stages
| Notebook | Stage | Description |
|---|---|---|
| 00_setup.py | Setup | Install libraries |
| 01_data_ingestion.py | Bronze | Load raw images into Delta |
| 02_data_processing.py | Silver | Clean & validate images |
| 03_feature_engineering.py | Gold | Splits & augmentation |
| 04_model_training.py | Training | CNN + MLflow tracking |
| 05_model_registry.py | Registry | Register @champion model |
| 06_batch_inference.py | Inference | Score new images |
| 07_monitoring.py | Monitoring | Drift detection |

## Tech Stack
- Databricks Free Edition (Serverless)
- Delta Lake + Unity Catalog
- PyTorch (LightweightCNN)
- MLflow (Tracking + Registry)
- PySpark

## GPU Upgrade Path
Swap LightweightCNN → EfficientNet-B0 when GPU is attached.