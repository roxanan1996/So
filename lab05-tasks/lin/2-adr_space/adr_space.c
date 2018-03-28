/**
  * SO, 2016
  * Lab #5
  *
  * Task #2, lin
  *
  * Variables in process address space viewed with objdump
  */
#include <stdlib.h>
#include <stdio.h>
int var_a;
int var_b = 2;
char var_c[] = "so";

int main(void)
{
	int var_d;
	static int var_e;
	char *var_f = "rulz";
	
	for (int i = 0; i < 4; ++i) {
		printf("%c\n", *(var_f + i));
	}
	for (int i = 0; i < 4; ++i) {
		*(var_f + i) = 'i';
	}

	char *var_g = malloc(10);

	return 0;
}
