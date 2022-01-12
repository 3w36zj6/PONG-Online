import socketio
import time
import sys
import pyxel
from datetime import datetime

YMDHMS = "%Y-%m-%d %H:%M:%S"


class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print(f"[{datetime.now().strftime(YMDHMS)}] connect")

    def on_disconnect(self):
        print(f"[{datetime.now().strftime(YMDHMS)}] disconnect")

    def on_response(self, msg):
        print(f"[{datetime.now().strftime(YMDHMS)}] response : {msg}")

    def on_enter_room(self, msg):
        print(f"[{datetime.now().strftime(YMDHMS)}] enter : {msg}")
        App.game_mode = 2


class SocketIOClient:
    def __init__(self, host, path):
        self.host = host
        self.path = path
        self.client = socketio.Client()
        self.connect()

    def connect(self):
        self.client.register_namespace(MyCustomNamespace(self.path))
        self.client.connect(self.host)

    def disconnect(self):
        self.client.disconnect()

    def get_sid(self):
        return self.client.get_sid(namespace=self.path)

    def test(self, message):
        self.client.emit("broadcast_message", message, namespace=self.path)


class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.y = max(self.y - 10, 0)

        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(self.y + 10, 360 - 100)

    def draw(self):
        pyxel.rect(self.x, self.y, 10, 100, 7)


class App:
    game_mode: int = 0

    def __init__(self, host):
        pyxel.init(640, 360, title="Hello Pyxel")

        App.game_mode = 1

        self.socketio_client = SocketIOClient(host=host, path="/test")

        self.bat = Bat(x=10, y=10)

        pyxel.run(self.update, self.draw)

    def update(self):

        self.bat.update()

        if App.game_mode == 0:  # タイトル
            pass
        elif App.game_mode == 1:  # 待機部屋
            pass
        elif App.game_mode == 2:  # 対戦中
            pass
        elif App.game_mode == 3:  # 対戦終了
            pass

        # self.socketio_client.test({"x": self.bat.x, "y": self.bat.y})

        # exit
        if pyxel.btn(pyxel.KEY_Q):
            self.socketio_client.disconnect()
            sys.exit()

    def draw(self):
        pyxel.cls(0)

        pyxel.text(0, 0, f"{self.socketio_client.get_sid()}", 3)
        if App.game_mode == 0:  # タイトル
            pass
        elif App.game_mode == 1:  # 待機部屋
            pyxel.text(40, 40, f"waiting room", 7)
        elif App.game_mode == 2:  # 対戦中
            pass
        elif App.game_mode == 3:  # 対戦終了
            pass
        self.bat.draw()


if __name__ == "__main__":
    App(host="http://localhost:3000")
