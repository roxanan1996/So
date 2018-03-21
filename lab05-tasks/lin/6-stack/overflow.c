/**
  * SO, 2016
  * Lab #5
  *
  * Task #6, lin
  *
  * Stack smashing
  */
#include <stdio.h>
#include <stdlib.h>

#include "utils.h"

#if defined(__i386__)
#define get_esp(esp) __asm__("movl %%esp, %0;":"=&r"(esp))
#define get_ebp(ebp) __asm__("movl %%ebp, %0;":"=&r"(ebp))

typedef int mytype;

#elif defined(__x86_64)
#define get_esp(esp) __asm__("mov %%rsp, %0;":"=&r"(esp))
#define get_ebp(ebp) __asm__("mov %%rbp, %0;":"=&r"(ebp))

typedef long mytype;

#else
  #error "Unknown architecture"
#endif

int i, size;
mytype *esp, *ebp;
mytype *p;


struct stack_element {
	mytype *address;
	mytype value;
};

/*
 * stack vector represents the program stack
 * each element contains an address from the stack and the actual value
 * at that address
 */
struct stack_element stack[128];

/**
 * show_snapshot - prints the stack in the following format:
 * [address: value]
 */
void show_snapshot(void)
{
	for (i = 0; i < size; i++)
		/* TODO1 - fill in the correct parameters to be printed */
		printf("[%p]:%x\n", ebp - i, *(ebp - i) /* TODO1 */);
}

/**
 * save the stack between ebp and esp in the stack vector
 */
void take_snapshot(void)
{
	for (p = ebp; p >= esp; p--) {
		stack[size].address = p; /* TODO1: set the current address */
		stack[size].value   = *p; /* TODO1: set the value at address */
		size++;
	}
}

void show_message(void)
{
	printf("s0rU1lz\n");
	exit(EXIT_FAILURE);
}

void f2(mytype x, mytype y, mytype z)
{
	mytype v[3];

	v[0] = 6;
	v[1] = 7;
	v[2] = 8;

	/* TODO2: use v so that when function 'f2' returns,
	 * the 'show_message' function executes
	 */
	v[4] = 8;
	v[5] = 9;
	v[6] = 20;
	v[7] = 0x400791;

	/* save current stack pointer */
	get_esp(esp);

	/* use previously saved esp and epb pointers */
	take_snapshot();
}

static void f1(mytype a, mytype b, mytype c)
{
	f2(3, 4, 5);
}

int main(void)
{
	/* save current ebp for later use */
	get_ebp(ebp);

	f1(1, 2, 3);

	/* analize the stack */
	show_snapshot();

	return 0;
}
