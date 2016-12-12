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

## Limitations

* If you have declared virtual methods in structure, you must declare constructor.
This is not necessary if you just inherit the methods, but do not specify a new
and do not override the old ones.
* You must explicitly call constructors and destructors.
You can not use virtual methods before a constructor call.
* You must explicitly call the parent implementation, if necessary,
even if it's constructor.
* If you defined typedef with name same as struct name, you need to place
method name in brackets in implementation:

`typedef struct A {
    void construct();
}

void (A::construct)() {
   // Do something
}`

## Future plans

* Lambdas
* Asynchronous programming

## License
This program distributed under terms of MIT license.
