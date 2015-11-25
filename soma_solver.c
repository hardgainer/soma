// gcc -O2 -Wall -std=c99 -o soma *.c && ./soma
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>
#include <semaphore.h>

typedef struct solve_param_t
{
	int v_num;
	int num_solutions;
} solve_param_t;

extern const int fig_a[], size_fig_a;
extern const int fig_b[], size_fig_b;
extern const int fig_l[], size_fig_l;
extern const int fig_p[], size_fig_p;
extern const int fig_t[], size_fig_t;
extern const int fig_v[], size_fig_v;
extern const int fig_z[], size_fig_z;
FILE *fout;
pthread_mutex_t mutex;

void *solve(void* in)
{
	solve_param_t *pparm = in;
	const int solution = (1<<27)-1;
	int i0 = pparm->v_num;

	for (int i1=0; i1 < size_fig_t; i1++)
	{
		if (fig_t[i1] & fig_v[i0]) continue;
		for (int i2=0; i2 < size_fig_l; i2++)
		{
			if (fig_l[i2] & fig_t[i1]) continue;
			for (int i3=0; i3 < size_fig_z; i3++)
			{
				if (fig_z[i3] & fig_l[i2]) continue;
				for (int i4=0; i4 < size_fig_p; i4++)
				{
					if (fig_p[i4] & fig_z[i3]) continue;
					for (int i5=0; i5 < size_fig_a; i5++)
					{
						if (fig_a[i5] & fig_p[i4]) continue;
						for (int i6=0; i6 < size_fig_b; i6++)
						{
							if (fig_b[i6] & fig_a[i5]) continue;
							int sol = fig_v[i0]+fig_t[i1]+fig_l[i2]+fig_z[i3]+fig_p[i4]+fig_a[i5]+fig_b[i6];
							if (sol == solution)
							{
								pthread_mutex_lock(&mutex);
								fprintf(stderr, "\nSolution #%d\n", ++(pparm->num_solutions));
								fprintf(fout, "%d,%d,%d,%d,%d,%d,%d\n", fig_v[i0],fig_t[i1],fig_l[i2],fig_z[i3],fig_p[i4],fig_a[i5],fig_b[i6]);
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

	pthread_mutex_init(&mutex, NULL);
	pthread_t thr[size_fig_v];
	solve_param_t sol_params[size_fig_v];

	for (int i = 0; i < size_fig_v; i++)
	{
		sol_params[i].v_num = i;
		sol_params[i].num_solutions = 0;
		pthread_create(&thr[i], NULL, solve, &sol_params[i]);
	}

	int total_solutions = 0;
	for (int i = 0; i < size_fig_v; i++)
	{
		pthread_join(thr[i], NULL);
		total_solutions += sol_params[i].num_solutions;
	}

	pthread_mutex_destroy(&mutex);
	fclose(fout);
	printf("Total solutions: %d\n", total_solutions);
	return 0;
}

