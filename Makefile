PRJ = soma

CC = c99
SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=.o)

CFLAGS = -O2 -Wall
#LDFLAGS = -o $(PRJ)

all: $(PRJ)

$(PRJ): $(SRCS)
	$(CC) $(CFLAGS) $^ -o $@

clean:
	rm $(PRJ)
