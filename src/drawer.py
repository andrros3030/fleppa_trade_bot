import io
import matplotlib.pyplot as plt


# функция которая возвращает изображение, которое потом можно отправить сообщением
def get_plot(x, y):
    my_stringIObytes = io.BytesIO()  # объект, который хранит данные изображения
    plt.plot(x, y)  # строим по x'ам и y'кам график
    plt.savefig(my_stringIObytes, format='jpg')  # сохраняем изображение графика в my_stringIObytes в формате jpg
    my_stringIObytes.seek(0)  # не знаю че такое, наверное что-то важное
    return my_stringIObytes  # возвращаем объект хранящий изображение
