#include <stdio.h>
#include <stdarg.h>

typedef struct A {
    void construct();
    virtual void destroy();
    virtual void print_text(const char *fmt, ...) = 0;
} A;

typedef struct B: A {
    void construct();
    virtual void print_text(const char *fmt, ...);
} B;

void (A::construct)() {
    printf("A::construct()\n");
}

void (A::destroy)() {
    printf("Object destroyed\n");
}

void (B::print_text)(const char *fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}

void (B::construct)() {
    this->A::construct();
    printf("B::construct()\n");
}

B b;
A *b_ptr = &b;

int main() {
    b.construct();
    b_ptr->print_text("%s\n", "Hello world!");
    b_ptr->destroy();
    return 0;
}
