import collections, random, sys, textwrap


def build_markov_table(source_text):
    # Empty string acts as a 'beginning of text' marker
    word_one = ''
    word_two = ''



    # Builds a dict where every val defaults to [], like {'a': [], 'b': [], ...}
    possibles = collections.defaultdict(list) 

    for line in source_text:
        for current_word in line.split():
            # First word is recorded under key ('', '') -> 'FIRST'
            # Second word is recorded under key('', 'FIRST') -> 'SECOND'
            # Third under ('FIRST', 'SECOND') -> 'THIRD'

            word_tuple = (word_one, word_two)
            possibles[word_tuple].append(current_word)

            word_one = word_two
            word_two = current_word


    # Avoid empty lists at the end of input
    possibles[word_one, word_two].append('')
    possibles[word_two, ''].append('')

    return possibles

# { ['of', 'the'] -> 'house', ['Alice', 'said'] -> 'hello'}


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


generate_random_output(int(sys.argv[1]), build_markov_table(sys.stdin))

# Source: https://benhoyt.com/writings/markov-chain/
