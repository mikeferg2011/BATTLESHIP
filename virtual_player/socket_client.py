import socketio
from helpers import setup_ships, rand_space
from time import sleep

server = 'http://127.0.0.1:5000'


class SocketClient:
    def __init__(self, room, username):
        self.room = room
        self.username = username
        self.sio = socketio.Client()
        self.ship_positions = setup_ships()
        self.missiles = []

        self.sio.connect(server)
        self.sio.emit("join", {"room": self.room, "username": self.username})

        sleep(5)

        self.sio.emit(
            "submit_ships",
            {'username': self.username, 'room': self.room, 'shipPositions': self.ship_positions},
            # room=self.room
        )

        @self.sio.on('joined')
        def on_message(data):
            print('I joined!')

        @self.sio.on('return_missile')
        def on_return_missile(data):
            # {"username": username, "loc": missile_result, "phase": new_phase}
            if data["username"] == self.username:
                self.missiles.append(data["loc"])
            elif data['phase']['secondary'] == self.username:
                next_shot = rand_space(self.missiles)
                self.sio.emit(
                    "fire_missile",
                    {"room": self.room, "username": self.username, "loc": next_shot}
                )

    def emit_test(self):
        self.sio.emit("test", {"room": self.room,
                      "message": 'This is a string'})

    def disconnect(self):
        self.sio.disconnect()
