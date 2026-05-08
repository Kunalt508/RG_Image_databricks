# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # 00 — Setup
# MAGIC Install all required libraries for the Deepfake Detector pipeline.

# COMMAND ----------

%pip install torch torchvision pillow mlflow scikit-learn \
             matplotlib seaborn opencv-python-headless kaggle

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

# Verify all installs
import torch
import torchvision
import mlflow
import sklearn
import cv2
import PIL

print(f"✅ PyTorch:     {torch.__version__}")
print(f"✅ Torchvision: {torchvision.__version__}")
print(f"✅ MLflow:      {mlflow.__version__}")
print(f"✅ Sklearn:     {sklearn.__version__}")
print(f"✅ OpenCV:      {cv2.__version__}")
print(f"✅ Pillow:      {PIL.__version__}")
print("\n🚀 All libraries ready!")