struct A {
    virtual int get_value();
};

struct B: A {
    virtual int get_value();
};

int A::get_value() {
    return 10;
}

int B::get_value() {
    this->get_value();
    return this->A::get_value() * 2;
}

struct B b;
struct B *b_ptr = &b;

int main() {
    b_ptr->get_value();
    return 0;
}
