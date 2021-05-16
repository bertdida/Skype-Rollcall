from skyperollcall import MySkypeEventLoop

if __name__ == "__main__":
    sk = MySkypeEventLoop(autoAck=True)
    sk.loop()
