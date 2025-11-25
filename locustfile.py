from locust import HttpUser, task, between
import itertools
import threading

# Bộ đếm ID duy nhất cho mỗi sinh viên
id_counter = itertools.count(1)
id_lock = threading.Lock()  # Lock để đồng bộ ID giữa các user

class StudentUser(HttpUser):
    # Khoảng thời gian chờ giữa các task
    wait_time = between(1, 3)

    @task(2)  # Tần suất GET gấp đôi POST
    def get_students(self):
        self.client.get("/students")

    @task(1)
    def create_student(self):
        # Đồng bộ lấy ID duy nhất
        with id_lock:
            student_id = next(id_counter)

        student_data = {
            "id": student_id,
            "name": f"Student{student_id}",
            "age": 18 + (student_id % 10),
            "major": "CNTT"
        }
        self.client.post("/students", json=student_data)
