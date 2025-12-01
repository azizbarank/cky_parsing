# CKY Parser for ATIS Grammar

Implementation of the Cocke-Kasami-Younger (CKY) parsing algorithm for the ATIS airline travel corpus.

## Files

- `cky_recognizer.py` - CKY parser with tree extraction
- `grammar_loader.py` - Loads ATIS CNF grammar and test sentences
- `main.py` - Parses all sentences and generates output files
- `test_recognizer.py` - Tests recognizer on ATIS and ungrammatical sentences
- `compare_nltk.py` - Compares results with NLTK's ChartParser
- `parse_results.txt` - Tab-separated output (sentence\t#parses)
- `parse_visualizations.txt` - Parse trees for sentences with 2-5 parses

## Setup

Install dependencies using uv:
```bash
uv sync
```

Or using pip:
```bash
pip install nltk
```

## How to Run

```bash
python3 main.py
python3 compare_nltk.py
python3 test_recognizer.py
```

## Results

Parsed 98 ATIS test sentences:
- 28 sentences with 0 parses (ungrammatical)
- 4 sentences with 1 parse (unambiguous)
- 66 sentences with multiple parses (structurally ambiguous)
- Maximum: 36,122 parses for one highly ambiguous sentence
- Median: 3 parses per grammatical sentence

## Validation

Compared against NLTK's ChartParser on 20 sentences: 20/20 matches (100% accuracy)

## Implementation

The CKY algorithm builds a parse table bottom-up, storing backpointers for tree extraction. Parse trees are extracted recursively and deduplicated using ImmutableTree.
