/**
  * SO, 2016
  * Lab #5
  *
  * Task #4, lin
  *
  * Use of gdb to solve "Segmentation fault" problems
  */
#include <stdlib.h>
#include <stdio.h>
#include <utils.h>

int main(void)
{
	char *buf;

	buf = malloc(1<<31);
	DIE(!buf, "NASPA");
	printf("Give input string:");
	fgets(buf, 1024, stdin);
	printf("\n\nString is %s\n", buf);

	free(buf);
	return 0;
}
