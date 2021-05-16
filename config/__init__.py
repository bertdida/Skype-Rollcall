import os


class Config:
    DATABASE_URL = os.environ["DATABASE_URL"]
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    USERNAME = os.environ["SKYPE_USERNAME"]
    PASSWORD = os.environ["SKYPE_PASSWORD"]
    COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", "!")


class Development(Config):
    ENV = "dev"


class Production(Config):
    ENV = "prod"


env = os.environ.get("ENV", "dev")
config = Production if env == "prod" else Development
