bước 1: tạo môi trường ảo
python -m venv venv
chạy mt ảo
venv\Scripts\activate

pip install fastapi uvicorn pydantic pytest requests locust httpx

Bước 2: Chạy FastAPI server

Chạy server FastAPI với nhiều worker để xử lý đồng thời tốt:
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
--workers 4 giúp server xử lý nhiều POST request song song ổn định.
Truy cập API docs: http://127.0.0.1:8000/docs.
Bước 3: Kiểm thử chức năng với TestClient
Mở file test_main.py
Chạy kiểm thử:
pytest test_main.py

Kết quả:
Tất cả test CRUD phải pass 100%.
Kiểm tra các tình huống đặc biệt:
GET sinh viên không tồn tại → trả 404
POST sinh viên trùng ID → trả 400

Bước 4: Kiểm thử hiệu năng với Locust

Mở terminal, chạy Locust:

thực hiện
locust -f locustfile.py --host http://127.0.0.1:8000
Mở trình duyệt http://localhost:8089, thiết lập số user, nhấn Start Swarming.

| Kịch bản      | Number of users | Spawn rate |
| ------------- | --------------- | ---------- |
| 🔵 Nhẹ        | 20              | 2          |
| 🟡 Trung bình | 100             | 10         |
| 🔴 Nặng       | 500             | 20         |


Quan sát latency, requests/s, error rate.

