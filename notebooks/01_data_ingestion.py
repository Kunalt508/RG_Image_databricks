# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # 01 — Data Ingestion (Bronze Layer)
# MAGIC Download CIFAKE dataset from Kaggle and create Bronze Delta table.

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 1: Upload Kaggle Credentials
# MAGIC Before running this notebook:
# MAGIC 1. Go to kaggle.com → Your Profile → Settings → API → Create New Token
# MAGIC 2. It downloads `kaggle.json`
# MAGIC 3. Upload it to Databricks: Catalog → Volumes → main → default → files

# COMMAND ----------

import os

# Point to kaggle credentials in UC Volume
os.environ["KAGGLE_CONFIG_DIR"] = "/Volumes/workspace/default/kaggle/kaggle.json"

# Download CIFAKE dataset
os.system("""
    kaggle datasets download \
    -d birdy654/cifake-real-and-ai-generated-synthetic-images \
    -p /Volumes/workspace/default/kaggle/raw_images/ \
    --unzip
""")

print("✅ Dataset downloaded!")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 2: Verify Downloaded Files

# COMMAND ----------

import os

base_path = "/Volumes/workspace/default/kaggle/raw_images"

for split in ["train", "test"]:
    for label in ["REAL", "FAKE"]:
        folder = f"{base_path}/{split}/{label}"
        count = len(os.listdir(folder))
        print(f"{split}/{label}: {count} images")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 3: Create Bronze Delta Table (metadata only)

# COMMAND ----------

from pyspark.sql import Row
from pyspark.sql import functions as F

base_path = "/Volumes/workspace/default/kaggle/raw_images"
image_records = []

for split in ["train", "test"]:
    for label_name, label_val in [("REAL", 1), ("FAKE", 0)]:
        folder = f"{base_path}/{split}/{label_name}"
        for fname in os.listdir(folder):
            if fname.endswith((".jpg", ".png", ".jpeg")):
                image_records.append(Row(
                    file_path=f"{folder}/{fname}",
                    file_name=fname,
                    label=label_val,
                    label_name=label_name,
                    split=split,
                    source="CIFAKE"
                ))

bronze_df = spark.createDataFrame(image_records)

bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("main.default.bronze_image_metadata")

print(f"✅ Bronze table created!")
print(f"Total records: {bronze_df.count()}")
bronze_df.groupBy("split", "label_name").count().orderBy("split").show()