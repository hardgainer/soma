from sys import exit
from soma import *

# фигуры галакуба
# описываются как кортеж занимаемых в пространстве точек (x,y,z)
fq1 = ((0,0,0), (1,0,0), (0,0,1), (1,0,1), (0,1,0), (1,1,0), (0,1,1), (1,1,1))
fq2 = ((0,0,0), (1,0,0), (0,0,1), (1,0,1), (0,1,0), (1,1,0), (0,1,1), (1,1,1))
fz1 = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,1), (2,0,1), (1,0,2), (2,0,2))
fz2 = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,1), (2,0,1), (1,0,2), (2,0,2))
fz3 = ((0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,1), (2,0,1), (1,0,2), (2,0,2))
fj1 = ((0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,0,1), (1,0,1), (0,0,2), (1,0,2))
fj2 = ((0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,0,1), (1,0,1), (0,0,2), (1,0,2))
fj3 = ((0,0,0), (1,0,0), (0,1,0), (1,1,0), (0,0,1), (1,0,1), (0,0,2), (1,0,2))

def print_figure_cutting(fig):
    """ Послойная печать фигуры в пространстве 4x4x4.
      y[0]:  y[1]:  y[2]:  y[3]:
    | 0123   0123   0123   0123  --> X
    | 1
    v 2
    Z 3
    """
    for z in range(4):
        for y in range(4):
            for x in range(4):
                if (x,y,z) in fig: print('#', end='')
                else: print('.', end='')
            print('  ', end='')
        print()

if __name__ == '__main__':
    cube = gen_cube(4)

    coord_bin = gen_coord_bin_dict(cube)
    all = [figures_to_bin(gen_all_positions(f, cube), coord_bin) for f in [fq1, fq2, fz1, fz2, fz3, fj1, fj2, fj3]]
    lens = [len(x) for x in all]
    print(lens)
    num_variants = reduce(lambda x,y: x*y, lens)
    print('Число комбинаций: %.1f триллионов\n' % ((num_variants/1e12), ))

    # сохраняем списки чисел-положений фигур в файлы
    dump_figure_bins(all[0], 'gala_q1')
    dump_figure_bins(all[1], 'gala_q2')
    dump_figure_bins(all[2], 'gala_z1')
    dump_figure_bins(all[3], 'gala_z2')
    dump_figure_bins(all[4], 'gala_z3')
    dump_figure_bins(all[5], 'gala_j1')
    dump_figure_bins(all[6], 'gala_j2')
    dump_figure_bins(all[7], 'gala_j3')

    # проверяем решение
    bin_coord = gen_bin_coord_dict(cube)
    sols = []
    for l in open('sols_galacube.log').readlines():
        sol = set(l.strip().split(','))
        # оставляем только уникальные решения, поскольку есть одинаковые фигурки
        if not sol in sols:
            sols.append(sol)
            # print(sol)

    for i in range(len(sols)):
        print('Solution %d' % (i+1))
        fig_num = 1
        for sn in sols[i]:
            n = int(sn)
            figure = []
            for i in range(64):
                if (1<<i) & n != 0:
                    figure.append(bin_coord[1<<i])
            print("Figure #%d: %s" % (fig_num, figure))
            print_figure_cutting(figure)
            print()
            fig_num += 1
