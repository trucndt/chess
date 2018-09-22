import chess.pgn as pgn
from graphviz import Graph

START = 3
END = 18
INPUTFILE = "Nimzo 4 Bg5.pgn"
input = open(INPUTFILE, encoding="utf-8-sig")

diagram = [[]]
for i in range(100):
    diagram.append([])

for count in range(10):
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
    diagram.append(token[START:END+1])

diagram = [x for x in diagram if x]
print(diagram)

dot = Graph(strict=True)
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'box'

draw = []
for i in range(len(diagram[0])):
    draw.append([diagram[0][i]])

dot.node('00', draw[0][0])
for i in range(1, len(draw)):
    dot.node(str(i) + '0', draw[i][0])
    dot.edge(str(i - 1) + '0', str(i) + '0')

for i in range(len(diagram)):
    state = 0
    if diagram[i][0] != draw[0][len(draw[0]) - 1]:
        draw[0].append(diagram[i][0])
        dot.node('0' + str(len(draw[0]) - 1), draw[0][len(draw[0]) - 1])
        state = 1
    for j in range(1, len(diagram[i])):
        if state == 1:
            draw[j].append(diagram[i][j])
            dot.node(str(j) + str(len(draw[j]) - 1), draw[j][len(draw[j]) - 1])
            dot.edge(str(j - 1) + str(len(draw[j - 1]) - 1), str(j) + str(len(draw[j]) - 1))
        else:
            if diagram[i][j] != draw[j][len(draw[j]) - 1]:
                state = 1
                draw[j].append(diagram[i][j])
                dot.node(str(j) + str(len(draw[j]) - 1), draw[j][len(draw[j]) - 1])
                dot.edge(str(j - 1) + str(len(draw[j - 1]) - 1), str(j) + str(len(draw[j]) - 1))
                # prev = max(loc for loc, val in enumerate(draw[j - 1]) if val == diagram[i][j - 1])
                # dot.edge(str(j - 1) + str(prev), str(j) + str(len(draw[j]) - 1))

print(draw)

dot.render('round-table.png', view=True)
print(dot.source)

