struct A {
    int a;
    static int (*c)();

    static void test1();
    void test2();
    virtual void test3();
};

struct B: A {
    int b;
};

struct B a;
struct B *b = &a;

int f(struct A*);

int main() {
    int (*g)(struct B*) = f;
    b->test1();
    b->test2();
    b->test3();
    a.test3();
    a.c();
    return 0;
}
