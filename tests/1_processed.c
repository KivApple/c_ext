struct A
{
  struct A_VTable *__vtable__;
};
struct A_VTable
{
  int (*get_value)(struct A *);
};
int A_get_value(struct A *);
struct B
{
  struct B_VTable *__vtable__;
};
struct B_VTable
{
  int (*get_value)(struct A *);
  int (*get_value)(struct B *);
};
int B_get_value(struct B *);
int A_get_value(struct A * const this)
{
  return 10;
}

int B_get_value(struct B * const this)
{
  this->__vtable__->get_value(this);
  return A_get_value((struct A * const ) this) * 2;
}

struct B b;
struct B *b_ptr = & b;
int main()
{
  b_ptr->__vtable__->get_value(b_ptr);
  return 0;
}

