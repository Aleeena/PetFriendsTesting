import pytest

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем возможность получения авторизационного ключа с валидными данными"""
    # Запрашиваем ключ
    status, result = pf.get_api_key(email, password)
    # Проверяем статус ответа и нахождение 'key' в тексте ответа
    assert status == 200
    assert 'key' in result


def test_get_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    """Возможность получения авторизационного ключа с неправильным email"""
    # Запрашиваем ключ
    status, result = pf.get_api_key(email, password)
    # Удостоверяемся, что статус ответа 403
    assert status == 403


def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    """Возможность получения авторизационного ключа с неправильным паролем"""
    # Запрашиваем ключ
    status, result = pf.get_api_key(email, password)
    # Удостоверяемся, что статус ответа 403
    assert status == 403


def test_get_api_key_with_invalid_user_data(email=invalid_email, password=invalid_password):
    """Возможность получения авторизационного ключа с невалидными данными юзера (некорректный email и пароль)"""
    # Запрашиваем ключ
    status, result = pf.get_api_key(email, password)
    # Удостоверяемся, что статус ответа 403
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список."""
    # Запрашиваем ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем статус ответа и то, что в результате мы получаем не пустой список
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список."""
    # Запрашиваем ключ
    _, auth_key = pf.get_api_key(invalid_email, invalid_password)

    # Ловим ошибку при запросе списка питомцев с некорректным ключом
    with pytest.raises(TypeError):
        status, result = pf.get_list_of_pets(auth_key, filter)


def test_add_new_pet_with_valid_key_and_data(name='Карамба', animal_type='кошка', age=7, pet_photo='images/photo_1.jpeg'):
    """Проверяем возможность добавления питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа и результат добавления питомца по name
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_valid_key_no_name(name='', animal_type='кошка', age=7, pet_photo='images/photo_1.jpeg'):
    """Проверяем возможность добавления питомца с корректными данными, но без указания имени"""
    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа
    assert status != 200


"""Здесь баг, так как питомец без имени добавляться не должен, но он успешно добавился"""


def test_add_new_pet_with_valid_key_no_animal_type(name='Карамбуленька', animal_type='', age=7, pet_photo='images/photo_1.jpeg'):
    """Проверяем возможность добавления питомца с корректными данными, но без указания породы"""
    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа
    assert status != 200


"""Здесь баг, так как питомец без породы добавляться не должен, но он успешно добавился"""


def test_add_new_pet_with_valid_key_no_age(name='Карамбулочка', animal_type='кошка', age='', pet_photo='images/photo_1.jpeg'):
    """Проверяем возможность добавления питомца с корректными данными, но без указания возраста"""
    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа
    assert status != 200


"""Здесь баг, так как питомец без возраста добавляться не должен, но он успешно добавился"""


def test_add_new_pet_with_valid_key_wrong_age_type(name='Карамба-малышка', animal_type='кошка', age='Два месяца и 5 дней', pet_photo='images/photo_1.jpeg'):
    """Проверяем возможность добавления питомца с корректными данными, но с указанием возраста в текстовом формате"""
    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа
    assert status != 200


"""Здесь баг, так как поле для указания возраста должно содержать только число, """
"""но питомец добавился с возрастом, указанном в текстовом формате"""


def test_add_new_pet_with_valid_key_wrong_image_format(name='Карамбусечка', animal_type='кошка', age=7, pet_photo='images/logo.svg'):
    """Проверяем возможность добавления питомца с некорректным форматом изображения"""
    # Получаем полный путь изображения питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Проверяем статус ответа
    assert status == 403


"""Здесь баг - питомец не должен добавляться с фотографией в формате .svg, но он был успешно создан (только без фото)"""


def test_successful_delete_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", 3, "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet_info(name='Карамба', animal_type='булочка-курочка', age=9):
    """Проверяем возможность обновления информации о питомце по ID"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        # Проверяем, есть ли питомцы в нашем списке и если да, то выполняем обновление данных по указанному ID
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        # Если питомцев нет в списке, вызываем исключение
        raise Exception("There is no my pets")


def test_update_pet_info_with_wrong_data(name=123467, animal_type=908576463, age=-1000):
    """Проверяем возможность обновления информации о питомце по ID"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        # Проверяем, есть ли питомцы в нашем списке и если да, то выполняем обновление данных по указанному ID
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status != 200
    else:
        # Если питомцев нет в списке, вызываем исключение
        raise Exception("There is no my pets")


"""Баг - допускаются цифры в имени и породе питомца так же, как и отрицательный возраст"""


def test_set_pet_photo():
    """Проверяем возможность добавления/замены фотографии питомца по ID"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        # Проверяем, есть ли питомцы в нашем списке и если да, то задаем новое фото питомца по указанному ID
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], "images/cat_2.jpg")
        assert status == 200
    else:
        # Если питомцев нет в списке, вызываем исключение
        raise Exception("There is no my pets for updating photo")


def test_set_pet_photo_with_wrong_file_format():
    """Проверяем возможность добавления/замены фотографии питомца по ID с некорректным форматом файла"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        # Проверяем, есть ли питомцы в нашем списке и если да, то задаем новое фото некорректного формата для питомца по указанному ID
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], "images/capologo.pdf")
        assert status != 200
    else:
        # Если питомцев нет в списке, вызываем исключение
        raise Exception("There is no my pets for updating photo")


def test_add_pet_without_photo(name="Дымок", animal_type="котёнок", age=0):
    """Проверяем возможность добавления информации о питомцае без фото"""
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_pet_without_photo_with_wrong_args(name="Дымок", animal_type="котёнок", age=0, pet_photo='images/cat_2.jpg'):
    """Проверяем возможность добавления информации о питомцае без фото"""
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Вызываем исключение при добавлении питомца с некорректным количеством аргументов
    with pytest.raises(TypeError):
        status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age, pet_photo)
