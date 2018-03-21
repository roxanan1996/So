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
	for (i = 0; i < 4; ++i) {
		printf("%hhx\n", *((unsigned char*)&w + 8 + 3 - i));
	}
	return 0;
}

