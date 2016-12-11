struct A
{
  struct A_VTable *__vtable__;
  int a;
};
struct A_VTable
{
  void (*test3)(struct A *);
};
int () *A_c;
void A_test1();
void A_test2(struct A *);
void A_test3(struct A *);
struct B
{
  struct B_VTable *__vtable__;
  int a;
  int b;
};
struct B_VTable
{
  void (*test3)(struct A *);
};
struct B a;
struct B *b = & a;
int f(struct A *);
int main()
{
  int (*g)(struct B *) = (int (struct B *) *) f;
  A_test1();
  A_test2((struct A *) b);
  b->__vtable__->test3((struct A *) b);
  A_test3((struct A *) (& a));
  A_c();
  return 0;
}

