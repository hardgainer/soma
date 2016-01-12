#include <glib.h>
#include <string.h>
#include "string_utilities.h"
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>    // abort

char *string_from_file(char const *filename)
{
	char *out;
	GError *e = NULL;
	GIOChannel *f = g_io_channel_new_file(filename, "r", &e);
	if (!f)
	{
		fprintf(stderr, "failed to open file '%s'.\n", filename);
		return NULL;
	}
	if (g_io_channel_read_to_end(f, &out, NULL, &e) != G_IO_STATUS_NORMAL)
	{
		fprintf(stderr, "found file '%s' but couldn't read it.\n", filename);
		return NULL;
	}
	return out;
}

ok_array *ok_array_new(char *instring, char const *delimeters)
{
	ok_array *out = malloc(sizeof(ok_array));
	*out = (ok_array){.base_string = instring};
	char *scratch = NULL;
	char *txt = strtok_r(instring, delimeters, &scratch);
	if (!txt) return NULL;
	while (txt)
	{
		out->elements = realloc(out->elements, sizeof(char*)*++(out->length));
		out->elements[out->length-1] = txt;
		txt = strtok_r(NULL, delimeters, &scratch);
	}
	return out;
}

// frees the original string, because strtok_r mangled it
void ok_array_free(ok_array *ok_in)
{
	if (ok_in == NULL) return;
	free(ok_in->base_string);
	free(ok_in->elements);
	free(ok_in);
}

#ifdef TEST_OK_ARRAY
int main()
{
	char *delimeters = " `~!@#$%^&*()_-+={[]}|\\;:\",<>./?\n";
	ok_array *o = ok_array_new(strdup("Hello,  reader.\nThis is text."), delimeters);
	assert(o->length == 5);
	assert(!strcmp(o->elements[1], "reader"));
	assert(!strcmp(o->elements[4], "text"));
	ok_array_free(o);
	printf("OK.\n");
}
#endif
