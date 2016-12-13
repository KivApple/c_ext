#line 216 "/usr/lib/gcc/x86_64-pc-linux-gnu/6.2.1/include/stddef.h"
typedef long unsigned int size_t;
#line 30 "/usr/include/bits/types.h"
typedef unsigned char __u_char;
typedef unsigned short int __u_short;
typedef unsigned int __u_int;
typedef unsigned long int __u_long;
#line 36 "/usr/include/bits/types.h"
typedef signed char __int8_t;
typedef unsigned char __uint8_t;
typedef signed short int __int16_t;
typedef unsigned short int __uint16_t;
typedef signed int __int32_t;
typedef unsigned int __uint32_t;
#line 43 "/usr/include/bits/types.h"
typedef signed long int __int64_t;
typedef unsigned long int __uint64_t;
#line 52 "/usr/include/bits/types.h"
typedef long int __quad_t;
typedef unsigned long int __u_quad_t;
#line 124 "/usr/include/bits/types.h"
typedef unsigned long int __dev_t;
typedef unsigned int __uid_t;
typedef unsigned int __gid_t;
typedef unsigned long int __ino_t;
typedef unsigned long int __ino64_t;
typedef unsigned int __mode_t;
typedef unsigned long int __nlink_t;
typedef long int __off_t;
typedef long int __off64_t;
typedef int __pid_t;
typedef struct 
{
#line 134 "/usr/include/bits/types.h"
  int __val[2];
} __fsid_t;
#line 135 "/usr/include/bits/types.h"
typedef long int __clock_t;
typedef unsigned long int __rlim_t;
typedef unsigned long int __rlim64_t;
typedef unsigned int __id_t;
typedef long int __time_t;
typedef unsigned int __useconds_t;
typedef long int __suseconds_t;
#line 143 "/usr/include/bits/types.h"
typedef int __daddr_t;
typedef int __key_t;
#line 147 "/usr/include/bits/types.h"
typedef int __clockid_t;
#line 150 "/usr/include/bits/types.h"
typedef void *__timer_t;
#line 153 "/usr/include/bits/types.h"
typedef long int __blksize_t;
#line 158 "/usr/include/bits/types.h"
typedef long int __blkcnt_t;
typedef long int __blkcnt64_t;
#line 162 "/usr/include/bits/types.h"
typedef unsigned long int __fsblkcnt_t;
typedef unsigned long int __fsblkcnt64_t;
#line 166 "/usr/include/bits/types.h"
typedef unsigned long int __fsfilcnt_t;
typedef unsigned long int __fsfilcnt64_t;
#line 170 "/usr/include/bits/types.h"
typedef long int __fsword_t;
#line 172 "/usr/include/bits/types.h"
typedef long int __ssize_t;
#line 175 "/usr/include/bits/types.h"
typedef long int __syscall_slong_t;
#line 177 "/usr/include/bits/types.h"
typedef unsigned long int __syscall_ulong_t;
#line 181 "/usr/include/bits/types.h"
typedef __off64_t __loff_t;
typedef __quad_t *__qaddr_t;
typedef char *__caddr_t;
#line 186 "/usr/include/bits/types.h"
typedef long int __intptr_t;
#line 189 "/usr/include/bits/types.h"
typedef unsigned int __socklen_t;
#line 44 "/usr/include/stdio.h"
struct _IO_FILE;
#line 48 "/usr/include/stdio.h"
typedef struct _IO_FILE FILE;
#line 64 "/usr/include/stdio.h"
typedef struct _IO_FILE __FILE;
#line 83 "/usr/include/wchar.h"
typedef struct 
{
#line 84 "/usr/include/wchar.h"
  int __count;
#line 86 "/usr/include/wchar.h"
  union 
  {
    unsigned int __wch;
#line 92 "/usr/include/wchar.h"
    char __wchb[4];
  } __value;
} __mbstate_t;
#line 22 "/usr/include/_G_config.h"
typedef struct 
{
#line 23 "/usr/include/_G_config.h"
  __off_t __pos;
  __mbstate_t __state;
} _G_fpos_t;
#line 27 "/usr/include/_G_config.h"
typedef struct 
{
#line 28 "/usr/include/_G_config.h"
  __off64_t __pos;
  __mbstate_t __state;
} _G_fpos64_t;
#line 40 "/usr/lib/gcc/x86_64-pc-linux-gnu/6.2.1/include/stdarg.h"
typedef __builtin_va_list __gnuc_va_list;
#line 144 "/usr/include/libio.h"
struct _IO_jump_t;
#line 144 "/usr/include/libio.h"
struct _IO_FILE;
#line 150 "/usr/include/libio.h"
typedef void _IO_lock_t;
#line 156 "/usr/include/libio.h"
struct _IO_marker
{
#line 157 "/usr/include/libio.h"
  struct _IO_marker *_next;
  struct _IO_FILE *_sbuf;
#line 162 "/usr/include/libio.h"
  int _pos;
};
#line 176 "/usr/include/libio.h"
enum __codecvt_result {__codecvt_ok, __codecvt_partial, __codecvt_error, __codecvt_noconv};
#line 241 "/usr/include/libio.h"
struct _IO_FILE
{
#line 242 "/usr/include/libio.h"
  int _flags;
#line 247 "/usr/include/libio.h"
  char *_IO_read_ptr;
  char *_IO_read_end;
  char *_IO_read_base;
  char *_IO_write_base;
  char *_IO_write_ptr;
  char *_IO_write_end;
  char *_IO_buf_base;
  char *_IO_buf_end;
#line 256 "/usr/include/libio.h"
  char *_IO_save_base;
  char *_IO_backup_base;
  char *_IO_save_end;
#line 260 "/usr/include/libio.h"
  struct _IO_marker *_markers;
#line 262 "/usr/include/libio.h"
  struct _IO_FILE *_chain;
#line 264 "/usr/include/libio.h"
  int _fileno;
#line 268 "/usr/include/libio.h"
  int _flags2;
#line 270 "/usr/include/libio.h"
  __off_t _old_offset;
#line 274 "/usr/include/libio.h"
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];
#line 280 "/usr/include/libio.h"
  _IO_lock_t *_lock;
