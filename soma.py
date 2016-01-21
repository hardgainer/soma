from functools import reduce
from pprint import pprint
from time import ctime,time
from sys import exit,stderr
from collections import OrderedDict
import argparse

# фигуры сома
# описываются как кортеж занимаемых в пространстве точек (x,y,z)
fp = ((0,0,0), (1,0,0), (0,1,0), (0,0,1))
fa = ((0,0,0), (1,0,0), (0,1,0), (1,0,1))
fb = ((0,0,0), (1,0,1), (0,1,0), (0,0,1))
fv = ((0,0,0), (1,0,0), (0,1,0))
fl = ((0,0,0), (1,0,0), (2,0,0), (0,1,0))
ft = ((0,0,0), (1,0,0), (2,0,0), (1,1,0))
fz = ((0,0,0), (1,0,0), (1,1,0), (2,1,0))

def gen_cube(n):
    "Создаем заполняемое пространство - куб со стороной n"
    space = []
    for p in traverse(n):
        space.append(p)
    return space

def traverse(n):
    "Вспомогательная функция для обхода куба со стороной n"
    for z in range(n):
        for y in range(n):
            for x in range(n):
                yield (x,y,z)

def move(fig, offset):
    "Сдвиг фигуры на заданное смещение в виде (x,y,z)"
    new_fig = ()
    for elem in fig:
        #print(elem)
        #nx = elem[0] + offset[0]
        #ny = elem[1] + offset[1]
        #nz = elem[2] + offset[2]
        #new_fig += (nx, ny, nz),
        new_fig += tuple(map(sum, zip(elem, offset))),
    return new_fig

def rx(fig):
    " Поворот фигуры вокруг оси X на 90°: (x,y,z) -> (x,z,-y) "
    return tuple(map(lambda e : (e[0],e[2],-e[1]), fig))

def ry(fig):
    " Поворот фигуры вокруг оси Y на 90°: (x,y,z) -> (z,y,-x) "
    return tuple(map(lambda e : (e[2],e[1],-e[0]), fig))

def rz(fig):
    " Поворот фигуры вокруг оси Z на 90°: (x,y,z) -> (-y,x,z) "
    return tuple(map(lambda e : (-e[1],e[0],e[2]), fig))

# список преобразований для получения всех 24 ориентаций фигуры
# сначала каждую из 6 граней ставим перпендикулярно оси Y
# каждую из этих позиций поворачиваем еще 3 раза вокруг оси Y
def gen_rotations_24(fig):
    facets = [fig]
    for turn in ((rx,),(rx,rx,),(rx,rx,rx,),(rz,),(rz,rz,rz,)):
        pos = reduce(lambda x,y : y(x), turn, fig)
        facets.append(pos)
    f_pos = []
    for facet in facets:
        f_pos.append(facet)
        for turn in ((ry,),(ry,ry,),(ry,ry,ry,)):
            pos = reduce(lambda x,y : y(x), turn, facet)
            f_pos.append(pos)
    return f_pos

def is_figure_in_space(fig, space):
    "Возвращает True, если все точки фигуры входят в заданное пространство"
    # если есть хоть одна точка в генерируемом списке, то не входит
    return 0 == len([e for e in fig if not e in space])

def gen_valid_positions(fig, space):
    "Получение списка всех возможных позиций фигуры в заданном пространстве"
    f_pos = []
    for point in space:
        new_fig = move(fig, point)
        if is_figure_in_space(new_fig, space):
            f_pos.append(new_fig)
    return f_pos

def gen_all_positions(fig, space):
    "Получение списка всех возможных позиций с учетом ориентации"
    f_all = []
    for pp in gen_rotations_24(fig):
        f_all.extend(gen_valid_positions(pp, space))
    return f_all

def gen_coord_bin_dict(space):
    "Словарь для преобразования трехмерных координат в биты по заданному пространству"
    shift = 0
    coord_to_bin = {}
    for p in space:
        # print(p, '<-', bin(1<<shift))
        coord_to_bin[p] = 1 << shift
        shift += 1
    return coord_to_bin

