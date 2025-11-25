
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

locust -f locustfile.py --host http://127.0.0.1:8000

Truy cập giao diện web Locust: http://127.0.0.1:8089
Cấu hình kịch bản:
Number of users (tổng user): 20 (nhẹ), 100 (trung bình), 500 (nặng)
Spawn rate (user/s): 2 (nhẹ), 10 (trung bình), 20 (nặng)
Click Start swarming.


locust -f locustfile.py --host http://127.0.0.1:8000
thực hiện

ab -n 5000 -c 100 http://127.0.0.1:8000/students

locust -f locustfile.py
Mở trình duyệt http://localhost:8089, thiết lập số user, nhấn Start Swarming.

| Kịch bản      | Number of users | Spawn rate |
| ------------- | --------------- | ---------- |
| 🔵 Nhẹ        | 20              | 2          |
| 🟡 Trung bình | 100             | 10         |
| 🔴 Nặng       | 500             | 20         |


Quan sát latency, requests/s, error rate.

