import argparse
import os
import chess.pgn as pgn
from graphviz import Graph

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Draw moves from a PGN file')
parser.add_argument('input', default='', help='Input pgn file')
parser.add_argument('-s', '--start', type=int, default=4, help='First step (default: 4)')
parser.add_argument('-e', '--end', type=int, default=18, help='Last step (default: 18)')
args = parser.parse_args()

INPUTFILE = args.input
START = args.start
END = args.end

input = open(INPUTFILE, encoding="utf-8-sig")

diagram = []

# Read all games to diagram
# diagram[i][j]: game i, step j
while True:
    first_game = pgn.read_game(input)
    if not first_game:
        break
    board = first_game.board()
    moves = board.variation_san(first_game.mainline_moves())

    token = moves.split(".")[1:]
    # print(token)
    for i in range(0, len(token)):
        if i == END:
            break
        if i != len(token) - 1:
            token[i] = token[i][1:token[i].rfind(" ")]
            token[i] = str(i + 1) + ". " + token[i]
        if i == END - 1 or i == len(token) - 1:  # if last one then append name
            result = ""
            if first_game.headers["Result"][:2] == "1/":
                result = "(1/2)"
            else:
                result = '(' + first_game.headers["Result"] + ')'
            token[i] += " " + result + " " + first_game.headers["White"].split(',')[0] + " vs " + first_game.headers["Black"].split(',')[0]
    diagram.append(token[START - 1:END])

diagram = [x for x in diagram if x]
# print(diagram)

# Initiate graph
dot = Graph(name='diagram-' + os.path.splitext(os.path.basename(INPUTFILE))[0], strict=True)
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'box'

# Draw first game
dot.node('00', diagram[0][0])
for i in range(1, len(diagram[0])):
    dot.node('0' + str(i), diagram[0][i])
    dot.edge('0' + str(i - 1), '0' + str(i))

for i in range(1, len(diagram)):
    longMatch = -1
    longMatchGame = -1
    longMatchStep = -1
    for game in range(0, i):  # Find longest match of moves from previous games
        cnt = -1
        step = 0
        for j in range(len(diagram[game])):
            if diagram[i][j] == diagram[game][j]:
                cnt += 1
                step = j
            else:
                break
        if cnt > longMatch:
            longMatch = cnt + 1
            longMatchGame = game
            longMatchStep = step

    if longMatch == -1: # If no match then draw all
        dot.node(str(i) + '0', diagram[i][0])
        for j in range(1, len(diagram[i])):
            dot.node(str(i) + str(j), diagram[i][j])
            dot.edge(str(i) + str(j - 1), str(i) + str(j))
    elif longMatch == len(diagram[i]):
        continue
    else:  # draw only from longMatchStep + 1
        dot.node(str(i) + str(longMatchStep + 1), diagram[i][longMatchStep + 1])
        dot.edge(str(longMatchGame) + str(longMatchStep), str(i) + str(longMatchStep + 1))  # connect to previous game
        for j in range(longMatchStep + 2, len(diagram[i])):
            dot.node(str(i) + str(j), diagram[i][j])
            dot.edge(str(i) + str(j - 1), str(i) + str(j))

dot.render(view=True, format='pdf')
print(dot.source)

