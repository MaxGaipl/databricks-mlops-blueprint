# Databricks notebook source

# MAGIC %md
# MAGIC # Test Notebook
# MAGIC 
# MAGIC This notebook is used to test the Databricks notebook source functionality.

# COMMAND ----------
sales_customers = spark.table("samples.bakehouse.sales_customers")

display(sales_customers.limit(10))
# COMMAND ----------
