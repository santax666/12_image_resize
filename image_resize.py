import os
import argparse
from PIL import Image


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


def arguments_checking(width, height, scale, size):
    MIN_VALUE = 0
    arguments_names = ('ширины', 'высоты', 'масштаба',)
    error_texts = ('Ширина и Высота не могут быть указаны вместе с Масштабом!',
                   'Значение {0} не может быть меньше или равным нулю!',
                   'Не соблюдены пропорции! Изображение будет искажено!',)
    for argument_num, argument in enumerate((width, height, scale)):
        if argument is not None:
            if argument <= MIN_VALUE:
                print(error_texts[1].format(arguments_names[argument_num]))
                return
    if scale is None:
        if width is None:
            return int(size[0] * height / size[1]), height
        elif height is None:
            return width, int(size[1] * width / size[0])
        else:
            if width / size[0] != height / size[1]:
                print(error_texts[2])
            return width, height
    else:
        if (width or height) is not None:
            print(error_texts[0])
        else:
            return int(scale * size[0]), int(scale * size[1])


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

    if (width or height or scale) is None:
        print('Не задан ни один из обязательных параметров!')
    else:
        image = Image.open(input_file)
        out_sides = arguments_checking(width, height, scale, image.size)
        if out_sides is not None:
            if out_file is None:
                out_file = create_output_name(input_file, out_sides)
            resize_image(image, out_sides, out_file)
            print('Преобразование изображения завершено.')
        else:
            print('Преобразование невозможно из-за некорректных данных.')
