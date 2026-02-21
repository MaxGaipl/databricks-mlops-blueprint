# Databricks notebook source
# MAGIC %md
# MAGIC # Exploratory Data Analysis (EDA) Template
# MAGIC 
# MAGIC This notebook serves as a best-practice template for interactive development and EDA. 
# MAGIC It is designed to work seamlessly both directly in the Databricks Workspace UI and locally in your IDE via Databricks Connect.
# MAGIC 
# MAGIC **How it works:**
# MAGIC By explicitly initializing the `SparkSession` and standard Databricks utilities (`dbutils`, `display`), you avoid relying on implicit "magic" variables (`__builtins__`). This makes your notebook standard Python code that your IDE (like VS Code) can understand and lint properly.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Initialization
# MAGIC This block initializes the connection to your Databricks Workspace.
# MAGIC *   **On a Cluster (UI):** It instantly connects to the existing environment.
# MAGIC *   **Locally (IDE):** It spins up a Databricks Connect session using your local configuration.

# COMMAND ----------
import IPython
from databricks.connect import DatabricksSession
from databricks.sdk import WorkspaceClient

# 1. Initialize Spark Session explicitly
spark = DatabricksSession.builder.getOrCreate()

# 2. explicitly initialize dbutils to use widgets, secrets etc.
# Note: databricks.sdk.WorkspaceClient provides the most robust dbutils implementation
dbutils = WorkspaceClient().dbutils

# 3. Explicitly define display for local IDEs (fallback to IPython.display if 'display' is not globally injected by Databricks)
try:
    display = display
except NameError:
    # If we are in an IDE (Databricks Connect), use IPython's display
    def display(df, *args, **kwargs):
        if hasattr(df, "toPandas"):
            IPython.display.display(df.limit(10).toPandas())
        else:
            IPython.display.display(df)

print(f"Connected to Databricks cluster. Spark version: {spark.version}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Data Exploration
# MAGIC Now that the session is initialized, you can query your Unity Catalog just like you would in a standard Databricks context.

# COMMAND ----------
# Example: Querying a sample dataset (replace with your catalog.schema.table)
# df = spark.table("samples.nyctaxi.trips")
# display(df)

# Example: Using dbutils to interact with DBFS or Volumes
# files = dbutils.fs.ls("/")
# display(files)

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Prototyping Business Logic
# MAGIC You can import the functions you are writing in the `src/` directory to test them interactively before committing.
# MAGIC 
# MAGIC *Note: If you change the code in `src/`, you may need to use `%autoreload` or restart the Python kernel in your IDE to pick up the changes.*

# COMMAND ----------
import sys
import os

# Ensure the src directory is in the Python path so we can import our modules
# Assuming this notebook is in the 'notebooks' folder at the repository root
repo_root = os.path.abspath(os.path.join(os.getcwd(), ".."))
if repo_root not in sys.path:
    sys.path.append(repo_root)

# Now you can import your custom functions
# from src.feature_engineering.compute_features import compute_features

# df_transformed = compute_features(df, spark=spark)
# display(df_transformed)
