"""CKY algorithm for sentence recognition."""

from nltk.grammar import CFG


def cky_recognize(grammar: CFG, sentence: list[str]) -> bool:
    """Check if a sentence is in the language of the CFG using CKY."""
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
                terminal_rules[word] = set()
            terminal_rules[word].add(lhs)
        elif len(rhs) == 2:
            pair = (rhs[0], rhs[1])
            if pair not in binary_rules:
                binary_rules[pair] = set()
            binary_rules[pair].add(lhs)

    table = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        word = sentence[i]
        if word in terminal_rules:
            table[i][i] = terminal_rules[word].copy()

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for b in table[i][k]:
                    for c in table[k + 1][j]:
                        pair = (b, c)
                        if pair in binary_rules:
                            table[i][j].update(binary_rules[pair])

    return grammar.start() in table[0][n - 1]
