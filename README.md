# Vietnamese Word Segmentation

## 1. Giới thiệu

Dự án thực hiện nghiên cứu và xây dựng chương trình tách từ tiếng Việt bằng ba phương pháp:

- FMM (Forward Maximum Matching).
- BMM (Backward Maximum Matching).
- HMM (Hidden Markov Model) kết hợp thuật toán Viterbi.

Mục tiêu của dự án là xây dựng các thuật toán tách từ, so sánh kết quả giữa các phương pháp và đánh giá chất lượng thông qua các chỉ số Precision, Recall và F1-score.

Trong quá trình thực hiện, dự án cũng tiến hành tối ưu thuật toán, xây dựng Unit Tests và đánh giá độ ổn định của mô hình qua nhiều lần chia dữ liệu Train/Test.

## 2. Công nghệ sử dụng

- Ngôn ngữ lập trình: Python.
- Môi trường thực hiện: Google Colab.
- Thư viện: Pandas, NumPy, Matplotlib, Scikit-learn.
- Cấu trúc dữ liệu từ điển: Hash Table (Python Set).
- Kiểm thử: Python Unittest.

## 3. Cấu trúc dự án

```text
Vietnamese-Word-Segmentation/
│
├── dataset/
│   └── dataset.csv
│
├── experiments/
│   └── run_experiments.py
│
├── notebooks/
│   ├── Vietnamese_Word_Segmentation_Week3.ipynb
│   └── Vietnamese_Word_Segmentation_Week4.ipynb
│
├── src/
│   ├── bmm.py
│   ├── fmm.py
│   └── hmm.py
│
├── tests/
│   ├── test_fmm_bmm.py
│   └── test_viterbi.py
│
└── README.md
```

## 4. Dữ liệu

Dự án sử dụng bộ dữ liệu gồm 120 câu tiếng Việt được tự gán nhãn.

Dữ liệu gồm hai cột:

- `sentence`: Câu đầu vào, các tiếng được phân cách bằng dấu cách.
- `segmented`: Câu đã tách từ, các tiếng thuộc cùng một từ được nối bằng dấu gạch dưới `_`.

Dữ liệu được chia thành:

- Tập huấn luyện (Train): 80%.
- Tập kiểm tra (Test): 20%.

Đối với thực nghiệm ở Tuần 4, việc chia dữ liệu được thực hiện với ba giá trị random seed khác nhau: 42, 123 và 2026.

## 5. Các phương pháp

### 5.1. FMM (Forward Maximum Matching)

Duyệt câu từ trái sang phải. Tại mỗi vị trí, thuật toán chọn chuỗi tiếng dài nhất có trong từ điển. Nếu không tìm thấy từ phù hợp, thuật toán giữ nguyên tiếng hiện tại.

### 5.2. BMM (Backward Maximum Matching)

Duyệt câu từ phải sang trái. Tại mỗi vị trí, thuật toán chọn chuỗi tiếng dài nhất có trong từ điển. Kết quả được ghép lại theo đúng thứ tự ban đầu của câu.

### 5.3. HMM kết hợp Viterbi

Sử dụng mô hình Markov ẩn với hai trạng thái:

- B: Bắt đầu một từ.
- I: Tiếng nằm bên trong một từ nhiều tiếng.

Các xác suất khởi đầu, chuyển trạng thái và phát xạ được ước lượng từ dữ liệu huấn luyện.

Mô hình sử dụng làm trơn Laplace và log xác suất để hạn chế hiện tượng xác suất bằng 0, sau đó áp dụng thuật toán Viterbi để tìm chuỗi trạng thái có xác suất cao nhất.

## 6. Kết quả thực nghiệm Tuần 3

Kết quả đánh giá trên tập Test:

| Mô hình | Precision | Recall | F1-score |
|---|---:|---:|---:|
| FMM | 0.5698 | 0.7259 | 0.6384 |
| BMM | 0.5698 | 0.7259 | 0.6384 |
| HMM ban đầu | 0.7395 | 0.6519 | 0.6929 |
| HMM UNK ngưỡng 2 | 0.6129 | 0.5630 | 0.5869 |
| HMM UNK ngưỡng 3 | 0.5630 | 0.4963 | 0.5276 |
| HMM không phân biệt hoa/thường | 0.7143 | 0.6296 | 0.6693 |

HMM ban đầu đạt F1-score cao nhất (0.6929) trong các phương pháp và biến thể được thử nghiệm ở Tuần 3.

## 7. Tối ưu thuật toán Tuần 4

### 7.1. Tối ưu độ dài tìm kiếm L

Đối với FMM và BMM, thay vì tìm kiếm trên toàn bộ phần còn lại của câu, thuật toán giới hạn độ dài chuỗi cần kiểm tra bằng độ dài từ dài nhất trong từ điển.

