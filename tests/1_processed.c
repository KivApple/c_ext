struct A
{
  int a;
};
void A_test(struct A *);
struct B
{
  int a;
  int b;
};
struct B a;
struct B *b = & a;
int f(struct A *);
int main()
{
  int (*g)(struct B *) = (int (struct B *) *) f;
  A_test((struct A *) b);
  return 0;
}

