#include <stdio.h>

struct A {
    void A();
    virtual void print_text() = 0;
};

struct B: A {
    void B();
    virtual void print_text();
};

void A::A() {

}

void B::print_text() {
    printf("Hello world\n");
}

void B::B() {

}

struct B b;
struct B *b_ptr = &b;

int main() {
    b.B();
    b_ptr->print_text();
    return 0;
}
