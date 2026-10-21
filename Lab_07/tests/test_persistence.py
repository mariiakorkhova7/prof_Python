import pytest
from grades_system.repositories import StudentRepository, SubjectRepository
from grades_system.services import GradeService
from grades_system.models import Grade

def test_crud_student(session):
    repo = StudentRepository(session)
    student = repo.add("Марія Корхова")
    assert student.id is not None
    assert student.full_name == "Марія Корхова"
    
    loaded = repo.get_by_id(student.id)
    assert loaded.full_name == "Марія Корхова"
    
    assert repo.delete(student.id) is True
    assert repo.get_by_id(student.id) is None

def test_batch_grades_rollback(session):
    student = StudentRepository(session).add("Іван Іванов")
    subject = SubjectRepository(session).add("Математика")
    service = GradeService(session)
    
    # Виклик rollback через некоректну оцінку (-5)[cite: 32, 48]
    with pytest.raises(ValueError):
        service.assign_batch_grades(student.id, subject.id, [90, 85, -5])
        
    # Перевірка властивості Atomicity: жодна оцінка не збереглася[cite: 40, 49]
    grades_count = session.query(Grade).count()
    assert grades_count == 0

def test_threshold_search(session):
    student1 = StudentRepository(session).add("Олена Петрівна")
    student2 = StudentRepository(session).add("Петро Олексійович")
    subject = SubjectRepository(session).add("Фізика")
    service = GradeService(session)
    
    service.assign_batch_grades(student1.id, subject.id, [95, 90]) # avg 92.5
    service.assign_batch_grades(student2.id, subject.id, [60, 70]) # avg 65
    
    excellent_students = service.get_students_above_threshold(90.0)
    assert len(excellent_students) == 1
    assert excellent_students[0][0] == "Олена Петрівна"