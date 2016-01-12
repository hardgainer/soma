#ifndef __NUMS_FROM_FILE_H__
#define __NUMS_FROM_FILE_H__

typedef struct dyn_array_int_t
{
	int* vals;
	unsigned int size;
} dyn_array_int_t;

dyn_array_int_t nums_from_file(const char *filename);
void deinit_dyn_array(dyn_array_int_t *p_da);
#endif
