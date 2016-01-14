#include <stdlib.h>
#include "string_utilities.h"
#include "nums_from_file.h"

////////////////////////////////////////////////////////////////////////////////
// создаёт и заполняет динамический массив целыми числами из указанного файла
dyn_array_int_t nums_from_file(const char *filename)
{
	dyn_array_int_t nums = {};
	const char *delimeters = " ;:,\t\v\r\n";
	char *text = string_from_file(filename);
	if (!text)
		return nums;
	char *text_copy = text;

	ok_array *words = ok_array_new(text_copy, delimeters);
	if (!words)
		return nums;

	nums.vals = malloc(sizeof(int)*words->length);
	if (!nums.vals)
	{
		ok_array_free(words);
		return nums;
	}

	nums.size = words->length;
	memset(nums.vals, 0, nums.size*sizeof(int));
	for (int i = 0; i < nums.size; i++)
	{
		nums.vals[i] = strtol(words->elements[i], NULL, 10);
	}
	ok_array_free(words);
	return nums;		// nums.vals must be freed later!
}

////////////////////////////////////////////////////////////////////////////////
// создаёт и заполняет динамический массив целыми числами из указанного файла
dyn_array_long_t nums_from_file_long(const char *filename)
{
	dyn_array_long_t nums = {};
	const char *delimeters = " ;:,\t\v\r\n";
	char *text = string_from_file(filename);
	if (!text)
		return nums;
	char *text_copy = text;

	ok_array *words = ok_array_new(text_copy, delimeters);
	if (!words)
		return nums;

	nums.vals = malloc(sizeof(long)*words->length);
	if (!nums.vals)
	{
		ok_array_free(words);
		return nums;
	}

	nums.size = words->length;
	memset(nums.vals, 0, nums.size*sizeof(long));
	for (int i = 0; i < nums.size; i++)
	{
		nums.vals[i] = strtol(words->elements[i], NULL, 10);
	}
	ok_array_free(words);
	return nums;		// nums.vals must be freed later!
}

////////////////////////////////////////////////////////////////////////////////
// освобождение памяти динамического массива
void deinit_dyn_array(dyn_array_int_t *p_da)
{
	free(p_da->vals);
	p_da->size = 0;
}

////////////////////////////////////////////////////////////////////////////////
// освобождение памяти динамического массива
void deinit_dyn_array_long(dyn_array_long_t *p_da)
{
	free(p_da->vals);
	p_da->size = 0;
}

////////////////////////////////////////////////////////////////////////////////
#ifdef TEST_NUMS_FROM_FILE
int main(int argc, char** argv)
{
	if (argc < 2)
	{
		fprintf(stderr, "Specify filename!\n");
		return EXIT_FAILURE;
	}

	dyn_array_long_t nums = nums_from_file_long(argv[1]);
	if (!nums.vals)
	{
		fprintf(stderr, "Data error!\n");
		return EXIT_FAILURE;
	}

	printf("Sizeof int is %zd\n", sizeof(int));
	printf("Sizeof long is %zd\n", sizeof(long));
	printf("Sizeof long long int is %zd\n", sizeof(long long int));

	printf("Nums: %d\n", nums.size);
	for (int i = 0; i < nums.size; i++)
		printf("%ld\n", nums.vals[i]);

	deinit_dyn_array_long(&nums);
}
#endif
