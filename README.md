# Simple Markov Chain

A toy text generator using a second-order Markov chain. Feed it one or more books and it produces random text that mimics the style of the source material.

## Requirements

Python 3 (no external dependencies).

## Usage

Both scripts read text from **stdin** and take one argument: the number of words to generate.

### Basic generation

```sh
cat data/alice_in_wonderland.txt | python3 markov_chain.py 100
```

### Generation with stats

Prints a summary of the Markov table (branching distribution, top bigrams, etc.) before generating text:

```sh
cat data/alice_in_wonderland.txt | python3 markov_chain_with_pretty_print.py 100
```

### Combining multiple sources

```sh
cat data/*.txt | python3 markov_chain.py 200
```

## Data

The `data/` directory contains public-domain texts from Project Gutenberg:

- `alice_in_wonderland.txt` - Lewis Carroll
- `communist_manifesto.txt` - Karl Marx and Friedrich Engels
- `macbeth.txt` - William Shakespeare
- `winnie_the_pooh.txt` - A. A. Milne
