from user import User
from secure_group import SecureCloudStorageGroup
from socket import socket
import threading


def start():
    alice.socket.bind(('localhost', 2222))
    alice.socket.listen(1)
    bob.socket.bind(('localhost', 3333))
    bob.socket.listen(1)
    chris.socket.bind(('localhost', 4444))
    chris.socket.listen(1)
    tom.socket.bind(('localhost', 5555))
    tom.socket.listen(1)
    while True:
        alice_input, _ = alice.socket.accept()
        threading.Thread(target=handler, args=(alice, alice_input)).start()
        bob_input, _ = bob.socket.accept()
        threading.Thread(target=handler, args=(bob, bob_input)).start()
        chris_input, _ = chris.socket.accept()
        threading.Thread(target=handler, args=(chris, chris_input)).start()
        tom_input, _ = tom.socket.accept()
        threading.Thread(target=handler, args=(tom, tom_input)).start()


def handler(user: User, sock: socket):
    sock.sendall(b'Type help for a list of available commands.\n')
    while True:
        sock.sendall('> '.encode())
        command = sock.recv(1024).decode('ASCII').strip()
        if command == 'help':
            sock.sendall(b'add | remove | admin | upload | download\n')
        elif command == 'add':
            user.ask_for_add(sock)
        elif command == 'remove':
            user.ask_for_removal(sock)
        elif command == 'admin':
            user.make_admin(sock)
        elif command == 'upload':
            user.upload_file(sock)
        else:
            user.download_file(sock)


if __name__ == '__main__':
    alice = User('Alice')
    bob = User('Bob')
    chris = User('Chris')
    tom = User('Tom')
    group = SecureCloudStorageGroup()
    group.users = {
        'Alice': alice,
        'Bob': bob,
        'Chris': chris,
        'Tom': tom
    }
    group.add_user(alice, admin=True)  # Let's suppose Alice created the group
    start()
