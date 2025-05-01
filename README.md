# Networked Chess

A simple networked chess application built in Python using Tkinter for the GUI and sockets for peer-to-peer communication. One player runs in **server** mode (white), the other in **client** mode (black). Chess logic and move validation are handled by the `python-chess` library.

---

## Features

- 8×8 chess board rendered with Tkinter
- Move legality enforced via `python-chess`
- Peer-to-peer networking over TCP sockets
- White-piece PNG images, with black pieces indicated by overlayed circle
- Game-over detection (checkmate, stalemate, draws)

---

## Requirements

- Python 3.7 or higher
- [python-chess](https://pypi.org/project/python-chess/)
- [Pillow](https://pypi.org/project/Pillow/)

Install dependencies with:

```bash
pip install python-chess Pillow
```

---

## Repository Structure

```
networked-chess/
├── chess_network.py       # Main game script
├── assets/                # Image assets for white pieces
│   ├── P.png              # White pawn
│   ├── N.png              # White knight
│   ├── B.png              # White bishop
│   ├── R.png              # White rook
│   ├── Q.png              # White queen
│   └── K.png              # White king
└── README.md
```

---

## How to Play

1. **Prepare assets**: Ensure the `assets` folder contains the six white-piece PNGs named exactly `P.png`, `N.png`, `B.png`, `R.png`, `Q.png`, and `K.png`.
2. **Start the server (White side)**:
   ```bash
   python chess_network.py server
   ```
3. **Connect as client (Black side)** on a second machine or terminal:
   ```bash
   python chess_network.py client <server_ip>
   ```
   Replace `<server_ip>` with the server’s IP address (or `localhost` if on the same machine).
4. **Make moves**:
   - Click on a piece to select it (highlight appears).
   - Click on the destination square.
   - Black pieces are drawn using the white-piece image plus a black circle overlay.
5. **Game end**: A message box will pop up showing the result (e.g. `1-0` for White win, `0-1` for Black win, or `1/2-1/2` for draw).

---

## Customization

- **Circle size/color**: Edit the padding (`pad`) or `fill` in the `draw_piece` method to change the black-piece indicator.
- **Board colors**: Change the hex values `#EEEED2` (light squares) and `#769656` (dark squares) in `draw_board`.
- **Port number**: Modify the `PORT` constant at the top of `chess_network.py`.

---

## Troubleshooting

- **Connection refused**: Verify firewall settings and that the server is running and listening on the specified port.
- **Missing images**: Ensure `assets/` contains all six PNGs with correct names.
- **Invalid moves**: Only legal chess moves are accepted.

---

## License

This project is released under the MIT License.

