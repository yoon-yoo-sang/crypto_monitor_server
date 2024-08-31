import os

from dotenv import load_dotenv

load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
