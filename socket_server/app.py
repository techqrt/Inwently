from flask import Flask, request
import threading

from socket_server.socket_app import SocketApp, socket_clients

app = Flask(__name__)


@app.route('/socket_response', methods=['POST'])
def socket_response():
    print(request.get_json())
    address = request.get_json()['address']
    message = request.get_json()['message']
    address = tuple(address)
    client_socket = socket_clients[str(address)]
    try:
        client_socket.sendall(message.encode('utf-8'))
        print(f"[DATA SENT] Sent '{message}' to {address}, {client_socket}")
        return "data sent successfully"
    except Exception as e:
        print(f"[ERROR] Unable to send data to {address}. Error: {str(e)}, {client_socket}")
        return "error occurred"


@app.route('/socket_disconnect', methods=['POST'])
def socket_disconnect():
    try:
        address = request.get_json()['address']
        address = tuple(address)
        client_socket = socket_clients[str(address)]
        client_socket.close()
        del socket_clients[str(address)]
        return f"socket disconnected for {address}"
    except:
        return f"failed to disconnect socket for {address}"


def main():
    global app
    app = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0'})
    socket_app = threading.Thread(target=SocketApp().start_server)
    app.start()
    socket_app.start()
