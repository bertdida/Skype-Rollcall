import os
from sqlalchemy import create_engine
from config import config
from skyperollcall import MySkypeEventLoop

if __name__ == "__main__":
    engine = create_engine(config.DATABASE_URI)
    with engine.connect() as conn:
        print("✅ database connection stablished")

        sk = MySkypeEventLoop(config=config, db_conn=conn, autoAck=True)
        sk.loop()

    conn.close()
