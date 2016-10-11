import os
import argparse
from PIL import Image


param_names = ('ширины', 'высоты', 'масштаба',)


def create_parser():
    parser = argparse.ArgumentParser(usage='%(prog)s [аргументы]',
                                     description='Изменение размера картинок'
                                                 ' с помощью %(prog)s')
    parser.add_argument('image', help='Изображение для обработки')
    parser.add_argument('-W', '--width', type=int, help='Ширина изображения')
    parser.add_argument('-H', '--height', type=int, help='Высота изображения')
    parser.add_argument('-S', '--scale', type=float, help='Масштаб')
    parser.add_argument('-O', '--out', help='Выходной файл')
    return parser


def calculate_scale_list(params, image_size):
    scale_list = []
    for side_num, side in enumerate(image_size):
        if params[side_num] is not None:
            scale_list.append(params[side_num]/side)
        else:
            scale_list.append(None)
    scale_list.append(params[2])
    return scale_list


def arguments_checking(params, image_size):
    error_texts = ('Ширина и Высота не могут быть указаны вместе с Масштабом!',
                   'Значение {0} не может быть меньше или равным нулю!',
                   'Значение {0} очень большое: картинка будет расплывчатой!',
                   'Не соблюдены пропорции! Изображение будет искажено!',)

    if ((params[0] or params[1]) and params[2]) is not None:
        print(error_texts[0])
        return

    for param_num, param in enumerate(params):
        if param is not None:
            if (param <= 0):
                print(error_texts[1].format(param_names[param_num]))
                return

    scale_list = calculate_scale_list(params, image_size)
    for scale_num, scale in enumerate(scale_list):
        if (scale is not None) and (scale > 5):
            print(error_texts[2].format(param_names[scale_num]))
            return

    if (scale_list[0] and scale_list[1]) is not None:
        if scale_list[0] != scale_list[1]:
            print(error_texts[3])
    return scale_list


def input_image_params():
    params = []
    message_input = ('Выполнить изменение картинки через (0 - Ширину; '
                     '1 - Высоту; 2 - Масштаб; 3 - Ширину/Высоту): ',
                     'Значение дожно быть {0,1,2,3}, повторите ввод: ',
                     'Введите значение {0}: ',
                     'Число должно быть целым, повторите ввод: ',
                     'Число должно быть вещественным!',)

    type_resize = input(message_input[0])
    while not int(type_resize) in (0, 1, 2, 3):
        type_resize = input(message_input[1])
    type_resize = int(type_resize)

    if type_resize == 3:
        for number in (0, 1,):
            value = input(message_input[2].format(param_names[number]))
            while not value.isdecimal():
                value = input(message_input[3])
            params.append(int(value))
        params.append(None)
    elif type_resize == 2:
        while True:
            try:
                value = float(input(message_input[2].format(param_names[2])))
            except ValueError:
                print(message_input[4])
            else:
                break
        params = [None, None, value]
    else:
        value = input(message_input[2].format(param_names[type_resize]))
        while not value.isdecimal():
            value = input(message_input[3])
        if type_resize == 0:
            params = [int(value), None, None]
        else:
            params = [None, int(value), None]
    return params


def calculate_resized_sides(scale_list, image_size):
    if scale_list[2] is None:
        if (scale_list[0] and scale_list[1]) is None:
            if scale_list[0] is None:
                width = scale_list[1] * image_size[0]
                height = scale_list[1] * image_size[1]
            else:
                width = scale_list[0] * image_size[0]
                height = scale_list[0] * image_size[1]
        else:
            width = scale_list[0] * image_size[0]
            height = scale_list[1] * image_size[1]
    else:
        width = scale_list[2] * image_size[0]
        height = scale_list[2] * image_size[1]
    return int(width), int(height)


def create_output_name(path_file, sides):
    name_file = os.path.splitext(path_file)
    out_file = '{0}__{1}x{2}{3}'.format(name_file[0], sides[0],
                                        sides[1], name_file[1])
    return out_file


def resize_image(image, sides, file_to_result):
    resized_img = image.resize((sides[0], sides[1]), Image.ANTIALIAS)
    resized_img.save(file_to_result)


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    input_file = namespace.image
    width = namespace.width
    height = namespace.height
    scale = namespace.scale
    out_file = namespace.out

    image = Image.open(input_file)

    if (width or height or scale) is None:
        params = input_image_params()
    else:
        params = (width, height, scale,)
    scale_list = arguments_checking(params, image.size)
    if scale_list is not None:
        values_of_sides = calculate_resized_sides(scale_list, image.size)
        if out_file is None:
            out_file = create_output_name(input_file, values_of_sides)
        resize_image(image, values_of_sides, out_file)
        print('Преобразование изображения завершено.')
    else:
        print('Преобразование невозможно из-за некорректных данных.')
