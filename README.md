# c_ext
Translator from extended C to normal C

## Usage

    c_ext input-file-name.c output-file-name.c
    c_ext input-file-name.c output-file-name.c --preprocessor "cpp -o {output} {input}"
    c_ext input-file-name.c output-file-name.c --preprocessor "gcc -E -DFOO=BAR -o {output} {input}"

## Dependencies

* pycparser
* pycparserext
* appdirs
* six

## Installation

    python setup.py install

## Features

### Struct inheritance

You can define new struct which extends some existing struct.

    struct A {
        int i;
    };

    struct B: A {
        int j;
    };

    // Now B conains two members: i and j.

Pointer to child struct is compatible with parent struct.

    struct B some_struct;
    struct A *some_ptr = &some_struct; // Will not produce compiler warnings

### Struct methods

You can define methods inside structure.

    struct C {
        int i;
        void construct();
        static void some_static_method(int a, int b);
        virtual void some_virtual_method(int x);
        virtual void some_abstract_method(int y) = 0;
    };

    void C::construct() {
        this->i = 10;
    }

    void C::some_static_method(int a, int b) {
        printf("%i, %i\n", a, b);
    }

    void C::some_virtual_method(int x) {
        this->i = x;
    }
    ...
    struct C c;
    c.construct();
    c.some_virtual_method(10);

Child inherits methods from parent, but you can override some.
Also you can explicitly call parent method.

    struct D: C {
        void construct();
        virtual void some_virtual_method(int x);
    };

    void D::construct() {
        this->C::construct();
    }

    void D::some_virtual_method(int x) {
        this->C::some_virtual_method(x * 2);
    }

## Static struct members

    struct E {
        static int i;
        static void f();
    };
    ...
    int E::i = 0;
    ...
    E::i = 10;
    E::test();

## Lambda-functions

You can create anonymous functions:

    int (*sum)(int, int) = [] (int a, int b) -> int {
        return a + b;
    }

In addition to normal functions pointers still exist delegates:

    int (**sum)(void*, int, int) = [](int a, int b) -> int {
        return a + b;
    }

You can call delegates as normal functions,
but in fact this is not a simple pointer to a function as a set of functions and related data it.

Anonymous function can capture variables from current context by value or by reference.
In this case, they only can be used as delegates.

    int a, b;
    int (**inc_second_and_sum)(void*, int, int) = [a, &b]() -> int {
        b++;
        return a + b;
    }

Captured by reference variables must be available at the time of the call the anonymous function.

Unlike the usual function pointer when creating delegates is an allocation of memory and it must be released
when the delegate is no longer needed.

    int a, b;
    int (**inc_second_and_sum)(void*, int, int) = [a, &b]() -> int {
        b++;
        return a + b;
    }
    int c = inc_second_and_sum();
    free(inc_second_and_sum);

Also you can declare lambda as static:

    int a, b;
    int (**inc_second_and_sum)(void*, int, int) = static [a, &b]() -> int {
        b++;
        return a + b;
    }

In this case storage for closure will be allocated from current stack and will be valid
only in current context. Also you shouldn't free this lambda via free() call.

## Default values for function arguments

You can specify default values for some arguments of a function.

    void f(int a, int b = 10);
    
    f(5); // b == 10

## Asynchronous programming

Of particular importance is a function that takes a delegate as the last argument.
For example:

    void readFile(FILE *file, void *buffer, size_t bufferSize, void (**callback)(void*));

If you omit the last argument, the caller function (which must return void) will turn into asynchronous.

    void f(FILE *file) {
        char buffer[1024];
        readFile(file, buffer, sizeof(buffer));
        printf(buffer); // Will be run only after readFile call callback.
    }

Memory for asynchronous function state will be allocated via malloc on function call
and freed on it return.

## Limitations

* If you have declared virtual methods in structure, you must declare constructor.
This is not necessary if you just inherit the methods, but do not specify a new
and do not override the old ones.
* You must explicitly call constructors and destructors.
You can not use virtual methods before a constructor call.
* You must explicitly call the parent implementation, if necessary,
even if it's constructor.
* Names starting with __ (double underscore) reserved for internal usage.
* Asynchronous functions cannot return value or accept variadic arguments.

## License
This program distributed under terms of MIT license.
