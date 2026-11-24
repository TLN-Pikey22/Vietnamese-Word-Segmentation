
import pandas as pd
from sklearn.model_selection import train_test_split

from fmm import fmm
from bmm import bmm
from hmm import train_hmm, viterbi


# Tính các vị trí ranh giới từ
def get_boundaries(segmented):
    words = segmented.split()
    boundaries = set()
    position = 0

    for word in words:
        position += len(word.split("_"))
        boundaries.add(position)

    boundaries.discard(position)
    return boundaries


# Tính Precision, Recall và F1
def evaluate(gold, predicted):
    tp = 0
    fp = 0
    fn = 0

    for true_sentence, pred_sentence in zip(gold, predicted):
        true_boundaries = get_boundaries(true_sentence)
        pred_boundaries = get_boundaries(pred_sentence)

        tp += len(true_boundaries & pred_boundaries)
        fp += len(pred_boundaries - true_boundaries)
        fn += len(true_boundaries - pred_boundaries)

    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0
    )

    return f1


# Đọc dữ liệu
df = pd.read_csv("dataset.csv")

seeds = [42, 123, 2026]

results = []

for seed in seeds:
    print("\n========== SEED", seed, "==========")

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=seed
    )

    # Tạo từ điển từ tập Train
    dictionary = set()

    for sentence in train_df["segmented"]:
        for word in sentence.split():
            dictionary.add(word)

    # Tính L
    L = max(
        (len(word.split("_")) for word in dictionary),
        default=1
    )

    # Huấn luyện HMM
    model = train_hmm(train_df)

    # Dự đoán
    gold = test_df["segmented"].tolist()

    pred_fmm = [
        fmm(sentence, dictionary, L)
        for sentence in test_df["sentence"]
    ]

    pred_bmm = [
        bmm(sentence, dictionary, L)
        for sentence in test_df["sentence"]
    ]

    pred_hmm = [
        viterbi(sentence, model)
        for sentence in test_df["sentence"]
    ]

    # Tính F1
    f1_fmm = evaluate(gold, pred_fmm)
    f1_bmm = evaluate(gold, pred_bmm)
    f1_hmm = evaluate(gold, pred_hmm)

    results.append({
        "Seed": seed,
        "FMM": f1_fmm,
        "BMM": f1_bmm,
        "HMM": f1_hmm
    })

    print("F1 FMM:", round(f1_fmm, 4))
    print("F1 BMM:", round(f1_bmm, 4))
    print("F1 HMM:", round(f1_hmm, 4))


# Tổng hợp kết quả
result_df = pd.DataFrame(results)

print("\n========== BẢNG KẾT QUẢ ==========")
print(result_df.to_string(index=False))

print("\n========== F1 TRUNG BÌNH ==========")
print("FMM:", round(result_df["FMM"].mean(), 4))
print("BMM:", round(result_df["BMM"].mean(), 4))
print("HMM:", round(result_df["HMM"].mean(), 4))
