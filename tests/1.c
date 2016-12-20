#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdarg.h>

typedef struct A {
    static int i;
    int j;
    void construct();
    virtual void destroy();
    virtual void print_text(const char *fmt = NULL, ...) = 0;
    static void test(bool b = true);
} A;

typedef struct B: A {
    void construct();
    virtual void print_text(const char *fmt = NULL, ...);
} B;

int A::i = 0;

void A::construct() {
    i++;
    j = 0;
    printf("A::construct(i == %i)\n", i);
}

void A::destroy() {
    printf("Object destroyed\n");
}

void B::print_text(const char *fmt, ...) {
    if (fmt) {
        va_list args;
        va_start(args, fmt);
        vprintf(fmt, args);
        va_end(args);
    } else {
        printf("(null)\n");
    }
}

void B::construct() {
    A::construct();
    printf("B::construct(i == %i)\n", i);
}

void A::test(bool b) {
    if (b) {
        printf("Test!\n");
    } else {
        printf("Test (b == false)!\n");
    }
}

B b;
A *b_ptr = &b;

void (**(make_print_func)(const char *s))() {
    return [s]() {
        printf("%s\n", s);
    };
}

void run_foreach_element(int *array, size_t size, void (**func)(void*, int), bool destroy_func = true) {
    int i;
    for (i = 0; i < size; ++i) {
        func(array[i]);
    }
    if (destroy_func) {
        free(func);
    }
}

void f(void (**callback)(void*)) {
    callback();
}

void g(int i) {
    int j = 0;
    f();
    j++;
    f();
}

int main() {
    b.construct();
    b_ptr->print_text("%s\n", "Hello world!");
    b_ptr->print_text();
    b_ptr->destroy();
    A::test();
    void (**print_func)() = make_print_func("Test");
    print_func();
    free(print_func);

    int nums[] = { 1, 2, 3, 4 };
    int sum = 0;
    run_foreach_element(nums, 4, [&sum](int elem) {
        sum += elem;
    });
    printf("Sum = %i\n", sum);

    return 0;
}
