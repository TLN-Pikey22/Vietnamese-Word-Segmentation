
def fmm(sentence, dictionary, L=None):
    syllables = sentence.split()
    result = []
    i = 0

    if L is None:
        L = max((len(word.split("_")) for word in dictionary), default=1)

    while i < len(syllables):
        found = False

        for j in range(min(len(syllables), i + L), i, -1):
            candidate = "_".join(syllables[i:j])

            if candidate in dictionary:
                result.append(candidate)
                i = j
                found = True
                break

        if not found:
            result.append(syllables[i])
            i += 1

    return " ".join(result)
