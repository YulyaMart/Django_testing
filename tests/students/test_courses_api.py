import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

# проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    
    course = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/1/')

    data = response.json()

    assert course[0].id == data['id']
    assert response.status_code == 200


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    course = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    data = response.json()

    assert len(course) == len(data)
    assert response.status_code == 200


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_filtered_course_by_id(client, course_factory):
    course = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?id={course[1].id}')

    data = response.json()

    assert course[1].id == data[0]['id']
    assert response.status_code == 200


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_get_filtered_course_by_name(client, course_factory):
    course = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?name={course[1].name}')

    data = response.json()

    assert course[1].name == data[0]['name']
    assert response.status_code == 200


# тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name': 'course test'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1



# тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=10)
    course_updated = {
        'name': 'course name updated'
    }

    response = client.patch(f'/api/v1/courses/{course[2].id}/', data=course_updated)
    
    data = response.json()
    
    assert course_updated['name'] == data['name']
    assert response.status_code == 200



# тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=10)

    response = client.delete(f'/api/v1/courses/{course[2].id}/')
    
    assert response.status_code == 204
