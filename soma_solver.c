#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>
#include <semaphore.h>
#include "nums_from_file.h"

typedef struct solve_param_t
{
	int v_num;
	int num_solutions;
} solve_param_t;

dyn_array_int_t fig_a, fig_b, fig_l, fig_p, fig_t, fig_v, fig_z;
FILE *fout;
pthread_mutex_t mutex;

void *solve(void* in)
{
	solve_param_t *pparm = in;
	const long solution = (1<<27)-1;
	int i0 = pparm->v_num;

	long fs0 = fig_v.vals[i0];		// fs - filled space
	for (int i1=0; i1 < fig_t.size; i1++)
	{
		if (fig_t.vals[i1] & fs0) continue;
		long fs1 = fig_t.vals[i1] ^ fs0;
		for (int i2=0; i2 < fig_l.size; i2++)
		{
			if (fig_l.vals[i2] & fs1) continue;
			long fs2 = fig_l.vals[i2] ^ fs1;
			for (int i3=0; i3 < fig_z.size; i3++)
			{
				if (fig_z.vals[i3] & fs2) continue;
				long fs3 = fig_z.vals[i3] ^ fs2;
				for (int i4=0; i4 < fig_p.size; i4++)
				{
					if (fig_p.vals[i4] & fs3) continue;
					long fs4 = fig_p.vals[i4] ^ fs3;
					for (int i5=0; i5 < fig_a.size; i5++)
					{
						if (fig_a.vals[i5] & fs4) continue;
						long fs5 = fig_a.vals[i5] ^ fs4;
						for (int i6=0; i6 < fig_b.size; i6++)
						{
							if (fig_b.vals[i6] & fs5) continue;
							long fs6 = fig_b.vals[i6] ^ fs5;
							if (fs6 == solution)
							{
								pthread_mutex_lock(&mutex);
								fprintf(stderr, "(%d) Solution #%d\n", i0, ++(pparm->num_solutions));
								fprintf(fout, "%d,%d,%d,%d,%d,%d,%d\n", \
										fig_v.vals[i0],fig_t.vals[i1],fig_l.vals[i2],fig_z.vals[i3],fig_p.vals[i4],fig_a.vals[i5],fig_b.vals[i6]);
								fflush(fout);
								pthread_mutex_unlock(&mutex);
							}
						}
					}
				}
			}
		}
	}
	pthread_exit(NULL);
}

// порядок обхода фигур: v,t,l,z,p,a,b
int main()
{
	fout = fopen("sols.log", "w");
	if (!fout)
	{
		perror("can't open file");
		exit(EXIT_FAILURE);
	}

	fig_v = nums_from_file("fig_v");
	fig_t = nums_from_file("fig_t");
	fig_l = nums_from_file("fig_l");
	fig_z = nums_from_file("fig_z");
	fig_p = nums_from_file("fig_p");
	fig_a = nums_from_file("fig_a");
	fig_b = nums_from_file("fig_b");

	if (0 == (fig_v.size + fig_t.size + fig_l.size + fig_z.size + fig_p.size + fig_a.size + fig_b.size))
	{
		perror("input data error");
		exit(EXIT_FAILURE);
	}

	printf("%d %d %d %d %d %d %d\n", fig_v.size, fig_t.size, fig_l.size, fig_z.size, fig_p.size, fig_a.size, fig_b.size);

	pthread_mutex_init(&mutex, NULL);
	pthread_t thr[fig_v.size];
	solve_param_t sol_params[fig_v.size];

	for (int i = 0; i < fig_v.size; i++)
	{
		sol_params[i].v_num = i;
		sol_params[i].num_solutions = 0;
		pthread_create(&thr[i], NULL, solve, &sol_params[i]);
	}

	int total_solutions = 0;
	for (int i = 0; i < fig_v.size; i++)
	{
		pthread_join(thr[i], NULL);
		total_solutions += sol_params[i].num_solutions;
	}

	pthread_mutex_destroy(&mutex);
	fclose(fout);
	printf("Total solutions: %d\n", total_solutions);

	deinit_dyn_array(&fig_v);
	deinit_dyn_array(&fig_t);
	deinit_dyn_array(&fig_l);
	deinit_dyn_array(&fig_z);
	deinit_dyn_array(&fig_p);
	deinit_dyn_array(&fig_a);
	deinit_dyn_array(&fig_b);
	return 0;
}

