
def bmm(sentence, dictionary, L=None):
    syllables = sentence.split()
    result = []
    i = len(syllables) - 1

    if L is None:
        L = max((len(word.split("_")) for word in dictionary), default=1)

    while i >= 0:
        found = False

        for j in range(max(0, i - L + 1), i + 1):
            candidate = "_".join(syllables[j:i + 1])

            if candidate in dictionary:
                result.insert(0, candidate)
                i = j - 1
                found = True
                break

        if not found:
            result.insert(0, syllables[i])
            i -= 1

    return " ".join(result)
