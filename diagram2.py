from __future__ import annotations

import argparse
import os
import chess.pgn as pgn
from graphviz import Graph
import math


class GraphNode:
    """
    Translate PGN nodes to nodes for drawing. Always start with a black move
    """

    white_node: pgn.GameNode  # The white move of the current node
    name: str
    step: int
    child: list[GraphNode]

    def __init__(self, name, step, white_node: pgn.GameNode or None):
        self.white_node = white_node
        self.step = step
        self.name = name
        self.child = []

    def make_tree(self):
        for black_node in self.white_node.variations:  # for every next black move
            black_node_step = math.ceil(black_node.ply() / 2)
            if black_node.is_end():
                child_node = GraphNode(str(black_node_step) + '. ' + black_node.san(), black_node_step, None)
                self.child.append(child_node)
                continue

            for black_node_white in black_node.variations:
                child_node = GraphNode(str(black_node_step) + '. ' + black_node.san() + ' ' + black_node_white.san(),
                                       black_node_step, black_node_white)
                child_node.make_tree()
                self.child.append(child_node)


class DrawGraphviz:
    """
    Draw a tree with Graphviz
    """

    m_start: int
    m_end: int
    dot: Graph

    def __init__(self, save_name, start, end):
        self.args = args
        self.m_end = end
        self.m_start = start

        self.dot = Graph(name='diagram-' + save_name, strict=True)
        self.dot.graph_attr['rankdir'] = 'LR'
        self.dot.node_attr['shape'] = 'box'

    def __draw_func(self, node: GraphNode, parent: GraphNode or None):
        if node.step > self.m_end:
            return

        if node.step >= self.m_start:
            self.dot.node(str(id(node)), node.name)

        if parent is not None and node.step >= self.m_start + 1:
            self.dot.edge(str(id(parent)), str(id(node)))

        for child_node in node.child:
            self.__draw_func(child_node, node)

    def draw(self, root: GraphNode):
        self.__draw_func(root, None)
        self.dot.render(view=True, format='pdf')


if __name__ == '__main__':

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Draw moves from a PGN file')
    parser.add_argument('input', default='', help='Input pgn file')
    parser.add_argument('-s', '--start', type=int, default=1, help='First step (default: 1)')
    parser.add_argument('-e', '--end', type=int, default=10000, help='Last step (default: max)')
    args = parser.parse_args()

    INPUTFILE = args.input
    START = args.start
    END = args.end

    # read game
    input = open(INPUTFILE, encoding="utf-8-sig")
    first_game = pgn.read_game(input)

    # construct a tree from the game
    root = GraphNode('start', 0, first_game)
    root.make_tree()

    # draw tree
    diagram = DrawGraphviz(os.path.splitext(os.path.basename(INPUTFILE))[0], START, END)
    diagram.draw(root)
