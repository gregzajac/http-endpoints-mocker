"""Configuration settings."""

import os

from dotenv import load_dotenv


load_dotenv()


class _Settings:
    PROJECT_NAME = "HTTP endpoints mocker"
    PROJECT_VERSION = os.getenv("PROJECT_VERSION")


settings = _Settings()
