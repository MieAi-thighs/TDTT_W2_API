# Lab 1: 2D to 3D - Depth Estimation Web API

Dự án triển khai một hệ thống Web API sử dụng mô hình học sâu để thực hiện bài toán **ước tính bản đồ độ sâu (Depth Estimation)** từ một ảnh 2D duy nhất.

## 1. Thông tin sinh viên

| Thông tin     |                        |
| ------------- | ---------------------- |
| **Họ và tên** | Nguyễn Phan Khánh Đăng |
| **MSSV**      | 24120032               |
| **Lớp**       | 24CTT5                 |

## 2. Mô hình sử dụng

- **Tên mô hình**: `Intel/dpt-large` (Dense Prediction Transformer)
- **Liên kết Hugging Face**: [Intel/dpt-large on Hugging Face](https://huggingface.co/Intel/dpt-large)

## 3. Mô tả chức năng hệ thống

Hệ thống cung cấp một **Web API** cho phép người dùng tải lên một tấm ảnh định dạng `.jpg` hoặc `.png`. Sau đó, mô hình AI sẽ xử lý và trả về dữ liệu JSON chứa thông tin về bản đồ độ sâu của tấm ảnh đó, bao gồm:

- Kích thước ảnh (Rộng x Cao)
- Giá trị độ sâu lớn nhất (`max_depth`)
- Giá trị độ sâu nhỏ nhất (`min_depth`)

## 4. Hướng dẫn cài đặt thư viện

Dự án được phát triển bằng ngôn ngữ **Python**. Để cài đặt các thư viện cần thiết, hãy chạy lệnh sau trong terminal:

```bash
pip install -r requirements.txt
```

### Thư viện sử dụng:

| Thư viện           | Mục đích                              |
| ------------------ | ------------------------------------- |
| `fastapi`          | Framework xây dựng Web API            |
| `uvicorn`          | ASGI server để chạy FastAPI           |
| `torch`            | PyTorch - framework deep learning     |
| `transformers`     | Thư viện Hugging Face để load mô hình |
| `pillow`           | Xử lý ảnh                             |
| `python-multipart` | Xử lý file upload                     |
| `requests`         | Gọi API (dùng cho testing)            |

## 5. Hướng dẫn chạy chương trình

### A. Chạy trên Google Colab

- **Cell 1 - Cài đặt môi trường**: Cài đặt các thư viện lõi
  > **Lưu ý**: Nếu Colab yêu cầu "Restart Session", hãy xác nhận và chạy cell 2.
- **Cell 2 - Khởi tạo Script Code & Model: Sử dụng lệnh `%%writefile main.py` để xuất mã nguồn ra file script riêng biệt**:
  - Tải mô hình AI `Intel/dpt-large` từ Hugging Face.

  - Thiết lập các Endpoint cho FastAPI.

  > **Lưu ý**: Cell này sẽ chạy ngầm một Thread để giữ Server luôn hoạt động ở cổng `8000`.

- **Cell 3 - Tạo Public URL (Pinggy Tunnel)**:
  - Sử dụng SSH để chuyển tiếp cổng từ máy ảo ra Internet.

  - Sau khi chạy, link truy cập có dạng `https://xxxx.a.free.pinggy.link` sẽ hiển thị ở terminal.
  
### B. Chạy trên Local

Sau khi đã có file `main.py` và tải các thư viện cần thiết như đã hướng dẫn, ta thực hiện:

```Bash
uvicorn main:app --reload
```
*Server sẽ chạy tại: http://127.0.0.1:8000*

### C. Kiểm thử kết quả

Sau khi Server (ở Colab hoặc Local) đã sẵn sàng:
1. Mở file `test_api.py` trên máy bạn.
2. Thay đổi biến `BASE_URL` thành link bạn nhận được từ Pinggy (nếu dùng Colab) hoặc `http://127.0.0.1:8000` (nếu chạy local).
3. Chạy lệnh: `python test_api.py` để gửi ảnh và nhận file Heatmap về thư mục máy mình.

## 6. Hướng dẫn gọi API và ví dụ về Request/Response

### Gọi API

**Giao diện Swagger UI**

Sau khi có Public URL ở Cell 3, bạn có thể truy cập trực tiếp bằng trình duyệt:
`[Public_URL]/docs` để kiểm tra các hàm bằng giao diện trực quan.

**Gọi API từ bên ngoài (Ví dụ Python)**

Sử dụng script `test_api.py` đính kèm hoặc chạy Cell kiểm thử trong Notebook:

```Python
import requests

url = "https://[Public_URL_Từ_Cell_3]/predict"
files = {"file": open("image_test.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Request/Response

**Request**

```JSON
{
  "file": "test_1.jpg",
  "content_type": "image/jpeg"
}
```

**Response(Thành công)**

```JSON
{
  "status": "success",
  "filename": "test_1.jpg",
  "heatmap_path": "/outputs/heatmap_test_1.jpg.png",
  "depth_map_info": {
    "width": 1000,
    "height": 667,
    "max_depth": 47.61238098144531,
    "min_depth": 0.15660227835178375
  }
}
```

**Response(Lỗi)**

```JSON
{
  "status": "error",
  "message": "Lỗi: Định dạng file không phải là hình ảnh."
}
```

## 7.Video Demo

**Link Video**: [![Xem Video Demo](https://img.youtube.com/vi/x-jAM1qeUmU/0.jpg)](https://www.youtube.com/watch?v=x-jAM1qeUmU)

## 8. Kết quả thực nghiệm

|          Ảnh gốc (Input)          |                 Bản đồ độ sâu (Heatmap Output)                 |
| :-------------------------------: | :------------------------------------------------------------: |
| ![Original](test_img/test_1.jpg)  |             ![Heatmap](outputs/heatmap_test_1.jpg)             |
| ![Original](test_img/test_2.jpeg) |            ![Heatmap](outputs/heatmap_test_2.jpeg)             |
|     _Mô tả: Ảnh chụp thực tế_     | _Mô tả: Ma trận độ sâu từ Model DPT ánh xạ qua bảng màu Magma_ |

## Cấu trúc thư mục dự án

```DPT
project/
├── main.py              # File chính chạy FastAPI server
├── requirements.txt     # Danh sách thư viện cần cài đặt
├── README.md           # Tài liệu hướng dẫn (file này)
└── test_images/        # Thư mục chứa ảnh test (optional)
│    └── image_test.jpg
└── outputs/            #  Thư mục chứa bản đồ độ sâu (optional)
    └──heatmap_test.jpg
```

## License

Dự án này được phát triển cho mục đích học tập.

## Tham khảo

- [Hugging Face - Intel/dpt-large](https://huggingface.co/Intel/dpt-large)
- [FastAPI Documents](https://fastapi.tiangolo.com)
