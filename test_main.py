from fastapi.testclient import TestClient
from main import app, students_lock

client = TestClient(app)

def test_create_student():
    """
    Kiểm thử tạo sinh viên mới (POST /students)
    """
    with students_lock:  # đồng bộ với API
        response = client.post(
            "/students",
            json={"id": 1, "name": "Alice", "age": 20, "major": "CNTT"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"

def test_get_student():
    """
    Kiểm thử lấy sinh viên theo ID (GET /students/{id})
    """
    with students_lock:
        response = client.get("/students/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Alice"

def test_update_student():
    """
    Kiểm thử cập nhật thông tin sinh viên (PUT /students/{id})
    """
    with students_lock:
        response = client.put(
            "/students/1",
            json={"id": 1, "name": "Alice", "age": 21, "major": "CNTT"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == 21

def test_delete_student():
    """
    Kiểm thử xóa sinh viên (DELETE /students/{id})
    """
    with students_lock:
        response = client.delete("/students/1")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Student deleted"

def test_get_nonexistent_student():
    """
    Kiểm thử GET sinh viên không tồn tại
    """
    with students_lock:
        response = client.get("/students/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Student not found"

def test_create_duplicate_student():
    """
    Kiểm thử POST sinh viên trùng ID
    """
    with students_lock:
        # Tạo sinh viên ban đầu
        client.post("/students", json={"id": 2, "name": "Bob", "age": 22, "major": "CNTT"})
        # Thử tạo lại với cùng ID
        response = client.post("/students", json={"id": 2, "name": "Bob", "age": 22, "major": "CNTT"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student ID already exists"
