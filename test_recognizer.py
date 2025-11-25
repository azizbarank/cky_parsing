"""Test CKY recognizer on ATIS sentences and ungrammatical examples."""

from grammar_loader import load_atis_grammar, load_atis_sentences
from cky_recognizer import cky_recognize


def main():
    grammar = load_atis_grammar()
    sentences = load_atis_sentences()

    print("=" * 60)
    print("Testing ATIS sentences")
    print("=" * 60)

    accepted = 0
    rejected = 0

    for i, sentence in enumerate(sentences, 1):
        result = cky_recognize(grammar, sentence)
        status = "ACCEPTED" if result else "REJECTED"
        if result:
            accepted += 1
        else:
            rejected += 1
        print(f"{i:3}. [{status}] {' '.join(sentence)}")

    print(f"\nTotal: {accepted} accepted, {rejected} rejected out of {len(sentences)}")

    print("\n" + "=" * 60)
    print("Testing ungrammatical sentences")
    print("=" * 60)

    ungrammatical = [
        "i want want a flight".split(),
        "show me me flights".split(),
        "what is is the fare".split(),
        "the the the".split(),
        "hello world".split(),
        "asdfgh jklmnop".split(),
        "i need need a ticket".split(),
        "what what is price".split(),
        "xyz abc def".split(),
        "blah blah blah".split(),
        "computer says no".split(),
        "supercalifragilistic expialidocious".split(),
    ]

    for sentence in ungrammatical:
        result = cky_recognize(grammar, sentence)
        status = "ACCEPTED" if result else "REJECTED"
        print(f"[{status}] {' '.join(sentence)}")


if __name__ == "__main__":
    main()
