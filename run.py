from config import config
from skyperollcall import MySkypeEventLoop

if __name__ == "__main__":
    sk = MySkypeEventLoop(config=config, autoAck=True)
    sk.loop()
