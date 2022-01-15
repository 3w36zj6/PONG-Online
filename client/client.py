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
        App.opponent_bat.y = msg["y"]

    def on_enter_room(self, msg):
        print(f"[{datetime.now().strftime(YMDHMS)}] enter : {msg}")
        App.socketio_client.room_id = msg
        App.game_mode = 2


class SocketIOClient:
    def __init__(self, host, path):
        self.host = host
        self.path = path
        self.client = socketio.Client()
        self.room_id = None

    def connect(self):
        self.client.register_namespace(MyCustomNamespace(self.path))
        self.client.connect(self.host)

    def disconnect(self):
        self.client.disconnect()

    def get_sid(self):
        return self.client.get_sid(namespace=self.path)

    def send_game_status(self, params):
        params["room_id"] = self.room_id
        self.client.emit("send_game_status", params, namespace=self.path)


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
    bat: Bat
    opponent_bat: Bat
    socketio_client = SocketIOClient(host="http://localhost:3000", path="/test")

    def __init__(self):
        pyxel.init(640, 360, title="Hello Pyxel")

        App.game_mode = 0

        App.bat = Bat(x=10, y=0)
        App.opponent_bat = Bat(x=620, y=0)

        pyxel.run(self.update, self.draw)

    def update(self):

        App.bat.update()

        if App.game_mode == 0:  # タイトル
            pass
        elif App.game_mode == 1:  # 待機部屋
            pass
        elif App.game_mode == 2:  # 対戦中
            pass
            if pyxel.frame_count % 6 == 0:
                App.socketio_client.send_game_status({"x": self.bat.x, "y": self.bat.y})
        elif App.game_mode == 3:  # 対戦終了
            pass

        if pyxel.btn(pyxel.KEY_RETURN):
            App.game_mode = 1
            App.socketio_client.connect()

        # exit
        if pyxel.btn(pyxel.KEY_Q):
            App.socketio_client.disconnect()
            sys.exit()

    def draw(self):
        pyxel.cls(0)

        pyxel.text(0, 0, f"{App.socketio_client.get_sid()}", 3)
        pyxel.text(0, 10, f"{pyxel.frame_count}", 3)
        if App.game_mode == 0:  # タイトル
            pass
        elif App.game_mode == 1:  # 待機部屋
            pyxel.text(40, 40, f"waiting room", 7)
        elif App.game_mode == 2:  # 対戦中
            App.opponent_bat.draw()
        elif App.game_mode == 3:  # 対戦終了
            pass
        App.bat.draw()


if __name__ == "__main__":
    App()
