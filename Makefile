obj-m+=gdpymod.o
#ccflags-y+=-O2

all:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) modules
#	make -C ../.. M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) clean
#	make -C ../.. M=$(PWD) clean
