from __future__ import annotations
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
from socket import socket

PADDING = padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None
)


class User:
    def __init__(self, name: str):
        self.name = name
        self.socket = socket()
        self.group = None
        self.admin = False
        self.private_key: rsa.RSAPrivateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key: rsa.RSAPublicKey = self.private_key.public_key()
        self.encrypted_keys = dict()

    def upload_file(self, sock: socket):
        if self.group is None:
            sock.sendall(b"You are not a member of any group.\n")
            return
        sock.sendall(b"Type the full name of the file you wish to upload: ")
        filename = sock.recv(1024).decode('ASCII').strip()
        with open(f"{self.name.lower()}/{filename}", 'rb') as file:
            data = file.read()
            key = Fernet.generate_key()
            encrypted_data = Fernet(key).encrypt(data)
            with open(f"uploaded/encrypted_{filename}", 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

            for username, user in self.group.users.items():
                encrypted_key = user.public_key.encrypt(key, padding=PADDING)
                user.encrypted_keys[filename] = encrypted_key

    def download_file(self, sock: socket):
        if self.group is None:
            sock.sendall(b"You are not a member of any group.\n")
            return

        sock.sendall(b"Type the full name of the file you wish to download: ")
        filename = sock.recv(1024).decode('ASCII').strip()
        with open(f"uploaded/encrypted_{filename}", 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
            encrypted_key = self.encrypted_keys[filename]
            key = self.private_key.decrypt(encrypted_key, padding=PADDING)
            data = Fernet(key).decrypt(encrypted_data)
            with open(f"{self.name.lower()}/{filename}", 'wb') as file:
                file.write(data)

    def ask_for_removal(self, sock: socket):
        if self.admin:
            sock.sendall(b"Which user would you like to remove: ")
            name = sock.recv(1024).decode('ASCII').strip()
            if name in self.group.users:
                self.group.remove_user(self.group.users[name])
            else:
                sock.sendall(b"Unknown user.\n")
        else:
            sock.sendall(b"Insufficient permissions.\n")

    def ask_for_add(self, sock: socket):
        if self.admin:
            sock.sendall(b"Which user would you like to add: ")
            name = sock.recv(1024).decode('ASCII').strip()
            if name in self.group.users:
                self.group.add_user(self.group.users[name])
            else:
                sock.sendall(b"Unknown user.\n")
        else:
            sock.sendall(b"Insufficient permissions.\n")

    def make_admin(self, sock: socket):
        if self.admin:
            sock.sendall(b"Which user would you like to promote: ")
            name = sock.recv(1024).decode('ASCII').strip()
            if name in self.group.group_users:
                self.group.group_users[name].admin = True
            else:
                sock.sendall(b"Unknown user.\n")
        else:
            sock.sendall(b"Insufficient permissions.\n")