def gen_bin_coord_dict(space):
    "Словарь для преобразования из бит в трехмерные координаты"
    shift = 0
    bin_to_coord = {}
    for p in space:
        # print(p, '<-', bin(1<<shift))
        bin_to_coord[1 << shift] = p
        shift += 1
    return bin_to_coord

def figures_to_bin(figures, dct):
    "Генерирует список чисел (битовых масок) из списка позиций фигуры"
    bin_pos = []
    for fig in figures:
        # складываем все битовые маски в одно число
        bin_pos.append(reduce(lambda x,y: x+y, [dct[elem] for elem in fig]))
    return list(set(bin_pos))

def dump_figure_bins(bins, filename):
    "Сохраняет список чисел-положений в указанный файл"
    out = open(filename, 'w')
    for n in bins:
        if n >= 2**63:
            n -= 2**64
        print('%d,' % n, file=out)
    out.close()

def enter_n_points(n):
    """Ввод n-точечной фигуры в виде триплетов 'xyz'"""
    prompt = 'Введите фигуру (%d точек через запятую): '
    points = []
    while len(points) < n:
        s = input(prompt % (n - len(points)))
        pts = [x.strip() for x in s.split(',') if len(x) > 0]   # обрезаем и удаляем пустые
        points.extend([x for x in pts if len(x) == 3])          # оставляем только триплеты
        for x in points:
            for i in range(3):
                if not x[i] in '0123456789':
                    points.remove(x)          # оставляем только цифры
                    break
        # points = list(set(points))      # оставляем только уникальные
        points = list(OrderedDict.fromkeys(points))      # оставляем только уникальные
        print('Вы ввели: %s' %  points)
        prompt = 'Введите ещё %d точек: '
    return points

def load_figure():
    "Загрузка фигуры из файла или куб по умолчанию"
    ans = input('Загрузить фигуру из файла ([yes]/no - для куба 3x3x3)?: ')
    if (len(ans) > 0 and ans.lower()[0] == 'n'):
        print('Выбран куб 3x3x3.')
        fig = gen_cube(3)
        return fig
    figs = {}
    for l in open('figures.txt').readlines():
        (name, data) = l.split(':')[:2]
        figs[name] = data.strip()
    ans = input('Введите название фигуры: ')
    if not ans in figs:
        print('Фигура не найдена.')
        return None
    print(figs[ans])
    ps = [x.strip() for x in figs[ans].split(',')]
    fig= [(int(x[0]),int(x[1]),int(x[2])) for x in ps]
    if len(fig) != 27:
        print('Фигура задана неправильно.')
        return None
    return fig

