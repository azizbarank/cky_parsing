# CKY Parsing for Context-Free Grammars Report

## Overview

I implemented the Cocke-Kasami-Younger (CKY) algorithm for parsing sentences according to a context-free grammar. The implementation includes both recognition and full parse tree extraction with backpointers.

---

## Implementation

### Data

I used the ATIS (Air Travel Information System) corpus:
- Grammar: ATIS CFG in Chomsky Normal Form
- Test set: 98 sentences

### Components

**1. Grammar Loader** (`grammar_loader.py`)

I loaded the ATIS grammar in CNF format and the test sentences using NLTK's CFG parser. The loader provides functions to access both the grammar and tokenized sentences.

**2. CKY Parser** (`cky_recognizer.py`)

I implemented three main functions:

- `cky_parse()`: Builds the parse table bottom-up, storing backpointers for each nonterminal in each cell
- `extract_trees()`: Recursively extracts all parse trees from the backpointers
- `parse()`: Combines the above to return all valid parse trees for a sentence

**3. Backpointers**

For each nonterminal in each cell, I store backpointers in two formats:
- Terminal: `("terminal", production)` for leaf nodes
- Binary: `("binary", production, split_point, left_NT, right_NT)` for internal nodes

This allows complete reconstruction of all parse trees.

**4. Tree Deduplication**

I used NLTK's `ImmutableTree` to convert trees into hashable objects, allowing me to store them in sets and count unique parses accurately.

---

## Results

**Overall Statistics**:
- Total sentences: 98
- Sentences with 0 parses: 28 (ungrammatical)
- Sentences with 1 parse: 4 (unambiguous)
- Sentences with multiple parses: 66 (structurally ambiguous)

**Ambiguity Distribution**:
- Median parses per grammatical sentence: 3
- Maximum parses: 36,122 for one highly ambiguous sentence

**Examples of sentences with 2-5 parses**:
- "prices ." → 2 parses (noun vs. verb)
- "show availability ." → 3 parses (different phrase structures)
- "list saturday flights ." → 5 parses (modifier attachment ambiguity)

---

## Discussion

### Validation

I compared my implementation against NLTK's built-in ChartParser on 20 test sentences. The results matched fully (20/20), thus, confirming the correctness of the CKY implementation.

### Why so many parses?

It turned out to be that for some sentences, there are many parses because of the following factors:

1. **Lexical ambiguity**: Many words can be multiple parts of speech (e.g., "prices" as noun or verb).

2. **Structural ambiguity**: Prepositional phrase attachment and modifier scope create multiple valid parse trees even when the word categories are fixed.

3. **Grammar coverage**: The ATIS grammar is designed for broad coverage, which means it accepts many grammatical variations that a human might consider unusual.

### Implementation choices

1. **Bottom-up parsing**: The CKY algorithm builds larger constituents from smaller ones, making it efficient for ambiguous grammars.

2. **CNF requirement**: By using Chomsky Normal Form, every production has exactly 2 or 1 symbols on the right-hand side, which simplifies the parsing logic significantly.

3. **Complete extraction**: Unlike just counting parses, I extract all parse trees explicitly. This allows visualization but can be memory-intensive for highly ambiguous sentences.

---
