# Vietnamese Word Segmentation

## 1. Giới thiệu

Dự án thực hiện tách từ tiếng Việt bằng ba phương pháp:

- FMM (Forward Maximum Matching).
- BMM (Backward Maximum Matching).
- HMM kết hợp thuật toán Viterbi.

Mục tiêu là xây dựng chương trình tách từ, so sánh kết quả của các phương pháp và đánh giá chất lượng bằng Precision, Recall và F1-score.

## 2. Công nghệ sử dụng

- Ngôn ngữ lập trình: Python.
- Môi trường thực hiện: Google Colab.
- Thư viện: Pandas, NumPy, Matplotlib, Scikit-learn.
- Cấu trúc dữ liệu từ điển: Hash Table (Python Set).

## 3. Cấu trúc dự án

```text
Vietnamese-Word-Segmentation/
│
├── Vietnamese_Word_Segmentation.ipynb
├── dataset.csv
├── so_sanh_cac_mo_hinh.csv
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

## 5. Các phương pháp

### 5.1. FMM

Duyệt câu từ trái sang phải, chọn từ dài nhất có trong từ điển tại mỗi vị trí.

### 5.2. BMM

Duyệt câu từ phải sang trái, chọn từ dài nhất có trong từ điển tại mỗi vị trí.

### 5.3. HMM kết hợp Viterbi

Sử dụng mô hình Markov ẩn với hai trạng thái:

- B: Bắt đầu một từ.
- I: Tiếng nằm bên trong một từ nhiều tiếng.

Các xác suất khởi đầu, chuyển trạng thái và phát xạ được ước lượng từ dữ liệu huấn luyện. Áp dụng làm trơn Laplace và log xác suất để thực hiện thuật toán Viterbi.

## 6. Kết quả thực nghiệm

Kết quả đánh giá trên tập Test:

| Mô hình | Precision | Recall | F1-score |
|---|---:|---:|---:|
| FMM | 0.5698 | 0.7259 | 0.6384 |
| BMM | 0.5698 | 0.7259 | 0.6384 |
| HMM ban đầu | 0.7395 | 0.6519 | 0.6929 |
| HMM UNK ngưỡng 2 | 0.6129 | 0.5630 | 0.5869 |
| HMM UNK ngưỡng 3 | 0.5630 | 0.4963 | 0.5276 |
| HMM không phân biệt hoa/thường | 0.7143 | 0.6296 | 0.6693 |

HMM ban đầu đạt F1-score cao nhất (0.6929) trong các phương pháp được thử nghiệm.

## 7. Hướng dẫn chạy chương trình

1. Truy cập Google Colab: https://colab.research.google.com/
2. Tải notebook của dự án lên Google Colab.
3. Tải file `dataset.csv` khi notebook yêu cầu.
4. Chạy lần lượt các ô lệnh từ trên xuống dưới.
5. Theo dõi kết quả đánh giá và bảng so sánh các mô hình.
6. File `so_sanh_cac_mo_hinh.csv` được tạo để lưu kết quả thực nghiệm.

## 8. Hạn chế

- Bộ dữ liệu hiện tại còn nhỏ, gồm 120 câu.
- Dữ liệu được tự gán nhãn nên cần được kiểm tra và mở rộng thêm.
- Một số tiếng chưa xuất hiện trong tập huấn luyện có thể ảnh hưởng đến kết quả HMM.
- Kết quả thực nghiệm phụ thuộc vào dữ liệu và cách chia Train/Test.

## 9. Hướng phát triển

- Mở rộng bộ dữ liệu huấn luyện và kiểm tra.
- Thử nghiệm cấu trúc Trie để tối ưu tra cứu từ.
- Cải thiện khả năng xử lý tiếng chưa xuất hiện.
- Nghiên cứu và thử nghiệm các mô hình tách từ nâng cao hơn.
