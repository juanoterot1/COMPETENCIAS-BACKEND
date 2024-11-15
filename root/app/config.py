import os
from datetime import timedelta

class Config:
    #DATABASE CONFIGURATION
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT CONFIGURATION
    SECRET_KEY = os.getenv('SECRET_KEY', 'madagascar28!@#2024') 