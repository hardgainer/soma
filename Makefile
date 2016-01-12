P=soma_solver

CFLAGS=`pkg-config --cflags glib-2.0` -g -Wall -O3 -D_GNU_SOURCE -pthread
LDLIBS=`pkg-config --libs glib-2.0` -lpthread
CC=c99
OBJECTS=nums_from_file.o string_utilities.o soma_solver.o

$(P): $(OBJECTS)

clean:
	@rm $(P) $(OBJECTS)
