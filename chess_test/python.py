import tkinter as tk
from tkinter import messagebox
import socket
import threading
import sys
import chess
from PIL import Image, ImageTk

HOST = ''  # Empty for server bind
PORT = 5000
BUFFER_SIZE = 1024

class ChessNetwork:
    def __init__(self, is_server, host, port):
        self.is_server = is_server
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None

    def start(self):
        if self.is_server:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            print(f"Waiting for connection on {self.host}:{self.port}...")
            self.conn, self.addr = self.sock.accept()
            print(f"Connected by {self.addr}")
        else:
            self.sock.connect((self.host, self.port))
            self.conn = self.sock
            print(f"Connected to server {self.host}:{self.port}")

    def send(self, data):
        self.conn.sendall(data.encode())

    def receive(self):
        return self.conn.recv(BUFFER_SIZE).decode()

    def close(self):
        self.conn.close()
        if self.is_server:
            self.sock.close()

class ChessGUI:
    def __init__(self, root, network):
        self.root = root
        self.net = network
        self.board = chess.Board()
        self.size = 64
        self.selected = None
        self.images = {}
        self.turn = chess.WHITE

        self.canvas = tk.Canvas(root, width=8*self.size, height=8*self.size)
        self.canvas.pack()
        self.draw_board()
        self.canvas.bind('<Button-1>', self.click)

        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def draw_board(self):
        self.canvas.delete('all')
        for row in range(8):
            for col in range(8):
                color = '#EEEED2' if (row+col)%2==0 else '#769656'
                x1, y1 = col*self.size, row*self.size
                x2, y2 = x1+self.size, y1+self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                square = chess.square(col, 7-row)
                piece = self.board.piece_at(square)
                if piece:
                    self.draw_piece(piece.symbol(), x1, y1)

    def draw_piece(self, symbol, x, y):
        # Always use the white-piece image (uppercase filename)
        key = symbol.upper()
        if key not in self.images:
            img = Image.open(f"assets/{key}.png")
            img = img.resize((self.size, self.size), Image.ANTIALIAS)
            self.images[key] = ImageTk.PhotoImage(img)
        # Draw the piece image
        self.canvas.create_image(x, y, anchor='nw', image=self.images[key])
        # If it's a black piece, overlay a small filled circle to indicate color
        if symbol.islower():
            pad = self.size * 0.2
            x_center = x + self.size / 2
            y_center = y + self.size / 2
            radius = (self.size / 2) - pad
            self.canvas.create_oval(
                x_center - radius,
                y_center - radius,
                x_center + radius,
                y_center + radius,
                fill='black'
            )

    def click(self, event):
        col = event.x // self.size
        row = event.y // self.size
        sq = chess.square(col, 7-row)
        if self.selected is None:
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.turn:
                self.selected = sq
                self.highlight(col, row)
        else:
            move = chess.Move(self.selected, sq)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.net.send(move.uci())
                self.turn = not self.turn
                self.selected = None
                self.draw_board()
                if self.board.is_game_over():
                    messagebox.showinfo("Game Over", str(self.board.result()))
            else:
                self.selected = None
                self.draw_board()

    def highlight(self, col, row):
        x1, y1 = col*self.size, row*self.size
        x2, y2 = x1+self.size, y1+self.size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=3)

    def listen_thread(self):
        while True:
            try:
                data = self.net.receive()
                if not data:
                    break
                move = chess.Move.from_uci(data)
                self.board.push(move)
                self.turn = not self.turn
                self.draw_board()
                if self.board.is_game_over():
                    messagebox.showinfo("Game Over", str(self.board.result()))
                    break
            except Exception as e:
                print(f"Error: {e}")
                break
        self.net.close()
        self.root.quit()

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('server','client'):
        print("Usage: python chess_network.py [server|client] [host (client)]")
        sys.exit(1)
    is_server = sys.argv[1] == 'server'
    host = HOST if is_server else sys.argv[2]
    network = ChessNetwork(is_server, host, PORT)
    network.start()

    root = tk.Tk()
    root.title("Networked Chess")
    ChessGUI(root, network)
    root.mainloop()
