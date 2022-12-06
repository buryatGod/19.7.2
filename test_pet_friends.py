import os
from api import Petfriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = Petfriends()


def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter = ''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert  len(result['pets']) > 0

def test_post_create_new_pet_without_photo(name = 'Бобик', animal_type = 'Собака', age = '2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_succesful_del_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барсик", "cat", "1", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name='Ябби', animal_type='Змея', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Здесь нет моих питомцев")

def test_post_create_new_pet_with_photo(name = 'Тенёк', animal_type = 'Кот', age = '4', pet_photo = 'images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Негативный тест кейс. Получение Api-ключа при использоавния неверного email
def test_get_api_key_for_invalid_user1(email = invalid_email, password = valid_password):
    status, result = pf.get_api_key_invalid_email(email, password)
    assert status == 400 or 401 or 402 or 403 or 404 or 405

# Негативный тест кейс. Получение Api-ключа при использоавния неверного password
def test_get_api_key_for_invalid_user2(email = valid_email, password = invalid_password):
    status, result = pf.get_api_key_invalid_password(email, password)
    assert status == 400 or 401 or 402 or 403 or 404 or 405

# Негативный тест кейс. Попытка обновить информацию о питомце с неправильным email
def test_update_pet_info_invalid_user1(name='', animal_type='Dog', age=3):
    _, auth_key = pf.get_api_key_invalid_email(invalid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 403
        assert result['name'] != name
    else:
        raise Exception("Здесь нет моих питомцев")

# Негативный тест кейс. Попытка добавить питомца без имени
def test_post_create_new_pet_without_name(name = '', animal_type = 'Cat', age = '3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 403
    assert result['name'] == name
