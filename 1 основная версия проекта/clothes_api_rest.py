from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json


# Этот код представляет собой простой RESTful API на Flask для работы с данными о товарах и изображениями товаров.

# Импортируются необходимые модули и классы, такие как Flask, jsonify для работы с JSON, и Api, Resource из Flask-RESTful для создания API.
# Создается экземпляр приложения Flask и API.
# Считываются данные о товарах из файла JSON clothes.json и сохраняются в переменной data.
# Определяется класс ClothesList, который наследуется от Resource и содержит методы get() и post(). Метод get() возвращает список товаров в формате JSON, а метод post() добавляет новый товар, полученный из запроса JSON, в список и сохраняет обновленные данные в файл JSON.
# Определяется класс Image, который также наследуется от Resource и содержит метод get(image_id). Этот метод возвращает изображение товара по его идентификатору, если такой товар найден в данных. В противном случае возвращается сообщение о том, что изображение не найдено.
# Устанавливаются URL-маршруты для классов ClothesList и Image.
# Если данный файл запускается напрямую (а не импортируется), выполняется запуск приложения Flask в режиме отладки.


app = Flask(__name__)
api = Api(app)

# Считываем данные о товарах из файла JSON
with open("clothes.json", "r") as file:
    data = json.load(file)

class ClothesList(Resource):
    def get(self):
        return jsonify(data)

    def post(self):
        new_item = request.json
        data.append(new_item)
        with open("clothes.json", "w") as file:
            json.dump(data, file, indent=4)
        return jsonify(new_item), 201

class Image(Resource):
    def get(self, image_id):
        image = next((item for item in data if item["id"] == image_id), None)
        if image:
            return image["img"]
        else:
            return "Изображение не найдено", 404

# URL-маршруты
api.add_resource(ClothesList, "/clothes")
api.add_resource(Image, "/image/<int:image_id>")

if __name__ == "__main__":
    app.run(debug=True)

