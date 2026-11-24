
import math
from collections import Counter, defaultdict


def train_hmm(train, alpha=1):
    states = ["B", "I"]

    # Đếm trạng thái bắt đầu, chuyển trạng thái và phát xạ
    start_counts = Counter()
    transition_counts = defaultdict(Counter)
    emission_counts = defaultdict(Counter)
    state_counts = Counter()
    vocabulary = set()

    for sentence, segmented in zip(train["sentence"], train["segmented"]):
        syllables = sentence.split()
        labels = []

        for word in segmented.split():
            parts = word.split("_")
            labels.extend(["B"] + ["I"] * (len(parts) - 1))

        if len(syllables) != len(labels):
            raise ValueError("Số tiếng và số nhãn không khớp!")

        if not labels:
            continue

        start_counts[labels[0]] += 1

        for i, (syllable, state) in enumerate(zip(syllables, labels)):
            vocabulary.add(syllable)
            emission_counts[state][syllable] += 1
            state_counts[state] += 1

            if i > 0:
                transition_counts[labels[i - 1]][state] += 1

    vocabulary.add("<UNK>")

    start_prob = {}
    transition_prob = {}
    emission_prob = {}

    # Xác suất bắt đầu
    for state in states:
        start_prob[state] = (start_counts[state] + alpha) / (
            sum(start_counts.values()) + alpha * len(states)
        )

    # Xác suất chuyển trạng thái
    for previous_state in states:
        transition_prob[previous_state] = {}
        outgoing_total = sum(transition_counts[previous_state].values())

        for state in states:
            transition_prob[previous_state][state] = (
                transition_counts[previous_state][state] + alpha
            ) / (outgoing_total + alpha * len(states))

    # Xác suất phát xạ
    for state in states:
        emission_prob[state] = {}

        for syllable in vocabulary:
            emission_prob[state][syllable] = (
                emission_counts[state][syllable] + alpha
            ) / (state_counts[state] + alpha * len(vocabulary))

    model = {
        "states": states,
        "vocabulary": vocabulary,
        "start_prob": start_prob,
        "transition_prob": transition_prob,
        "emission_prob": emission_prob
    }

    return model


def viterbi(sentence, model):
    syllables = sentence.split()
    n = len(syllables)

    if n == 0:
        return ""

    states = model["states"]
    vocabulary = model["vocabulary"]
    start_prob = model["start_prob"]
    transition_prob = model["transition_prob"]
    emission_prob = model["emission_prob"]

    dp = [{} for _ in range(n)]
    backpointer = [{} for _ in range(n)]

    # Khởi tạo
    first = syllables[0] if syllables[0] in vocabulary else "<UNK>"

    for state in states:
        dp[0][state] = (
            math.log(start_prob[state])
            + math.log(emission_prob[state][first])
        )

    # Quy hoạch động
    for i in range(1, n):
        word = syllables[i] if syllables[i] in vocabulary else "<UNK>"

        for state in states:
            best_score = float("-inf")
            best_previous = None

            for previous_state in states:
                score = (
                    dp[i - 1][previous_state]
                    + math.log(transition_prob[previous_state][state])
                    + math.log(emission_prob[state][word])
                )

                if score > best_score:
                    best_score = score
                    best_previous = previous_state

            dp[i][state] = best_score
            backpointer[i][state] = best_previous

    # Chọn trạng thái cuối và truy vết
    last_state = max(dp[-1], key=dp[-1].get)
    best_path = [last_state]

    for i in range(n - 1, 0, -1):
        last_state = backpointer[i][last_state]
        best_path.append(last_state)

    best_path.reverse()

    # B ghép bằng dấu cách, I ghép bằng dấu gạch dưới
    result = []

    for i, syllable in enumerate(syllables):
        if i > 0:
            result.append(" " if best_path[i] == "B" else "_")

        result.append(syllable)

    return "".join(result)
