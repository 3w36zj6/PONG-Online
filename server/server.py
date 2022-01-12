import eventlet
import socketio
from datetime import datetime

YMDHMS = "%Y-%m-%d %H:%M:%S"


class MyCustomNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print(f"[{datetime.now().strftime(YMDHMS)}] connect sid : {sid}")
        print(f"[{datetime.now().strftime(YMDHMS)}] connect env : {environ}")

    def on_sid_message(self, sid, msg):  # 送信してきたクライアントだけにメッセージを送る
        self.emit("response", msg, room=sid)
        print(f"[{datetime.now().strftime(YMDHMS)}] emit sid : {msg}")

    def on_broadcast_message(self, sid, msg):  # 接続しているすべてのクライアントにメッセージを送る
        self.emit("response", msg)
        print(f"[{datetime.now().strftime(YMDHMS)}] emit all : {msg}")

    def on_disconnect(self, sid):
        print(f"[{datetime.now().strftime(YMDHMS)}] disconnect sid : {sid}")


if __name__ == "__main__":
    server = socketio.Server(cors_allowed_origins="*")
    server.register_namespace(MyCustomNamespace("/test"))
    app = socketio.WSGIApp(server)
    eventlet.wsgi.server(eventlet.listen(("localhost", 3000)), app)
