import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # 👈 esto es clave

def get_engine():
    return create_engine(
        f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}",
        pool_pre_ping=True
    )