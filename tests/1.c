struct A {
    int a;

    void test();
};

struct B: A {
    int b;
};

struct B a;
struct B *b = &a;

int f(struct A*);

int main() {
    int (*g)(struct B*) = f;
    b->test();
    return 0;
}
