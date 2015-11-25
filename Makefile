PRJ=soma

CC=c99
SRCS := soma_solver.c $(wildcard fig*.c)
OBJS := $(SRCS:.c=.o)

CFLAGS := -O2 -Wall -pthread
LDLIBS := -lpthread

all: $(PRJ)

$(PRJ): $(SRCS)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm $(PRJ)
