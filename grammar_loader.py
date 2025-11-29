from pathlib import Path
from nltk.grammar import CFG

DATA_DIR = Path(__file__).parent / "data"


def load_atis_grammar(cnf: bool = True) -> CFG:
    """Load ATIS CFG grammar in CNF or original form."""
    grammar_file = "atis-grammar-cnf.cfg" if cnf else "atis-grammar-original.cfg"
    grammar_path = DATA_DIR / grammar_file
    with open(grammar_path) as f:
        return CFG.fromstring(f.read())


def load_atis_sentences() -> list[list[str]]:
    """Load ATIS test sentences as tokenized lists."""
    sentences_path = DATA_DIR / "atis-test-sentences.txt"
    with open(sentences_path) as f:
        return [line.strip().split() for line in f if line.strip()]
