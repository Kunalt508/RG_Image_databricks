# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 1: Install Libraries

# COMMAND ----------
%pip install kaggle torch torchvision pillow mlflow scikit-learn

# COMMAND ----------
dbutils.library.restartPython()

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 2: Download CIFAKE Dataset

# COMMAND ----------
import os
os.environ["KAGGLE_CONFIG_DIR"] = "/Volumes/main/default/files/"
os.system("kaggle datasets download -d birdy654/cifake-real-and-ai-generated-synthetic-images \
           -p /Volumes/main/default/raw_images/ --unzip")
print("✅ Dataset downloaded!")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 3: Create Bronze Delta Table

# COMMAND ----------
from pyspark.sql import Row

image_records = []
for label_name, label_val in [("REAL", 1), ("FAKE", 0)]:
    folder = f"/Volumes/main/default/raw_images/train/{label_name}"
    for fname in os.listdir(folder):
        if fname.endswith((".jpg", ".png")):
            image_records.append(Row(
                file_path=f"{folder}/{fname}",
                label=label_val,
                label_name=label_name,
                split="train"
            ))

bronze_df = spark.createDataFrame(image_records)
bronze_df.write.format("delta").mode("overwrite") \
    .saveAsTable("main.default.bronze_image_metadata")
print(f"✅ Bronze table: {bronze_df.count()} records")