import os
import config
from skyperollcall import MySkypeEventLoop

env = os.environ.get("ENV", "dev")
config_class = "Production" if env == "prod" else "Development"

if __name__ == "__main__":
    app_config = getattr(config, config_class)
    sk = MySkypeEventLoop(config=app_config, autoAck=True)
    sk.loop()
