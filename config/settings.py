from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    APP_NAME = "VITA 3.0"

    VERSION = "3.0"

    GEMINI_MODEL = "gemini-2.5-pro"

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    DEBUG = True


settings = Settings()
