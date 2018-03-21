/**
  * SO, 2016
  * Lab #5
  *
  * Task #8, lin
  *
  * Endianess
  */
#include <stdlib.h>
#include <stdio.h>

#include "utils.h"

int main(void)
{
	int i;
	unsigned int n = 0xDEADBEEF;
	unsigned char *w;

	/* TODO - use w to show all bytes of n in order */
	
	unsigned char *sth = &w;
	for (i = 1; i < 5; ++i) {
		printf("%hhx\n", *(sth - i));
	}
	return 0;
}