################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Поиск решения для SOMA-фигур.",
            epilog="По умолчанию работает в режиме поиска решения и проверки.")
    parser.add_argument("-i", "--input", action="store_true", help="ввести фигуру интерактивно")
    parser.add_argument("-o", "--output", action="store_true", help="сохранить наборы положений фигурок в файлы")
    parser.add_argument("-s", "--solve", action="store_true", help="искать решение")
    parser.add_argument("-c", "--check", nargs='?', const='sols_py.log', metavar='solutions_file', help="проверить решение")
    args = parser.parse_args()
    if not (args.input or args.output or args.solve or args.check):     # если ничего не задано
        args.solve = True
        args.check = 'sols_py.log'

    figure = None
    order = ['v','t','l','z','p','a','b']
    if args.input:
        ps = enter_n_points(27)
        figure = [(int(x[0]),int(x[1]),int(x[2])) for x in ps]
        ans = input('Сохранить фигуру ([yes]/no): ')
        if len(ans) == 0 or (len(ans) > 0 and ans.lower()[0] == 'y'):
            ans = input('Введите название фигуры: ')
            file_fig = open('figures.txt', 'a')
            fig_data = '%s: ' % ans + ','.join(ps) + '\n'
            file_fig.write(fig_data)
            file_fig.close()

    if args.solve:
        if not figure: figure = load_figure()   # если не была введена вручную
        if not figure: exit(1)

        coord_bin = gen_coord_bin_dict(figure)
        # f_all_bin = figures_to_bin(f_all, coord_bin)
        # for fig in f_all_bin: print(bin(fig))
        all = [figures_to_bin(gen_all_positions(f, figure), coord_bin) for f in [fv, ft, fl, fz, fp, fa, fb]]
        # print(len(all))
        lens = [len(x) for x in all]
        print(lens)
        num_variants = reduce(lambda x,y: x*y, lens)
        print('Число комбинаций: %.1f миллиардов\n' % ((num_variants/1e9), ))

        # сохраняем списки чисел-положений фигур в файлы
        if args.output:
            dump_figure_bins(all[0], 'fig_v')
            dump_figure_bins(all[1], 'fig_t')
            dump_figure_bins(all[2], 'fig_l')
            dump_figure_bins(all[3], 'fig_z')
            dump_figure_bins(all[4], 'fig_p')
            dump_figure_bins(all[5], 'fig_a')
            dump_figure_bins(all[6], 'fig_b')

        # решаем
        solutions = []
        fsol = open('sols_py.log', 'w')
        start_time = int(time())
        for i0 in range(lens[0]):
            print('%s%%  \r' % (100*i0//lens[0]), file=stderr, end='')
            f0 = all[0][i0]
            fs0 = f0        # filled space
            for i1 in range(lens[1]):
                f1 = all[1][i1]
                if f1 & fs0 != 0: continue
                fs1 = f1 ^ fs0
                for i2 in range(lens[2]):
                    f2 = all[2][i2]
                    if f2 & fs1 != 0: continue
                    fs2 = f2 ^ fs1
                    for i3 in range(lens[3]):
                        f3 = all[3][i3]
                        if f3 & fs2 != 0: continue
                        fs3 = f3 ^ fs2
                        for i4 in range(lens[4]):
                            f4 = all[4][i4]
                            if f4 & fs3 != 0: continue
                            fs4 = f4 ^ fs3
                            for i5 in range(lens[5]):
                                f5 = all[5][i5]
                                if f5 & fs4 != 0: continue
                                fs5 = f5 ^ fs4
                                for i6 in range(lens[6]):
                                    f6 = all[6][i6]
                                    if f6 & fs5 != 0: continue
                                    if f6 ^ fs5 == 2**27-1:
                                        sol = (f0,f1,f2,f3,f4,f5,f6)
                                        solutions.append(sol)
                                        print(','.join(map(str, sol)), file=fsol)   # печать чисел без скобок
        fsol.close()
        print('Найдено %d решений. %d секунд затрачено.' % (len(solutions), int(time() - start_time)))
        if len(solutions) == 0: exit(0)

    if args.check:
        if not figure: figure = load_figure()
        if not figure: exit(1)
        # проверяем решение
        if not args.solve:
            # проверяем решение из файла
            solutions = []
            for s in open(args.check).readlines():
                sol = tuple(map(int, s.split(',')))
                solutions.append(sol)
            print('Прочитано %d решений.' % len(solutions))

        bin_coord = gen_bin_coord_dict(figure)
        while True:
            while True:
                ans = input('Введите номер решения (ENTER для завершения): ')
                if len(ans) == 0: exit(0)
                try:
                    sol_num = int(ans)
                    if sol_num > len(solutions):
                        print('Слишком большой номер.')
                        continue
                    if sol_num <= 0:
                        print('Номер должен быть положительным.')
                        continue
                    break
                except: pass

            sol = solutions[sol_num-1]
            fig_num = 0
            for n in sol:
                solution = []
                for i in range(27):
                    if (1<<i) & n != 0:
                        solution.append(bin_coord[1<<i])
                print('%s %28s  ' % (order[fig_num], format(n,'b')), end='')
                print(solution)
                fig_num += 1
