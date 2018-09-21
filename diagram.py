import chess.pgn as pgn

START = 3
END = 8
INPUTFILE = "Nimzo 4 Bg5.pgn"
input = open(INPUTFILE, encoding="utf-8-sig")

diagram = [[]]
for i in range(100):
    diagram.append([])

for count in range(3):
    first_game = pgn.read_game(input)

    board = first_game.board()
    moves = board.variation_san(first_game.main_line())

    token = moves.split(".")[1:]
    for i in range(START, len(token)):
        if i == END + 1:
            break
        if i != len(token) - 1:
            token[i] = token[i][1:token[i].rfind(" ")]
        if i == END or i == len(token) - 1:
            token[i] += " " + first_game.headers["White"]
        # if len(diagram[i]) != 1 or token[i] != diagram[i][len(diagram[i]) - 1]:
        # diagram[i].append(token[i])
    diagram.append(token[START:END+1])

diagram = [x for x in diagram if x]
print(diagram)

