from functools import reduce
from pprint import pprint
from time import ctime,time
from sys import exit

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
    "Сохраняет список чисел-положений в указанный файл (без расширения) (C-формат)"
    out = open(filename, 'w')
    for n in bins:
        print('%s,' % n, file=out)
    out.close()

if __name__ == '__main__':
    #cube = gen_cube(3)
    cube = [
            # фигура №8
            (0,0,0),(0,0,1),(1,0,0),(1,0,1),
            (0,1,0),(0,1,1),(1,1,0),(1,1,1),
            (0,2,0),(0,2,1),(1,2,0),(1,2,1),
            (0,3,0),(0,3,1),(1,3,0),(1,3,1),
            (0,4,0),(0,4,1),(1,4,0),(1,4,1),
            (0,5,0),(0,5,1),(1,5,0),(1,5,1),
            (0,6,0),(0,6,1),(1,6,0)
            # фигура №24 - нет решения ?
            #(2,0,0),(1,0,1),(2,0,1),(3,0,1),
            #(0,0,2),(1,0,2),(2,0,2),(3,0,2),(4,0,2),
            #(2,0,4),(1,0,3),(2,0,3),(3,0,3),
            #(2,1,0),(1,1,1),(2,1,1),(3,1,1),
            #(0,1,2),(1,1,2),(2,1,2),(3,1,2),(4,1,2),
            #(2,1,4),(1,1,3),(2,1,3),(3,1,3),
            #(2,2,2)
            # фигура №29 - нет решения ?
            #(0,0,0),(0,0,1),(1,0,0),(1,0,1),(2,0,0),(2,0,1),(2,0,2),(1,0,2),(0,0,2),
            #(0,1,0),(0,1,1),(1,1,0),(1,1,1),
            #(0,2,0),(0,2,1),(1,2,0),(1,2,1),
            #(0,3,0),(0,3,1),(1,3,0),(1,3,1),
            #(0,4,0),(0,4,1),(1,4,0),(1,4,1),
            #(0,5,0),(0,6,0)
            # фигура №33 - нет решения ?
            #(2,0,0),(3,0,0),(4,0,0),(2,0,1),
            #(0,0,2),(1,0,2),(2,0,2),(0,0,3),(0,0,4),
            #(2,1,0),(3,1,0),(4,1,0),(2,1,1),
            #(0,1,2),(1,1,2),(2,1,2),(0,1,3),(0,1,4),
            #(2,2,0),(3,2,0),(4,2,0),(2,2,1),
            #(0,2,2),(1,2,2),(2,2,2),(0,2,3),(0,2,4),
            ]
    #print(cube)
    if len(set(cube)) != 27:
        print('Фигура задана неправильно!')
        exit(1)

    coord_bin = gen_coord_bin_dict(cube)
    # f_all_bin = figures_to_bin(f_all, coord_bin)
    # for fig in f_all_bin: print(bin(fig))
    all = [figures_to_bin(gen_all_positions(f, cube), coord_bin) for f in [fv, ft, fl, fz, fp, fa, fb]]
    # print(len(all))
    lens = [len(x) for x in all]
    print(lens)
    num_variants = reduce(lambda x,y: x*y, lens)
    print('Число комбинаций: %.1f миллиардов\n' % ((num_variants/1e9), ))

    # сохраняем списки чисел-положений фигур в файлы
    dump_figure_bins(all[0], 'fig_v')
    dump_figure_bins(all[1], 'fig_t')
    dump_figure_bins(all[2], 'fig_l')
    dump_figure_bins(all[3], 'fig_z')
    dump_figure_bins(all[4], 'fig_p')
    dump_figure_bins(all[5], 'fig_a')
    dump_figure_bins(all[6], 'fig_b')

    # проверяем решение
    bin_coord = gen_bin_coord_dict(cube)
    order = ['v','t','l','z','p','a','b']
    sol = [
        #16420,263681,131520,100761600,9963520,4122,23076864
        #5632,23330816,131520,100761600,9963520,16422,8217
        #4609,23330816,456,100761600,9963520,155664,1062
        #4609,23330816,456,100761600,9963520,9222,147504
        #4609,23330816,33216,147492,9963520,100737024,1050
        #16420,263681,67240320,33652800,9963520,4122,23076864
        #5632,1067012,456,51,52461568,75694080,4988928,
        172032,4880,345088,2210,77,121634816,12058624
    ]
    fig_num = 0
    for n in sol:
        figure = []
        for i in range(27):
            if (1<<i) & n != 0:
                figure.append(bin_coord[1<<i])
        print('%s %28s  ' % (order[fig_num], format(n,'b')), end='')
        print(figure)
        fig_num += 1
    exit(0)

    # решаем
    # этот алгоритм решает примерно 1 млн комбинаций в секунду (нужно ~63e6 секунд)
    num_solves = 0
    start_time = int(time())
    for i0 in range(lens[0]):
        f0 = all[0][i0]
        for i1 in range(lens[1]):
            f1 = all[1][i1]
            if f1 & f0 != 0: continue
            for i2 in range(lens[2]):
                f2 = all[2][i2]
                if f2 & f1 != 0: continue
                for i3 in range(lens[3]):
                    f3 = all[3][i3]
                    if f3 & f2 != 0: continue
                    for i4 in range(lens[4]):
                        f4 = all[4][i4]
                        if f4 & f3 != 0: continue
                        for i5 in range(lens[5]):
                            f5 = all[5][i5]
                            if f5 & f4 != 0: continue
                            for i6 in range(lens[6]):
                                f6 = all[6][i6]
                                if f6 & f5 != 0: continue
                                if f0+f1+f2+f3+f4+f5+f6 == 2^27-1:
                                    num_solves += 1
                                    print("Solve #%s:" % num_solves)
                                    print("%30s" % format(f0,'b'))
                                    print("%30s" % format(f1,'b'))
                                    print("%30s" % format(f2,'b'))
                                    print("%30s" % format(f3,'b'))
                                    print("%30s" % format(f4,'b'))
                                    print("%30s" % format(f5,'b'))
                                    print("%30s" % format(f6,'b'))
                                cnt = 1+i6+i5*lens[6]+i4*lens[6]*lens[5]+i3*lens[6]*lens[5]*lens[4]+i2*lens[6]*lens[5]*lens[4]*lens[3]+i1*lens[6]*lens[5]*lens[4]*lens[3]*lens[2]+i0*lens[6]*lens[5]*lens[4]*lens[3]*lens[2]*lens[1]
                                # elapsed = int(time()) - start_time
                                # if elapse % 100 == 0:
                print(ctime()[10:20], i0, i1, i2, i3, i4, i5, i6, cnt)

    # ищем и убираем повторяющиеся позиции
    # ll = [set(pos_f[0])]
    # print(ll)
    # for pos in pos_f[1:]:
        # poss = set(pos)
        # if not poss in ll:
            # ll.append(poss)
    # pprint(ll)
    # print(len(ll))

