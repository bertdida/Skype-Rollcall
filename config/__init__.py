import os


class Config:
    DATABASE_URI = os.environ["DATABASE_URI"]
    USERNAME = os.environ["SKYPE_USERNAME"]
    PASSWORD = os.environ["SKYPE_PASSWORD"]
    GROUP_IDS = (
        os.environ["SKYPE_GROUP_IDS"].split(",")
        if os.environ.get("SKYPE_GROUP_IDS")
        else []
    )

    COMMAND_PREFIX = os.environ.get("COMMAND_PREFIX", "!")


class Development(Config):
    ENV = "dev"
    GROUP_IDS = []


class Production(Config):
    ENV = "prod"


env = os.environ.get("ENV", "dev")
config = Production if env == "prod" else Development