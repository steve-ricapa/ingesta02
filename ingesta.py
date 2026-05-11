import boto3
import pandas as pd
from sqlalchemy import create_engine

# =========================
# CONFIGURACION MYSQL
# =========================

usuario = "root"
password = "123456"
host = "host.docker.internal"
puerto = "3306"
database = "empresa"

tabla = "clientes"

# =========================
# CONFIGURACION S3
# =========================

ficheroUpload = "data.csv"
nombreBucket = "gcr-output-01"

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
# GENERAR CSV
# =========================

df.to_csv(ficheroUpload, index=False)

print("CSV generado correctamente")

# =========================
# SUBIR CSV A S3
# =========================

s3 = boto3.client('s3')

response = s3.upload_file(
    ficheroUpload,
    nombreBucket,
    ficheroUpload
)

print("Archivo subido a S3")

print("Ingesta completada")
