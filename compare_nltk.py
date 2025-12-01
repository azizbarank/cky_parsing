from nltk.parse.chart import ChartParser
from nltk.tree import ImmutableTree
from grammar_loader import load_atis_grammar, load_atis_sentences
from cky_recognizer import parse


def main():
    grammar = load_atis_grammar()
    sentences = load_atis_sentences()
    nltk_parser = ChartParser(grammar)

    print("Comparing CKY parser with NLTK ChartParser\n")
    print(f"{'Sentence':<50} {'Our Count':<12} {'NLTK Count':<12} {'Match'}")
    print("=" * 85)

    matches = 0
    total = 0

    for sentence in sentences[:20]:
        our_trees = parse(grammar, sentence)
        our_unique = set(ImmutableTree.convert(tree) for tree in our_trees)
        our_count = len(our_unique)

        try:
            nltk_trees = list(nltk_parser.parse(sentence))
            nltk_unique = set(ImmutableTree.convert(tree) for tree in nltk_trees)
            nltk_count = len(nltk_unique)
        except ValueError:
            nltk_count = 0

        match = "✓" if our_count == nltk_count else "✗"
        if our_count == nltk_count:
            matches += 1
        total += 1

        sentence_str = " ".join(sentence)[:47]
        print(f"{sentence_str:<50} {our_count:<12} {nltk_count:<12} {match}")

    print("=" * 85)
    print(f"Matches: {matches}/{total}")


if __name__ == "__main__":
    main()
