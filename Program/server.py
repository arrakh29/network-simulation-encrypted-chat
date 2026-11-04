import socket 
import threading 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, 
modes 
from cryptography.hazmat.backends import default_backend 
 
# Kunci enkripsi dan IV (Initialization Vector) harus disepakati 
sebelumnya 
key = b'0123456789abcdef' 
iv = b'1234567890abcdef' 
 
def encrypt_message(message): 
    backend = default_backend() 
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend) 
    encryptor = cipher.encryptor() 
    ct = encryptor.update(message.encode()) + encryptor.finalize() 
    return ct 
 
def decrypt_message(ciphertext): 
    backend = default_backend() 
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend) 
    decryptor = cipher.decryptor() 
 
 
 
    decrypted_message = decryptor.update(ciphertext) + 
decryptor.finalize() 
    return decrypted_message.decode() 
 
def handle_client(client_socket, address): 
    print(f"[NEW CONNECTION] {address} connected.") 
 
    while True: 
        try: 
            encrypted_message = client_socket.recv(1024) 
            if not encrypted_message: 
                print(f"[DISCONNECTED] {address} disconnected.") 
                break 
             
            decrypted_message = decrypt_message(encrypted_message) 
            print(f"[{address}] {decrypted_message}") 
             
            # Echo the decrypted message back to the client 
            client_socket.send(encrypted_message) 
         
        except Exception as e: 
            print(f"[ERROR] {address}: {e}") 
            break 
     
    client_socket.close() 
 
def start_server(): 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind(("172.168.10.1", 8888))  # Ganti IP dan port sesuai 
kebutuhan 
    server.listen(5) 
    print("[LISTENING] Server is listening on 172.168.10.1:8888") 
 
    while True: 
        client_socket, address = server.accept() 
        thread = threading.Thread(target=handle_client, 
args=(client_socket, address)) 
        thread.start() 
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}") 
 
if __name__ == "__main__": 
    start_server() 
