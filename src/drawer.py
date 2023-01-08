import io
import matplotlib.pyplot as plt


def get_plot(x, y):
    my_stringIObytes = io.BytesIO()
    plt.plot(x, y)
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return my_stringIObytes
