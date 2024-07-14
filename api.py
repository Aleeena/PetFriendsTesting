import requests
import json


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
                JSON с уникальным ключем пользователя, найденного по указанным email и паролю"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
                со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
                либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
                собственных питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def add_new_pet(self, auth_key, name, animal_type, age: int, pet_photo):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key, pet_id):
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении."""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key, pet_id, name, animal_type, age: int):
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def set_pet_photo(self, auth_key, pet_id, pet_photo):
        """Метод отправляет на сервер запрос на размещение фото питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном размещении фото."""

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_without_photo(self, auth_key, name, animal_type, age: int):
        """Метод отправляет (постит) на сервер данные о добавляемом питомце без фото и возвращает статус
                        запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