#line 289 "/usr/include/libio.h"
  __off64_t _offset;
#line 297 "/usr/include/libio.h"
  void *__pad1;
  void *__pad2;
  void *__pad3;
  void *__pad4;
#line 302 "/usr/include/libio.h"
  size_t __pad5;
  int _mode;
#line 305 "/usr/include/libio.h"
  char _unused2[((15 * (sizeof(int))) - (4 * (sizeof(void *)))) - (sizeof(size_t))];
};
#line 310 "/usr/include/libio.h"
typedef struct _IO_FILE _IO_FILE;
#line 313 "/usr/include/libio.h"
struct _IO_FILE_plus;
#line 315 "/usr/include/libio.h"
extern struct _IO_FILE_plus _IO_2_1_stdin_;
extern struct _IO_FILE_plus _IO_2_1_stdout_;
extern struct _IO_FILE_plus _IO_2_1_stderr_;
#line 333 "/usr/include/libio.h"
typedef __ssize_t __io_read_fn(void *__cookie, char *__buf, size_t __nbytes);
#line 341 "/usr/include/libio.h"
typedef __ssize_t __io_write_fn(void *__cookie, const char *__buf, size_t __n);
#line 350 "/usr/include/libio.h"
typedef int __io_seek_fn(void *__cookie, __off64_t *__pos, int __w);
#line 353 "/usr/include/libio.h"
typedef int __io_close_fn(void *__cookie);
#line 385 "/usr/include/libio.h"
extern int __underflow(_IO_FILE *);
extern int __uflow(_IO_FILE *);
extern int __overflow(_IO_FILE *, int);
#line 429 "/usr/include/libio.h"
extern int _IO_getc(_IO_FILE *__fp);
extern int _IO_putc(int __c, _IO_FILE *__fp);
extern int _IO_feof(_IO_FILE *__fp) __attribute__((__nothrow__, __leaf__));
extern int _IO_ferror(_IO_FILE *__fp) __attribute__((__nothrow__, __leaf__));
#line 434 "/usr/include/libio.h"
extern int _IO_peekc_locked(_IO_FILE *__fp);
#line 440 "/usr/include/libio.h"
extern void _IO_flockfile(_IO_FILE *) __attribute__((__nothrow__, __leaf__));
extern void _IO_funlockfile(_IO_FILE *) __attribute__((__nothrow__, __leaf__));
extern int _IO_ftrylockfile(_IO_FILE *) __attribute__((__nothrow__, __leaf__));
#line 459 "/usr/include/libio.h"
extern int _IO_vfscanf(_IO_FILE *__restrict , const char *__restrict , __gnuc_va_list, int *__restrict );
#line 461 "/usr/include/libio.h"
extern int _IO_vfprintf(_IO_FILE *__restrict , const char *__restrict , __gnuc_va_list);
#line 463 "/usr/include/libio.h"
extern __ssize_t _IO_padn(_IO_FILE *, int, __ssize_t);
extern size_t _IO_sgetn(_IO_FILE *, void *, size_t);
#line 466 "/usr/include/libio.h"
extern __off64_t _IO_seekoff(_IO_FILE *, __off64_t, int, int);
extern __off64_t _IO_seekpos(_IO_FILE *, __off64_t, int);
#line 469 "/usr/include/libio.h"
extern void _IO_free_backup_area(_IO_FILE *) __attribute__((__nothrow__, __leaf__));
#line 79 "/usr/include/stdio.h"
typedef __gnuc_va_list va_list;
#line 90 "/usr/include/stdio.h"
typedef __off_t off_t;
#line 104 "/usr/include/stdio.h"
typedef __ssize_t ssize_t;
#line 112 "/usr/include/stdio.h"
typedef _G_fpos_t fpos_t;
#line 170 "/usr/include/stdio.h"
extern struct _IO_FILE *stdin;
extern struct _IO_FILE *stdout;
extern struct _IO_FILE *stderr;
#line 180 "/usr/include/stdio.h"
extern int remove(const char *__filename) __attribute__((__nothrow__, __leaf__));
#line 182 "/usr/include/stdio.h"
extern int rename(const char *__old, const char *__new) __attribute__((__nothrow__, __leaf__));
#line 187 "/usr/include/stdio.h"
extern int renameat(int __oldfd, const char *__old, int __newfd, const char *__new) __attribute__((__nothrow__, __leaf__));
#line 197 "/usr/include/stdio.h"
extern FILE *tmpfile(void);
#line 211 "/usr/include/stdio.h"
extern char *tmpnam(char *__s) __attribute__((__nothrow__, __leaf__));
#line 217 "/usr/include/stdio.h"
extern char *tmpnam_r(char *__s) __attribute__((__nothrow__, __leaf__));
#line 229 "/usr/include/stdio.h"
extern char *tempnam(const char *__dir, const char *__pfx) __attribute__((__nothrow__, __leaf__, __malloc__));
#line 239 "/usr/include/stdio.h"
extern int fclose(FILE *__stream);
#line 244 "/usr/include/stdio.h"
extern int fflush(FILE *__stream);
#line 254 "/usr/include/stdio.h"
extern int fflush_unlocked(FILE *__stream);
#line 274 "/usr/include/stdio.h"
extern FILE *fopen(const char *__restrict __filename, const char *__restrict __modes);
#line 280 "/usr/include/stdio.h"
extern FILE *freopen(const char *__restrict __filename, const char *__restrict __modes, FILE *__restrict __stream);
#line 308 "/usr/include/stdio.h"
extern FILE *fdopen(int __fd, const char *__modes) __attribute__((__nothrow__, __leaf__));
#line 321 "/usr/include/stdio.h"
extern FILE *fmemopen(void *__s, size_t __len, const char *__modes) __attribute__((__nothrow__, __leaf__));
#line 327 "/usr/include/stdio.h"
extern FILE *open_memstream(char **__bufloc, size_t *__sizeloc) __attribute__((__nothrow__, __leaf__));
#line 334 "/usr/include/stdio.h"
extern void setbuf(FILE *__restrict __stream, char *__restrict __buf) __attribute__((__nothrow__, __leaf__));
#line 338 "/usr/include/stdio.h"
extern int setvbuf(FILE *__restrict __stream, char *__restrict __buf, int __modes, size_t __n) __attribute__((__nothrow__, __leaf__));
#line 345 "/usr/include/stdio.h"
extern void setbuffer(FILE *__restrict __stream, char *__restrict __buf, size_t __size) __attribute__((__nothrow__, __leaf__));
#line 349 "/usr/include/stdio.h"
extern void setlinebuf(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 358 "/usr/include/stdio.h"
extern int fprintf(FILE *__restrict __stream, const char *__restrict __format, ...);
#line 364 "/usr/include/stdio.h"
extern int printf(const char *__restrict __format, ...);
#line 366 "/usr/include/stdio.h"
extern int sprintf(char *__restrict __s, const char *__restrict __format, ...) __attribute__((__nothrow__));
#line 373 "/usr/include/stdio.h"
extern int vfprintf(FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg);
#line 379 "/usr/include/stdio.h"
extern int vprintf(const char *__restrict __format, __gnuc_va_list __arg);
#line 381 "/usr/include/stdio.h"
extern int vsprintf(char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __attribute__((__nothrow__));
#line 388 "/usr/include/stdio.h"
extern int snprintf(char *__restrict __s, size_t __maxlen, const char *__restrict __format, ...) __attribute__((__nothrow__, __format__(__printf__, 3, 4)));
#line 392 "/usr/include/stdio.h"
extern int vsnprintf(char *__restrict __s, size_t __maxlen, const char *__restrict __format, __gnuc_va_list __arg) __attribute__((__nothrow__, __format__(__printf__, 3, 0)));
#line 414 "/usr/include/stdio.h"
extern int vdprintf(int __fd, const char *__restrict __fmt, __gnuc_va_list __arg) __attribute__((__format__(__printf__, 2, 0)));
#line 417 "/usr/include/stdio.h"
extern int dprintf(int __fd, const char *__restrict __fmt, ...) __attribute__((__format__(__printf__, 2, 3)));
#line 427 "/usr/include/stdio.h"
extern int fscanf(FILE *__restrict __stream, const char *__restrict __format, ...);
#line 433 "/usr/include/stdio.h"
extern int scanf(const char *__restrict __format, ...);
#line 435 "/usr/include/stdio.h"
extern int sscanf(const char *__restrict __s, const char *__restrict __format, ...) __attribute__((__nothrow__, __leaf__));
#line 445 "/usr/include/stdio.h"
extern int fscanf(FILE *__restrict __stream, const char *__restrict __format, ...)  __asm__("__isoc99_fscanf");
#line 448 "/usr/include/stdio.h"
extern int scanf(const char *__restrict __format, ...)  __asm__("__isoc99_scanf");
#line 450 "/usr/include/stdio.h"
extern int sscanf(const char *__restrict __s, const char *__restrict __format, ...)  __asm__("__isoc99_sscanf") __attribute__((__nothrow__, __leaf__));
#line 473 "/usr/include/stdio.h"
extern int vfscanf(FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __attribute__((__format__(__scanf__, 2, 0)));
#line 481 "/usr/include/stdio.h"
extern int vscanf(const char *__restrict __format, __gnuc_va_list __arg) __attribute__((__format__(__scanf__, 1, 0)));
#line 485 "/usr/include/stdio.h"
extern int vsscanf(const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg) __attribute__((__nothrow__, __leaf__, __format__(__scanf__, 2, 0)));
#line 496 "/usr/include/stdio.h"
extern int vfscanf(FILE *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg)  __asm__("__isoc99_vfscanf") __attribute__((__format__(__scanf__, 2, 0)));
#line 501 "/usr/include/stdio.h"
extern int vscanf(const char *__restrict __format, __gnuc_va_list __arg)  __asm__("__isoc99_vscanf") __attribute__((__format__(__scanf__, 1, 0)));
#line 504 "/usr/include/stdio.h"
extern int vsscanf(const char *__restrict __s, const char *__restrict __format, __gnuc_va_list __arg)  __asm__("__isoc99_vsscanf") __attribute__((__nothrow__, __leaf__, __format__(__scanf__, 2, 0)));
#line 533 "/usr/include/stdio.h"
extern int fgetc(FILE *__stream);
extern int getc(FILE *__stream);
#line 540 "/usr/include/stdio.h"
extern int getchar(void);
#line 552 "/usr/include/stdio.h"
extern int getc_unlocked(FILE *__stream);
extern int getchar_unlocked(void);
#line 563 "/usr/include/stdio.h"
extern int fgetc_unlocked(FILE *__stream);
#line 575 "/usr/include/stdio.h"
extern int fputc(int __c, FILE *__stream);
extern int putc(int __c, FILE *__stream);
#line 582 "/usr/include/stdio.h"
extern int putchar(int __c);
#line 596 "/usr/include/stdio.h"
extern int fputc_unlocked(int __c, FILE *__stream);
#line 604 "/usr/include/stdio.h"
extern int putc_unlocked(int __c, FILE *__stream);
extern int putchar_unlocked(int __c);
#line 612 "/usr/include/stdio.h"
extern int getw(FILE *__stream);
#line 615 "/usr/include/stdio.h"
extern int putw(int __w, FILE *__stream);
#line 624 "/usr/include/stdio.h"
extern char *fgets(char *__restrict __s, int __n, FILE *__restrict __stream);
#line 667 "/usr/include/stdio.h"
extern __ssize_t __getdelim(char **__restrict __lineptr, size_t *__restrict __n, int __delimiter, FILE *__restrict __stream);
#line 670 "/usr/include/stdio.h"
extern __ssize_t getdelim(char **__restrict __lineptr, size_t *__restrict __n, int __delimiter, FILE *__restrict __stream);
#line 680 "/usr/include/stdio.h"
extern __ssize_t getline(char **__restrict __lineptr, size_t *__restrict __n, FILE *__restrict __stream);
#line 691 "/usr/include/stdio.h"
extern int fputs(const char *__restrict __s, FILE *__restrict __stream);
#line 697 "/usr/include/stdio.h"
extern int puts(const char *__s);
#line 704 "/usr/include/stdio.h"
extern int ungetc(int __c, FILE *__stream);
#line 711 "/usr/include/stdio.h"
extern size_t fread(void *__restrict __ptr, size_t __size, size_t __n, FILE *__restrict __stream);
#line 717 "/usr/include/stdio.h"
extern size_t fwrite(const void *__restrict __ptr, size_t __size, size_t __n, FILE *__restrict __s);
#line 739 "/usr/include/stdio.h"
extern size_t fread_unlocked(void *__restrict __ptr, size_t __size, size_t __n, FILE *__restrict __stream);
#line 741 "/usr/include/stdio.h"
extern size_t fwrite_unlocked(const void *__restrict __ptr, size_t __size, size_t __n, FILE *__restrict __stream);
#line 751 "/usr/include/stdio.h"
extern int fseek(FILE *__stream, long int __off, int __whence);
#line 756 "/usr/include/stdio.h"
extern long int ftell(FILE *__stream);
#line 761 "/usr/include/stdio.h"
extern void rewind(FILE *__stream);
#line 775 "/usr/include/stdio.h"
extern int fseeko(FILE *__stream, __off_t __off, int __whence);
#line 780 "/usr/include/stdio.h"
extern __off_t ftello(FILE *__stream);
#line 800 "/usr/include/stdio.h"
extern int fgetpos(FILE *__restrict __stream, fpos_t *__restrict __pos);
#line 805 "/usr/include/stdio.h"
extern int fsetpos(FILE *__stream, const fpos_t *__pos);
#line 828 "/usr/include/stdio.h"
extern void clearerr(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 830 "/usr/include/stdio.h"
extern int feof(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 832 "/usr/include/stdio.h"
extern int ferror(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 837 "/usr/include/stdio.h"
extern void clearerr_unlocked(FILE *__stream) __attribute__((__nothrow__, __leaf__));
extern int feof_unlocked(FILE *__stream) __attribute__((__nothrow__, __leaf__));
extern int ferror_unlocked(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 848 "/usr/include/stdio.h"
extern void perror(const char *__s);
#line 26 "/usr/include/bits/sys_errlist.h"
extern int sys_nerr;
extern const char *const sys_errlist[];
#line 860 "/usr/include/stdio.h"
extern int fileno(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 865 "/usr/include/stdio.h"
extern int fileno_unlocked(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 874 "/usr/include/stdio.h"
extern FILE *popen(const char *__command, const char *__modes);
#line 880 "/usr/include/stdio.h"
extern int pclose(FILE *__stream);
#line 886 "/usr/include/stdio.h"
extern char *ctermid(char *__s) __attribute__((__nothrow__, __leaf__));
#line 914 "/usr/include/stdio.h"
extern void flockfile(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 918 "/usr/include/stdio.h"
extern int ftrylockfile(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 921 "/usr/include/stdio.h"
extern void funlockfile(FILE *__stream) __attribute__((__nothrow__, __leaf__));
#line 4 "/home/kiv/projects/c_ext/tests/1.c"
typedef struct A
{
#line 4 "/home/kiv/projects/c_ext/tests/1.c"
  const struct A_VTable *__vtable__;
} A;
#line 4 "/home/kiv/projects/c_ext/tests/1.c"
extern const struct A_VTable
{
#line 4 "/home/kiv/projects/c_ext/tests/1.c"
  const void *__parent__;
#line 4 "/home/kiv/projects/c_ext/tests/1.c"
  const char *__name__;
#line 7 "/home/kiv/projects/c_ext/tests/1.c"
  void (*destroy)(struct A *);
  void (*print_text)(struct A *, const char *, ...);
} A_vtable;
#line 5 "/home/kiv/projects/c_ext/tests/1.c"
extern int A_i;
void A_construct(struct A *);
void A_destroy(struct A *);
#line 9 "/home/kiv/projects/c_ext/tests/1.c"
void A_test();
#line 12 "/home/kiv/projects/c_ext/tests/1.c"
typedef struct B
{
#line 12 "/home/kiv/projects/c_ext/tests/1.c"
  const struct B_VTable *__vtable__;
} B;
#line 12 "/home/kiv/projects/c_ext/tests/1.c"
extern const struct B_VTable
{
#line 12 "/home/kiv/projects/c_ext/tests/1.c"
  const struct A_VTable *__parent__;
#line 12 "/home/kiv/projects/c_ext/tests/1.c"
  const char *__name__;
#line 7 "/home/kiv/projects/c_ext/tests/1.c"
  void (*destroy)(struct A *);
#line 14 "/home/kiv/projects/c_ext/tests/1.c"
  void (*print_text)(struct B *, const char *, ...);
} B_vtable;
#line 13 "/home/kiv/projects/c_ext/tests/1.c"
void B_construct(struct B *);
void B_print_text(struct B *, const char *, ...);
#line 17 "/home/kiv/projects/c_ext/tests/1.c"
int A_i = 0;
#line 19 "/home/kiv/projects/c_ext/tests/1.c"
void A_construct(struct A *const this)
{
#line 20 "/home/kiv/projects/c_ext/tests/1.c"
  A_i++;
#line 19 "/home/kiv/projects/c_ext/tests/1.c"
  this->__vtable__ = & A_vtable;
#line 21 "/home/kiv/projects/c_ext/tests/1.c"
  printf("A::construct(i == %i)\n", A_i);
}

#line 19 "/home/kiv/projects/c_ext/tests/1.c"
const struct A_VTable A_vtable = {0, "A", A_destroy, 0};
#line 24 "/home/kiv/projects/c_ext/tests/1.c"
void A_destroy(struct A *const this)
{
#line 25 "/home/kiv/projects/c_ext/tests/1.c"
  printf("Object destroyed\n");
}

void B_print_text(struct B *const this, const char *fmt, ...)
{
#line 29 "/home/kiv/projects/c_ext/tests/1.c"
  va_list args;
  __builtin_va_start(args, fmt);
  vprintf(fmt, args);
  __builtin_va_end(args);
}

void B_construct(struct B *const this)
{
#line 36 "/home/kiv/projects/c_ext/tests/1.c"
  A_construct((struct A *const ) this);
  printf("B::construct(i == %i)\n", A_i);
#line 35 "/home/kiv/projects/c_ext/tests/1.c"
  this->__vtable__ = & B_vtable;
}

#line 35 "/home/kiv/projects/c_ext/tests/1.c"
const struct B_VTable B_vtable = {& A_vtable, "B", A_destroy, B_print_text};
#line 40 "/home/kiv/projects/c_ext/tests/1.c"
void A_test()
{
#line 41 "/home/kiv/projects/c_ext/tests/1.c"
  printf("Test!\n");
}

B b;
A *b_ptr = (struct A *) (& b);
#line 47 "/home/kiv/projects/c_ext/tests/1.c"
int main()
{
#line 48 "/home/kiv/projects/c_ext/tests/1.c"
  B_construct(& b);
  b_ptr->__vtable__->print_text(b_ptr, "%s\n", "Hello world!");
  b_ptr->__vtable__->destroy(b_ptr);
  A_test();
  return 0;
}