Trong thực nghiệm, từ điển có 302 từ và độ dài từ lớn nhất là L = 3.

Việc giới hạn phạm vi tìm kiếm giúp giảm số lần kiểm tra từ không cần thiết.

### 7.2. Kết quả đo thời gian

Thực hiện đo thời gian với 24 câu kiểm tra, lặp lại 1000 lần.

| Thuật toán | Trước tối ưu (giây) | Sau tối ưu (giây) | Tốc độ cải thiện |
|---|---:|---:|---:|
| FMM | 0.9562 | 0.2123 | 4.50 lần |
| BMM | 0.4229 | 0.2190 | 1.93 lần |

Kết quả cho thấy việc giới hạn độ dài tìm kiếm L giúp giảm đáng kể thời gian thực thi của cả FMM và BMM.

Lưu ý: Thời gian thực thi có thể thay đổi tùy thuộc vào môi trường và cấu hình máy tính.

### 7.3. Kiểm thử Unit Tests

Dự án xây dựng 3 Unit Tests:

- Kiểm thử thuật toán FMM với câu mẫu `"học sinh học sinh học"`.
- Kiểm thử thuật toán BMM với cùng câu mẫu.
- Kiểm thử thuật toán Viterbi bằng ví dụ gồm 3 tiếng, trong đó kết quả được tính toán thủ công để đối chiếu.

Kết quả kiểm thử:

```text
Ran 3 tests in 0.001s

OK
```

Cả 3 Unit Tests đều thực hiện thành công.

### 7.4. Thực nghiệm với 3 lần chia dữ liệu

Tiến hành chia dữ liệu Train/Test theo tỷ lệ 80/20 với ba random seed khác nhau.

Kết quả F1-score:

| Random seed | FMM | BMM | HMM |
|---|---:|---:|---:|
| 42 | 0.857143 | 0.857143 | 0.825243 |
| 123 | 0.854772 | 0.854772 | 0.832487 |
| 2026 | 0.855019 | 0.855019 | 0.837838 |
| Trung bình | 0.8556 | 0.8556 | 0.8319 |

FMM và BMM đạt F1-score trung bình 0.8556, trong khi HMM đạt 0.8319.

Kết quả cho thấy FMM và BMM có kết quả tương đương nhau trong ba lần thực nghiệm. HMM có F1-score thấp hơn trong thực nghiệm này.

Lưu ý: Kết quả ở mục này được đánh giá bằng cách so sánh ranh giới từ. Không nên so sánh trực tiếp với kết quả Tuần 3 nếu cách đánh giá hoặc cách chia dữ liệu khác nhau.

## 8. Hướng dẫn chạy chương trình

### 8.1. Thực hiện trên Google Colab

1. Truy cập Google Colab: https://colab.research.google.com/
2. Tải notebook trong thư mục `notebooks/` lên Google Colab.
3. Đảm bảo file dữ liệu `dataset.csv` được đặt đúng đường dẫn mà notebook sử dụng.
4. Chạy lần lượt các ô lệnh từ trên xuống dưới.
5. Theo dõi kết quả đánh giá và bảng so sánh các mô hình.

### 8.2. Kiểm thử các module Python

Tại thư mục gốc của dự án, chạy lệnh:

```bash
python -m unittest discover -s tests -v
```

Lệnh trên thực hiện các Unit Tests trong thư mục `tests/`.

### 8.3. Chạy thực nghiệm

Chạy file `run_experiments.py` trong thư mục `experiments/` để thực hiện đánh giá với ba random seed và lưu kết quả.

## 9. Hạn chế

- Bộ dữ liệu hiện tại còn nhỏ, chỉ gồm 120 câu tiếng Việt.
- Dữ liệu được tự gán nhãn nên cần được kiểm tra và mở rộng thêm.
- Một số tiếng chưa xuất hiện trong tập huấn luyện có thể ảnh hưởng đến kết quả HMM.
- Các thuật toán FMM và BMM phụ thuộc nhiều vào chất lượng và độ bao phủ của từ điển.
- Kết quả thực nghiệm có thể thay đổi tùy thuộc vào cách chia dữ liệu và phương pháp đánh giá.

## 10. Hướng phát triển

- Mở rộng bộ dữ liệu huấn luyện và kiểm tra.
- Nghiên cứu và thử nghiệm cấu trúc Trie để tối ưu quá trình tra cứu từ.
- Cải thiện khả năng xử lý các tiếng chưa xuất hiện trong tập huấn luyện.
- Thử nghiệm các mô hình tách từ nâng cao hơn.
- Tiếp tục tối ưu hiệu năng và đánh giá mô hình trên bộ dữ liệu lớn hơn.
