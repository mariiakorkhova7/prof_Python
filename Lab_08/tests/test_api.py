def test_create_student(client):
    response = client.post("/students", json={"first_name": "Іван", "last_name": "Франко"})
    assert response.status_code == 201
    assert response.json()["first_name"] == "Іван"

def test_create_grade_and_average(client):
    client.post("/students", json={"first_name": "Іван", "last_name": "Франко"})
    client.post("/subjects", json={"name": "Математика"})
    
    response = client.post("/grades", json={"student_id": 1, "subject_id": 1, "value": 95.0})
    assert response.status_code == 201
    
    avg_resp = client.get("/students/1/average")
    assert avg_resp.status_code == 200
    assert avg_resp.json() == 95.0

def test_query_parameters(client):
    client.post("/students", json={"first_name": "Іван", "last_name": "Франко"})
    client.post("/subjects", json={"name": "Математика"})
    client.post("/grades", json={"student_id": 1, "subject_id": 1, "value": 95.0})
    
    # Шукаємо студентів із балом вище 90
    response = client.get("/students?min_average=90.0")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # Шукаємо студентів із балом вище 98
    response2 = client.get("/students?min_average=98.0")
    assert response2.status_code == 200
    assert len(response2.json()) == 0