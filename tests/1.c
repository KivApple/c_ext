struct A {
    int a;

    void test();
};

struct B: A {
    int b;
};

struct B a;
struct A *b = &a;

int f(struct A*);

int main() {
    int (*g)(struct B*) = f;
    return 0;
}
