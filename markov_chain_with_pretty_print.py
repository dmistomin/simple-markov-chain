import collections, random, statistics, sys, textwrap


def build_markov_table(source_text):
    # Empty string acts as a 'beginning of text' marker
    word_one = ''
    word_two = ''

    # Builds a dict where every val defaults to [], like {'a': [], 'b': [], ...}
    possibles = collections.defaultdict(list)

    for line in source_text:
        for current_word in line.split():
            # First word is recorded under key ('', '') -> 'FIRST'
            # Second word is recorded under key ('', 'FIRST') -> 'SECOND'
            # Third under ('FIRST', 'SECOND') -> 'THIRD'

            word_tuple = (word_one, word_two)
            possibles[word_tuple].append(current_word)

            word_one = word_two
            word_two = current_word

    # Avoid empty lists at the end of input
    possibles[word_one, word_two].append('')
    possibles[word_two, ''].append('')

    return possibles


def generate_random_output(output_length, markov_table):
    def starts_with_capital(key):
        first_word = key[0]
        if not first_word:
            return False
        return first_word[0].isupper()

    sentence_starts = [key for key in markov_table if starts_with_capital(key)]
    word_one, word_two = random.choice(sentence_starts)
    output = [word_one, word_two]

    for _ in range(output_length):
        word = random.choice(markov_table[word_one, word_two])
        output.append(word)
        word_one = word_two
        word_two = word

    print(textwrap.fill(' '.join(output)))


def summarize_markov_table(markov_table, top_n=5, sample_n=5):
    """Print a summary of the Markov table: size, branching distribution, and sample entries."""

    successor_counts = [len(successors) for successors in markov_table.values()]
    total_transitions = sum(successor_counts)
    unique_bigrams = len(markov_table)

    vocabulary = set()
    for key in markov_table:
        vocabulary.update(key)
    for successors in markov_table.values():
        vocabulary.update(successors)
    vocabulary.discard('')  # The '' sentinel isn't really a word

    # --- Size stats ---
    print("Markov chain summary")
    print("=" * 60)
    print(f"  Unique bigram keys:     {unique_bigrams:>8,}")
    print(f"  Total transitions:      {total_transitions:>8,}")
    print(f"  Unique words:           {len(vocabulary):>8,}")
    print(f"  Avg successors per key: {total_transitions / unique_bigrams:>8.2f}")
    print(f"  Median successors:      {statistics.median(successor_counts):>8.0f}")
    print(f"  Max successors:         {max(successor_counts):>8}")
    print()

    # --- Branching distribution ---
    #
    # How many different words can follow each bigram? For most bigrams it's just one
    # (those are the parts of the source text that get reproduced near-verbatim).
    # Bigrams with many successors are the "decision points" where output can diverge.
    buckets = [('1 successor     ', lambda n: n == 1),
               ('2-5 successors  ', lambda n: 2 <= n <= 5),
               ('6-20 successors ', lambda n: 6 <= n <= 20),
               ('21+ successors  ', lambda n: n >= 21)]

    print("Branching distribution:")
    for label, predicate in buckets:
        count = sum(1 for n in successor_counts if predicate(n))
        pct = 100 * count / unique_bigrams
        bar = '█' * int(pct / 2)  # each block = 2%
        print(f"  {label} {count:>6,}  ({pct:5.1f}%)  {bar}")
    print()

    # --- Top branching bigrams ---
    #
    # Sorted by successor count. These are the bigrams where the generator has
    # the most choices. The preview shows the top successors so you can eyeball
    # the weighted-sampling distribution.
    top_branching = sorted(markov_table.items(), key=lambda kv: -len(kv[1]))[:top_n]
    print(f"Top {top_n} branching bigrams:")
    for (w1, w2), successors in top_branching:
        top_successors = collections.Counter(successors).most_common(4)
        preview = ", ".join(
            f"{w!r}×{c}" if c > 1 else f"{w!r}"
            for w, c in top_successors
        )
        bigram_label = f"({w1!r}, {w2!r})"
        print(f"  {bigram_label:<32} -> {len(successors):>3} successors: {preview}, ...")
    print()

    # --- Random sample entries ---
    #
    # Shows raw successor lists, including duplicates -- the list-of-duplicates
    # representation is what gives random.choice frequency-weighted sampling.
    sample_keys = random.sample(list(markov_table.keys()), min(sample_n, len(markov_table)))
    print(f"Random sample of {len(sample_keys)} entries:")
    for key in sample_keys:
        w1, w2 = key
        successors = markov_table[key]
        preview = successors[:8]
        truncated = ", ..." if len(successors) > 8 else ""
        bigram_label = f"({w1!r}, {w2!r})"
        print(f"  {bigram_label:<32} -> {preview}{truncated}")
    print()


if __name__ == '__main__':
    markov_table = build_markov_table(sys.stdin)
    summarize_markov_table(markov_table)

    print("Generated text")
    print("=" * 60)
    generate_random_output(int(sys.argv[1]), markov_table)
