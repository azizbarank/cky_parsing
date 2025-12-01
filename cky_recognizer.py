"""CKY algorithm for sentence recognition with backpointers."""

from nltk.grammar import CFG
from nltk.tree import Tree


def cky_parse(grammar: CFG, sentence: list[str]):
    """Parse a sentence and return the CKY table with backpointers."""
    n = len(sentence)
    if n == 0:
        return None

    terminal_rules = {}
    binary_rules = {}

    for production in grammar.productions():
        rhs = production.rhs()
        lhs = production.lhs()

        if len(rhs) == 1 and isinstance(rhs[0], str):
            word = rhs[0]
            if word not in terminal_rules:
                terminal_rules[word] = []
            terminal_rules[word].append(production)
        elif len(rhs) == 2:
            pair = (rhs[0], rhs[1])
            if pair not in binary_rules:
                binary_rules[pair] = []
            binary_rules[pair].append(production)

    table = [[{} for _ in range(n)] for _ in range(n)]

    for i in range(n):
        word = sentence[i]
        if word in terminal_rules:
            for production in terminal_rules[word]:
                lhs = production.lhs()
                if lhs not in table[i][i]:
                    table[i][i][lhs] = []
                table[i][i][lhs].append(("terminal", production))

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for b in table[i][k]:
                    for c in table[k + 1][j]:
                        pair = (b, c)
                        if pair in binary_rules:
                            for production in binary_rules[pair]:
                                lhs = production.lhs()
                                if lhs not in table[i][j]:
                                    table[i][j][lhs] = []
                                table[i][j][lhs].append(("binary", production, k, b, c))

    return table


def cky_recognize(grammar: CFG, sentence: list[str]) -> bool:
    """Check if a sentence is in the language of the CFG using CKY."""
    table = cky_parse(grammar, sentence)
    if table is None:
        return False
    n = len(sentence)
    return grammar.start() in table[0][n - 1]


def extract_trees(table, sentence, i, j, nonterminal):
    """Extract parse trees from backpointers."""
    if nonterminal not in table[i][j]:
        return []

    trees = []
    for backpointer in table[i][j][nonterminal]:
        bp_type = backpointer[0]

        if bp_type == "terminal":
            production = backpointer[1]
            word = sentence[i]
            tree = Tree(str(production.lhs()), [word])
            trees.append(tree)
        elif bp_type == "binary":
            production = backpointer[1]
            k = backpointer[2]
            left_nt = backpointer[3]
            right_nt = backpointer[4]

            left_trees = extract_trees(table, sentence, i, k, left_nt)
            right_trees = extract_trees(table, sentence, k + 1, j, right_nt)

            for left_tree in left_trees:
                for right_tree in right_trees:
                    tree = Tree(str(production.lhs()), [left_tree, right_tree])
                    trees.append(tree)

    return trees


def parse(grammar: CFG, sentence: list[str]) -> list[Tree]:
    """Parse a sentence and return all parse trees."""
    table = cky_parse(grammar, sentence)
    if table is None:
        return []
    n = len(sentence)
    if grammar.start() not in table[0][n - 1]:
        return []
    return extract_trees(table, sentence, 0, n - 1, grammar.start())
