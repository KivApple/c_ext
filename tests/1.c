#include <stdio.h>

struct A {
    void construct();
    virtual void destroy();
    virtual void print_text() = 0;
};

struct B: A {
    void construct();
    virtual void print_text();
};

void A::construct() {

}

void A::destroy() {

}

void B::print_text() {
    printf("Hello world\n");
}

void B::construct() {

}

struct B b;
struct A *b_ptr = &b;

int main() {
    b.construct();
    b_ptr->print_text();
    b_ptr->destroy();
    return 0;
}
