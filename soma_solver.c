// gcc -O2 -Wall -std=c99 -o soma *.c && ./soma
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

extern const int fig_a[], size_fig_a;
extern const int fig_b[], size_fig_b;
extern const int fig_l[], size_fig_l;
extern const int fig_p[], size_fig_p;
extern const int fig_t[], size_fig_t;
extern const int fig_v[], size_fig_v;
extern const int fig_z[], size_fig_z;

// порядок обхода фигур: v,t,l,z,p,a,b
int main()
{
	const int solution = (1<<27)-1;
	int num_solutions = 0;
	int i0, last_v;
	const char *fname;

	/*setvbuf(stdout, NULL, _IOLBF, 0);*/
	pid_t pid = fork();
	switch(pid)
	{
		case -1: perror("fork failed"); exit(1);
		case  0: i0 = size_fig_v/2; last_v = size_fig_v; fname = "s1.log"; break;	// child
		default: i0 = 0; last_v = size_fig_v/2; fname = "s0.log"; break;	// parent
	}
	FILE *fout = fopen(fname, "w");
	if (!fout)
	{
		perror("can't open file");
		exit(2);
	}

	for (; i0 < last_v; i0++)
	{
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
									fprintf(stderr, "\nSolution #%d\n", ++num_solutions);
									fprintf(fout, "%d,%d,%d,%d,%d,%d,%d\n", fig_v[i0],fig_t[i1],fig_l[i2],fig_z[i3],fig_p[i4],fig_a[i5],fig_b[i6]);
									fflush(fout);
								}
							}
						}
					}
				}
			}
		}
		fprintf(stderr, "%d ", i0);
	}
	fclose(fout);
	return 0;
}
