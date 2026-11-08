import os

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3308"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv(
    "MYSQL_ROOT_PASSWORD", "poll_demo_password"
)
DB_NAME = os.getenv("DB_NAME", "poll_db")