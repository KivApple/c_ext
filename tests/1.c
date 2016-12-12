#include <stdlib.h>
#include <stdio.h>

struct A {
    virtual void print_text();
};

struct B: A {
    virtual void print_text();
};

void A::print_text() {
    printf("Hello world");
}

struct B b;
struct B *b_ptr = &b;

int main() {
    b_ptr->print_text();
    return 0;
}
