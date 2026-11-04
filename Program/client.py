import socket 
import threading 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, 
modes 
from cryptography.hazmat.backends import default_backend 
import tkinter as tk 
from tkinter import scrolledtext 
 
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
 
class ChatClient: 
    def __init__(self, master): 
        self.master = master 
        self.master.title("Chat Client") 
 
        self.text_area = scrolledtext.ScrolledText(self.master) 
        self.text_area.pack(padx=10, pady=10) 
 
        self.entry = tk.Entry(self.master) 
        self.entry.pack(fill=tk.BOTH, padx=10, pady=10) 
        self.entry.bind("<Return>", self.send_message) 
 
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.client.connect(("172.168.10.1", 8888))  # Ganti port ke 8888 
         
        threading.Thread(target=self.receive_messages).start() 
 
 
 
 
    def send_message(self, event): 
        message = self.entry.get() 
        encrypted_message = encrypt_message(message) 
        self.client.send(encrypted_message) 
        self.text_area.insert(tk.END, f"You: {message}\n") 
        self.entry.delete(0, tk.END) 
 
    def receive_messages(self): 
        while True: 
            try: 
                response = self.client.recv(1024) 
                if not response: 
                    break 
                decrypted_response = decrypt_message(response) 
                self.text_area.insert(tk.END, f"{decrypted_response}\n") 
            except Exception as e: 
                self.text_area.insert(tk.END, f"Error: {e}\n") 
                break 
 
if __name__ == "__main__": 
    root = tk.Tk() 
    app = ChatClient(ro
