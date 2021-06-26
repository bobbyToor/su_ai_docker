import os
from milvus import MetricType

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")

MILVUS_HOST = os.getenv("MILVUS_HOST", "127.0.0.1")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
VECTOR_DIMENSION = int(os.getenv("VECTOR_DIMENSION", 768))
METRIC_TYPE = MetricType.L2
TOP_K = int(os.getenv("TOP_K", 7))
L2_DISTANCE_THRESHOLD = int(os.getenv("L2_DISTANCE_THRESHOLD", 7))

MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION", "ideas")

MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB = os.getenv("MYSQL_DB", "sucity")
MYSQL_TABLE = os.getenv("MYSQL_TABLE", "embeddings")

FIRESTORE_USERS_COLLECTION = os.getenv("FIRESTORE_USERS_COLLECTION", "users")
FIRESTORE_IDEAS_COLLECTION = os.getenv("FIRESTORE_IDEAS_COLLECTION", "ideas")
