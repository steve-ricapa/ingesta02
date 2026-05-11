import boto3
import pandas as pd
import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

# =========================
# CARGAR VARIABLES .ENV
# =========================

load_dotenv()

# =========================
# MYSQL
# =========================

usuario = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
puerto = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DATABASE")
tabla = os.getenv("MYSQL_TABLE")

# =========================
# AWS
# =========================

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
aws_region = os.getenv("AWS_REGION")

bucket_name = os.getenv("S3_BUCKET")

# =========================
# CSV
# =========================

archivo_csv = os.getenv("CSV_FILE")

# =========================
# CONEXION MYSQL
# =========================

conexion = create_engine(
    f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{database}"
)

# =========================
# LEER DATOS MYSQL
# =========================

query = f"SELECT * FROM {tabla}"

df = pd.read_sql(query, conexion)

# =========================
# CREAR CSV
# =========================

df.to_csv(archivo_csv, index=False)

print("CSV generado correctamente")

# =========================
# CONEXION S3
# =========================

s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    aws_session_token=aws_session_token,
    region_name=aws_region
)

# =========================
# SUBIR ARCHIVO A S3
# =========================

s3.upload_file(
    archivo_csv,
    bucket_name,
    archivo_csv
)

print("Archivo subido a S3")
print("Ingesta completada")