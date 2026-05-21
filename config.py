import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me")
