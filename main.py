from nltk.tree import ImmutableTree
from grammar_loader import load_atis_grammar, load_atis_sentences
from cky_recognizer import parse


def main():
    grammar = load_atis_grammar()
    sentences = load_atis_sentences()

    results = []
    for sentence in sentences:
        trees = parse(grammar, sentence)
        unique_trees = set(ImmutableTree.convert(tree) for tree in trees)
        num_parses = len(unique_trees)
        sentence_str = " ".join(sentence)
        results.append((sentence_str, num_parses, unique_trees))
        print(f"{sentence_str}\t{num_parses}")

    with open("parse_results.txt", "w") as f:
        for sentence_str, num_parses, _ in results:
            f.write(f"{sentence_str}\t{num_parses}\n")

    print(f"\nResults written to parse_results.txt")

    with open("parse_visualizations.txt", "w") as f:
        for sentence_str, num_parses, unique_trees in results:
            if 2 <= num_parses <= 5:
                f.write(f"\n{'=' * 70}\n")
                f.write(f"Sentence: {sentence_str}\n")
                f.write(f"Number of parses: {num_parses}\n")
                f.write(f"{'=' * 70}\n\n")
                for i, tree in enumerate(unique_trees, 1):
                    f.write(f"Parse {i}:\n")
                    f.write(str(tree) + "\n\n")

    print(f"Visualizations written to parse_visualizations.txt")


if __name__ == "__main__":
    main()
