CFLAGS=`pkg-config --cflags glib-2.0` -g -Wall -O2 -D_GNU_SOURCE -pthread
LDLIBS=`pkg-config --libs glib-2.0` -lpthread
CC=c99
OBJECTS=nums_from_file.o string_utilities.o

all: soma gala

soma: soma_solver

gala: galacube_solver

soma_solver: $(OBJECTS) soma_solver.o

galacube_solver: $(OBJECTS) galacube_solver.o

clean:
	@rm *.o
