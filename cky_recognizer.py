"""CKY algorithm for sentence recognition with backpointers."""

from nltk.grammar import CFG
from nltk.tree import Tree


def cky_recognize(grammar: CFG, sentence: list[str]) -> bool:
    """Check if a sentence is in the language of the CFG using CKY.

    This version stores backpointers for parse tree extraction.
    """
    n = len(sentence)
    if n == 0:
        return False

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

    # Table now stores dict: {Nonterminal: [list of backpointers]}
    table = [[{} for _ in range(n)] for _ in range(n)]

    # Initialize with terminal rules
    for i in range(n):
        word = sentence[i]
        if word in terminal_rules:
            for production in terminal_rules[word]:
                lhs = production.lhs()
                if lhs not in table[i][i]:
                    table[i][i][lhs] = []
                # Backpointer for terminal: (production, None for terminal)
                table[i][i][lhs].append(("terminal", production))

    # Fill table with binary rules
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
                                # Backpointer: (type, production, split_point, left_NT, right_NT)
                                table[i][j][lhs].append(("binary", production, k, b, c))

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

    return trees
