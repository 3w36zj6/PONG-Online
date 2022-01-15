import eventlet
import socketio
from datetime import datetime

YMDHMS = "%Y-%m-%d %H:%M:%S"


class Player:
    players: list["Player"] = []

    @classmethod
    def setup(cls):
        cls.players = []

    @classmethod
    def append(cls, sid):  # 待機室に追加
        cls.players.append(sid)


class MyCustomNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print(f"[{datetime.now().strftime(YMDHMS)}] connect sid : {sid}")
        print(f"[{datetime.now().strftime(YMDHMS)}] connect env : {environ}")

        if not Player.players:
            Player.append(sid)
        else:
            sid2 = Player.players.pop()
            self.enter_room(sid, sid + sid2)
            self.enter_room(sid2, sid + sid2)
            self.emit("enter_room", sid + sid2, room=sid + sid2)

    def on_sid_message(self, sid, msg):  # 送信してきたクライアントだけにメッセージを送る
        self.emit("response", msg, room=sid)
        print(f"[{datetime.now().strftime(YMDHMS)}] emit sid : {msg}")

    def on_broadcast_message(self, sid, msg):  # 接続しているすべてのクライアントにメッセージを送る
        self.emit("response", msg)
        print(f"[{datetime.now().strftime(YMDHMS)}] emit all : {msg}")

    def on_send_game_status(self, sid, params):
        self.emit("response", params, room=params["room_id"], skip_sid=sid)
        print(f"[{datetime.now().strftime(YMDHMS)}] game status : {params}")

    def on_disconnect(self, sid):
        print(f"[{datetime.now().strftime(YMDHMS)}] disconnect sid : {sid}")

        if sid in Player.players:
            Player.players.remove(sid)


if __name__ == "__main__":
    Player.setup()

    server = socketio.Server(cors_allowed_origins="*")
    server.register_namespace(MyCustomNamespace("/test"))
    app = socketio.WSGIApp(server)
    eventlet.wsgi.server(eventlet.listen(("localhost", 3000)), app)
