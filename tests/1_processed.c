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
#line 328 "/usr/lib/gcc/x86_64-pc-linux-gnu/6.2.1/include/stddef.h"
typedef int wchar_t;
#line 59 "/usr/include/stdlib.h"
typedef struct 
{
#line 60 "/usr/include/stdlib.h"
  int quot;
  int rem;
} div_t;
#line 67 "/usr/include/stdlib.h"
typedef struct 
{
#line 68 "/usr/include/stdlib.h"
  long int quot;
  long int rem;
} ldiv_t;
#line 79 "/usr/include/stdlib.h"
__extension__ typedef struct 
{
#line 80 "/usr/include/stdlib.h"
  long long int quot;
  long long int rem;
} lldiv_t;
#line 100 "/usr/include/stdlib.h"
extern size_t __ctype_get_mb_cur_max(void) __attribute__((__nothrow__, __leaf__));
#line 105 "/usr/include/stdlib.h"
extern double atof(const char *__nptr) __attribute__((__nothrow__, __leaf__, __pure__, __nonnull__(1)));
#line 108 "/usr/include/stdlib.h"
extern int atoi(const char *__nptr) __attribute__((__nothrow__, __leaf__, __pure__, __nonnull__(1)));
#line 111 "/usr/include/stdlib.h"
extern long int atol(const char *__nptr) __attribute__((__nothrow__, __leaf__, __pure__, __nonnull__(1)));
#line 118 "/usr/include/stdlib.h"
__extension__ extern long long int atoll(const char *__nptr) __attribute__((__nothrow__, __leaf__, __pure__, __nonnull__(1)));
#line 125 "/usr/include/stdlib.h"
extern double strtod(const char *__restrict __nptr, char **__restrict __endptr) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 133 "/usr/include/stdlib.h"
extern float strtof(const char *__restrict __nptr, char **__restrict __endptr) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 136 "/usr/include/stdlib.h"
extern long double strtold(const char *__restrict __nptr, char **__restrict __endptr) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 144 "/usr/include/stdlib.h"
extern long int strtol(const char *__restrict __nptr, char **__restrict __endptr, int __base) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 148 "/usr/include/stdlib.h"
extern unsigned long int strtoul(const char *__restrict __nptr, char **__restrict __endptr, int __base) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 156 "/usr/include/stdlib.h"
__extension__ extern long long int strtoq(const char *__restrict __nptr, char **__restrict __endptr, int __base) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 161 "/usr/include/stdlib.h"
__extension__ extern unsigned long long int strtouq(const char *__restrict __nptr, char **__restrict __endptr, int __base) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 170 "/usr/include/stdlib.h"
__extension__ extern long long int strtoll(const char *__restrict __nptr, char **__restrict __endptr, int __base) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 175 "/usr/include/stdlib.h"
__extension__ extern unsigned long long int strtoull(const char *__restrict __nptr, char **__restrict __endptr, int __base) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 266 "/usr/include/stdlib.h"
extern char *l64a(long int __n) __attribute__((__nothrow__, __leaf__));
#line 269 "/usr/include/stdlib.h"
extern long int a64l(const char *__s) __attribute__((__nothrow__, __leaf__, __pure__, __nonnull__(1)));
#line 33 "/usr/include/sys/types.h"
typedef __u_char u_char;
typedef __u_short u_short;
typedef __u_int u_int;
typedef __u_long u_long;
typedef __quad_t quad_t;
typedef __u_quad_t u_quad_t;
typedef __fsid_t fsid_t;
#line 44 "/usr/include/sys/types.h"
typedef __loff_t loff_t;
#line 48 "/usr/include/sys/types.h"
typedef __ino_t ino_t;
#line 60 "/usr/include/sys/types.h"
typedef __dev_t dev_t;
#line 65 "/usr/include/sys/types.h"
typedef __gid_t gid_t;
#line 70 "/usr/include/sys/types.h"
typedef __mode_t mode_t;
#line 75 "/usr/include/sys/types.h"
typedef __nlink_t nlink_t;
#line 80 "/usr/include/sys/types.h"
typedef __uid_t uid_t;
#line 98 "/usr/include/sys/types.h"
typedef __pid_t pid_t;
#line 104 "/usr/include/sys/types.h"
typedef __id_t id_t;
#line 115 "/usr/include/sys/types.h"
typedef __daddr_t daddr_t;
typedef __caddr_t caddr_t;
#line 122 "/usr/include/sys/types.h"
typedef __key_t key_t;
#line 59 "/usr/include/time.h"
typedef __clock_t clock_t;
#line 75 "/usr/include/time.h"
typedef __time_t time_t;
#line 91 "/usr/include/time.h"
typedef __clockid_t clockid_t;
#line 103 "/usr/include/time.h"
typedef __timer_t timer_t;
#line 150 "/usr/include/sys/types.h"
typedef unsigned long int ulong;
typedef unsigned short int ushort;
typedef unsigned int uint;
#line 194 "/usr/include/sys/types.h"
typedef int int8_t __attribute__((__mode__(__QI__)));
typedef int int16_t __attribute__((__mode__(__HI__)));
typedef int int32_t __attribute__((__mode__(__SI__)));
typedef int int64_t __attribute__((__mode__(__DI__)));
#line 200 "/usr/include/sys/types.h"
typedef unsigned int u_int8_t __attribute__((__mode__(__QI__)));
typedef unsigned int u_int16_t __attribute__((__mode__(__HI__)));
typedef unsigned int u_int32_t __attribute__((__mode__(__SI__)));
typedef unsigned int u_int64_t __attribute__((__mode__(__DI__)));
#line 205 "/usr/include/sys/types.h"
typedef int register_t __attribute__((__mode__(__word__)));
#line 45 "/usr/include/bits/byteswap.h"
__inline static unsigned int __bswap_32(unsigned int __bsx)
{
  return __builtin_bswap32(__bsx);
}

#line 109 "/usr/include/bits/byteswap.h"
__inline static __uint64_t __bswap_64(__uint64_t __bsx)
{
  return __builtin_bswap64(__bsx);
}

#line 22 "/usr/include/bits/sigset.h"
typedef int __sig_atomic_t;
#line 28 "/usr/include/bits/sigset.h"
typedef struct 
{
#line 29 "/usr/include/bits/sigset.h"
  unsigned long int __val[1024 / (8 * (sizeof(unsigned long int)))];
} __sigset_t;
#line 37 "/usr/include/sys/select.h"
typedef __sigset_t sigset_t;
#line 120 "/usr/include/time.h"
struct timespec
{
  __time_t tv_sec;
  __syscall_slong_t tv_nsec;
};
#line 30 "/usr/include/bits/time.h"
struct timeval
{
  __time_t tv_sec;
  __suseconds_t tv_usec;
};
#line 50 "/usr/include/sys/select.h"
typedef __suseconds_t suseconds_t;
#line 56 "/usr/include/sys/select.h"
typedef long int __fd_mask;
#line 67 "/usr/include/sys/select.h"
typedef struct 
{
#line 74 "/usr/include/sys/select.h"
  __fd_mask __fds_bits[1024 / (8 * ((int) (sizeof(__fd_mask))))];
} fd_set;
#line 84 "/usr/include/sys/select.h"
typedef __fd_mask fd_mask;
#line 108 "/usr/include/sys/select.h"
extern int select(int __nfds, fd_set *__restrict __readfds, fd_set *__restrict __writefds, fd_set *__restrict __exceptfds, struct timeval *__restrict __timeout);
#line 120 "/usr/include/sys/select.h"
extern int pselect(int __nfds, fd_set *__restrict __readfds, fd_set *__restrict __writefds, fd_set *__restrict __exceptfds, const struct timespec *__restrict __timeout, const __sigset_t *__restrict __sigmask);
#line 27 "/usr/include/sys/sysmacros.h"
__extension__ extern unsigned int gnu_dev_major(unsigned long long int __dev) __attribute__((__nothrow__, __leaf__, __const__));
#line 30 "/usr/include/sys/sysmacros.h"
__extension__ extern unsigned int gnu_dev_minor(unsigned long long int __dev) __attribute__((__nothrow__, __leaf__, __const__));
#line 33 "/usr/include/sys/sysmacros.h"
__extension__ extern unsigned long long int gnu_dev_makedev(unsigned int __major, unsigned int __minor) __attribute__((__nothrow__, __leaf__, __const__));
#line 228 "/usr/include/sys/types.h"
typedef __blksize_t blksize_t;
#line 235 "/usr/include/sys/types.h"
typedef __blkcnt_t blkcnt_t;
#line 239 "/usr/include/sys/types.h"
typedef __fsblkcnt_t fsblkcnt_t;
#line 243 "/usr/include/sys/types.h"
typedef __fsfilcnt_t fsfilcnt_t;
#line 60 "/usr/include/bits/pthreadtypes.h"
typedef unsigned long int pthread_t;
#line 63 "/usr/include/bits/pthreadtypes.h"
union pthread_attr_t
{
  char __size[56];
  long int __align;
};
#line 69 "/usr/include/bits/pthreadtypes.h"
typedef union pthread_attr_t pthread_attr_t;
#line 75 "/usr/include/bits/pthreadtypes.h"
typedef struct __pthread_internal_list
{
  struct __pthread_internal_list *__prev;
  struct __pthread_internal_list *__next;
} __pthread_list_t;
#line 91 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 92 "/usr/include/bits/pthreadtypes.h"
  struct __pthread_mutex_s
  {
    int __lock;
    unsigned int __count;
    int __owner;
#line 98 "/usr/include/bits/pthreadtypes.h"
    unsigned int __nusers;
#line 102 "/usr/include/bits/pthreadtypes.h"
    int __kind;
#line 104 "/usr/include/bits/pthreadtypes.h"
    short __spins;
    short __elision;
    __pthread_list_t __list;
  } __data;
#line 126 "/usr/include/bits/pthreadtypes.h"
  char __size[40];
  long int __align;
} pthread_mutex_t;
#line 131 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 132 "/usr/include/bits/pthreadtypes.h"
  char __size[4];
  int __align;
} pthread_mutexattr_t;
#line 140 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
  struct 
  {
#line 143 "/usr/include/bits/pthreadtypes.h"
    int __lock;
    unsigned int __futex;
    __extension__ unsigned long long int __total_seq;
    __extension__ unsigned long long int __wakeup_seq;
    __extension__ unsigned long long int __woken_seq;
    void *__mutex;
    unsigned int __nwaiters;
    unsigned int __broadcast_seq;
  } __data;
  char __size[48];
  __extension__ long long int __align;
} pthread_cond_t;
#line 157 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 158 "/usr/include/bits/pthreadtypes.h"
  char __size[4];
  int __align;
} pthread_condattr_t;
#line 164 "/usr/include/bits/pthreadtypes.h"
typedef unsigned int pthread_key_t;
#line 168 "/usr/include/bits/pthreadtypes.h"
typedef int pthread_once_t;
#line 175 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 178 "/usr/include/bits/pthreadtypes.h"
  struct 
  {
#line 179 "/usr/include/bits/pthreadtypes.h"
    int __lock;
    unsigned int __nr_readers;
    unsigned int __readers_wakeup;
    unsigned int __writer_wakeup;
    unsigned int __nr_readers_queued;
    unsigned int __nr_writers_queued;
    int __writer;
    int __shared;
    signed char __rwelision;
#line 192 "/usr/include/bits/pthreadtypes.h"
    unsigned char __pad1[7];
#line 195 "/usr/include/bits/pthreadtypes.h"
    unsigned long int __pad2;
#line 198 "/usr/include/bits/pthreadtypes.h"
    unsigned int __flags;
  } __data;
#line 220 "/usr/include/bits/pthreadtypes.h"
  char __size[56];
  long int __align;
} pthread_rwlock_t;
#line 225 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 226 "/usr/include/bits/pthreadtypes.h"
  char __size[8];
  long int __align;
} pthread_rwlockattr_t;
#line 234 "/usr/include/bits/pthreadtypes.h"
typedef volatile int pthread_spinlock_t;
#line 240 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 241 "/usr/include/bits/pthreadtypes.h"
  char __size[32];
  long int __align;
} pthread_barrier_t;
#line 246 "/usr/include/bits/pthreadtypes.h"
typedef union 
{
#line 247 "/usr/include/bits/pthreadtypes.h"
  char __size[4];
  int __align;
} pthread_barrierattr_t;
#line 282 "/usr/include/stdlib.h"
extern long int random(void) __attribute__((__nothrow__, __leaf__));
#line 285 "/usr/include/stdlib.h"
extern void srandom(unsigned int __seed) __attribute__((__nothrow__, __leaf__));
#line 291 "/usr/include/stdlib.h"
extern char *initstate(unsigned int __seed, char *__statebuf, size_t __statelen) __attribute__((__nothrow__, __leaf__, __nonnull__(2)));
#line 296 "/usr/include/stdlib.h"
extern char *setstate(char *__statebuf) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 304 "/usr/include/stdlib.h"
struct random_data
{
  int32_t *fptr;
  int32_t *rptr;
  int32_t *state;
  int rand_type;
  int rand_deg;
  int rand_sep;
  int32_t *end_ptr;
};
#line 315 "/usr/include/stdlib.h"
extern int random_r(struct random_data *__restrict __buf, int32_t *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 318 "/usr/include/stdlib.h"
extern int srandom_r(unsigned int __seed, struct random_data *__buf) __attribute__((__nothrow__, __leaf__, __nonnull__(2)));
#line 321 "/usr/include/stdlib.h"
extern int initstate_r(unsigned int __seed, char *__restrict __statebuf, size_t __statelen, struct random_data *__restrict __buf) __attribute__((__nothrow__, __leaf__, __nonnull__(2, 4)));
#line 326 "/usr/include/stdlib.h"
extern int setstate_r(char *__restrict __statebuf, struct random_data *__restrict __buf) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 335 "/usr/include/stdlib.h"
extern int rand(void) __attribute__((__nothrow__, __leaf__));
#line 337 "/usr/include/stdlib.h"
extern void srand(unsigned int __seed) __attribute__((__nothrow__, __leaf__));
#line 342 "/usr/include/stdlib.h"
extern int rand_r(unsigned int *__seed) __attribute__((__nothrow__, __leaf__));
#line 350 "/usr/include/stdlib.h"
extern double drand48(void) __attribute__((__nothrow__, __leaf__));
extern double erand48(unsigned short int __xsubi[3]) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 354 "/usr/include/stdlib.h"
extern long int lrand48(void) __attribute__((__nothrow__, __leaf__));
extern long int nrand48(unsigned short int __xsubi[3]) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 359 "/usr/include/stdlib.h"
extern long int mrand48(void) __attribute__((__nothrow__, __leaf__));
extern long int jrand48(unsigned short int __xsubi[3]) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 364 "/usr/include/stdlib.h"
extern void srand48(long int __seedval) __attribute__((__nothrow__, __leaf__));
extern unsigned short int *seed48(unsigned short int __seed16v[3]) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 367 "/usr/include/stdlib.h"
extern void lcong48(unsigned short int __param[7]) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 373 "/usr/include/stdlib.h"
struct drand48_data
{
  unsigned short int __x[3];
  unsigned short int __old_x[3];
  unsigned short int __c;
  unsigned short int __init;
  __extension__ unsigned long long int __a;
};
#line 384 "/usr/include/stdlib.h"
extern int drand48_r(struct drand48_data *__restrict __buffer, double *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 386 "/usr/include/stdlib.h"
extern int erand48_r(unsigned short int __xsubi[3], struct drand48_data *__restrict __buffer, double *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 391 "/usr/include/stdlib.h"
extern int lrand48_r(struct drand48_data *__restrict __buffer, long int *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 394 "/usr/include/stdlib.h"
extern int nrand48_r(unsigned short int __xsubi[3], struct drand48_data *__restrict __buffer, long int *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 400 "/usr/include/stdlib.h"
extern int mrand48_r(struct drand48_data *__restrict __buffer, long int *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 403 "/usr/include/stdlib.h"
extern int jrand48_r(unsigned short int __xsubi[3], struct drand48_data *__restrict __buffer, long int *__restrict __result) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 409 "/usr/include/stdlib.h"
extern int srand48_r(long int __seedval, struct drand48_data *__buffer) __attribute__((__nothrow__, __leaf__, __nonnull__(2)));
#line 412 "/usr/include/stdlib.h"
extern int seed48_r(unsigned short int __seed16v[3], struct drand48_data *__buffer) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 415 "/usr/include/stdlib.h"
extern int lcong48_r(unsigned short int __param[7], struct drand48_data *__buffer) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2)));
#line 427 "/usr/include/stdlib.h"
extern void *malloc(size_t __size) __attribute__((__nothrow__, __leaf__, __malloc__));
#line 429 "/usr/include/stdlib.h"
extern void *calloc(size_t __nmemb, size_t __size) __attribute__((__nothrow__, __leaf__, __malloc__));
#line 441 "/usr/include/stdlib.h"
extern void *realloc(void *__ptr, size_t __size) __attribute__((__nothrow__, __leaf__, __warn_unused_result__));
#line 444 "/usr/include/stdlib.h"
extern void free(void *__ptr) __attribute__((__nothrow__, __leaf__));
#line 449 "/usr/include/stdlib.h"
extern void cfree(void *__ptr) __attribute__((__nothrow__, __leaf__));
#line 32 "/usr/include/alloca.h"
extern void *alloca(size_t __size) __attribute__((__nothrow__, __leaf__));
#line 459 "/usr/include/stdlib.h"
extern void *valloc(size_t __size) __attribute__((__nothrow__, __leaf__, __malloc__));
#line 464 "/usr/include/stdlib.h"
extern int posix_memalign(void **__memptr, size_t __alignment, size_t __size) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 470 "/usr/include/stdlib.h"
extern void *aligned_alloc(size_t __alignment, size_t __size) __attribute__((__nothrow__, __leaf__, __malloc__, __alloc_size__(2)));
#line 476 "/usr/include/stdlib.h"
extern void abort(void) __attribute__((__nothrow__, __leaf__, __noreturn__));
#line 480 "/usr/include/stdlib.h"
extern int atexit(void (*__func)(void)) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 488 "/usr/include/stdlib.h"
extern int at_quick_exit(void (*__func)(void)) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 496 "/usr/include/stdlib.h"
extern int on_exit(void (*__func)(int __status, void *__arg), void *__arg) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 504 "/usr/include/stdlib.h"
extern void exit(int __status) __attribute__((__nothrow__, __leaf__, __noreturn__));
#line 510 "/usr/include/stdlib.h"
extern void quick_exit(int __status) __attribute__((__nothrow__, __leaf__, __noreturn__));
#line 518 "/usr/include/stdlib.h"
extern void _Exit(int __status) __attribute__((__nothrow__, __leaf__, __noreturn__));
#line 525 "/usr/include/stdlib.h"
extern char *getenv(const char *__name) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 539 "/usr/include/stdlib.h"
extern int putenv(char *__string) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 545 "/usr/include/stdlib.h"
extern int setenv(const char *__name, const char *__value, int __replace) __attribute__((__nothrow__, __leaf__, __nonnull__(2)));
#line 549 "/usr/include/stdlib.h"
extern int unsetenv(const char *__name) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 556 "/usr/include/stdlib.h"
extern int clearenv(void) __attribute__((__nothrow__, __leaf__));
#line 567 "/usr/include/stdlib.h"
extern char *mktemp(char *__template) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 580 "/usr/include/stdlib.h"
extern int mkstemp(char *__template) __attribute__((__nonnull__(1)));
#line 602 "/usr/include/stdlib.h"
extern int mkstemps(char *__template, int __suffixlen) __attribute__((__nonnull__(1)));
#line 623 "/usr/include/stdlib.h"
extern char *mkdtemp(char *__template) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 677 "/usr/include/stdlib.h"
extern int system(const char *__command);
#line 694 "/usr/include/stdlib.h"
extern char *realpath(const char *__restrict __name, char *__restrict __resolved) __attribute__((__nothrow__, __leaf__));
#line 702 "/usr/include/stdlib.h"
typedef int (*__compar_fn_t)(const void *, const void *);
#line 715 "/usr/include/stdlib.h"
extern void *bsearch(const void *__key, const void *__base, size_t __nmemb, size_t __size, __compar_fn_t __compar) __attribute__((__nonnull__(1, 2, 5)));
#line 725 "/usr/include/stdlib.h"
extern void qsort(void *__base, size_t __nmemb, size_t __size, __compar_fn_t __compar) __attribute__((__nonnull__(1, 4)));
#line 735 "/usr/include/stdlib.h"
extern int abs(int __x) __attribute__((__nothrow__, __leaf__, __const__));
extern long int labs(long int __x) __attribute__((__nothrow__, __leaf__, __const__));
#line 740 "/usr/include/stdlib.h"
__extension__ extern long long int llabs(long long int __x) __attribute__((__nothrow__, __leaf__, __const__));
#line 749 "/usr/include/stdlib.h"
extern div_t div(int __numer, int __denom) __attribute__((__nothrow__, __leaf__, __const__));
#line 751 "/usr/include/stdlib.h"
extern ldiv_t ldiv(long int __numer, long int __denom) __attribute__((__nothrow__, __leaf__, __const__));
#line 757 "/usr/include/stdlib.h"
__extension__ extern lldiv_t lldiv(long long int __numer, long long int __denom) __attribute__((__nothrow__, __leaf__, __const__));
#line 772 "/usr/include/stdlib.h"
extern char *ecvt(double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4)));
#line 778 "/usr/include/stdlib.h"
extern char *fcvt(double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4)));
#line 784 "/usr/include/stdlib.h"
extern char *gcvt(double __value, int __ndigit, char *__buf) __attribute__((__nothrow__, __leaf__, __nonnull__(3)));
#line 790 "/usr/include/stdlib.h"
extern char *qecvt(long double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4)));
#line 793 "/usr/include/stdlib.h"
extern char *qfcvt(long double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4)));
#line 796 "/usr/include/stdlib.h"
extern char *qgcvt(long double __value, int __ndigit, char *__buf) __attribute__((__nothrow__, __leaf__, __nonnull__(3)));
#line 802 "/usr/include/stdlib.h"
extern int ecvt_r(double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign, char *__restrict __buf, size_t __len) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4, 5)));
#line 805 "/usr/include/stdlib.h"
extern int fcvt_r(double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign, char *__restrict __buf, size_t __len) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4, 5)));
#line 809 "/usr/include/stdlib.h"
extern int qecvt_r(long double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign, char *__restrict __buf, size_t __len) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4, 5)));
#line 813 "/usr/include/stdlib.h"
extern int qfcvt_r(long double __value, int __ndigit, int *__restrict __decpt, int *__restrict __sign, char *__restrict __buf, size_t __len) __attribute__((__nothrow__, __leaf__, __nonnull__(3, 4, 5)));
#line 823 "/usr/include/stdlib.h"
extern int mblen(const char *__s, size_t __n) __attribute__((__nothrow__, __leaf__));
#line 826 "/usr/include/stdlib.h"
extern int mbtowc(wchar_t *__restrict __pwc, const char *__restrict __s, size_t __n) __attribute__((__nothrow__, __leaf__));
#line 830 "/usr/include/stdlib.h"
extern int wctomb(char *__s, wchar_t __wchar) __attribute__((__nothrow__, __leaf__));
#line 834 "/usr/include/stdlib.h"
extern size_t mbstowcs(wchar_t *__restrict __pwcs, const char *__restrict __s, size_t __n) __attribute__((__nothrow__, __leaf__));
#line 837 "/usr/include/stdlib.h"
extern size_t wcstombs(char *__restrict __s, const wchar_t *__restrict __pwcs, size_t __n) __attribute__((__nothrow__, __leaf__));
#line 848 "/usr/include/stdlib.h"
extern int rpmatch(const char *__response) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 859 "/usr/include/stdlib.h"
extern int getsubopt(char **__restrict __optionp, char *const *__restrict __tokens, char **__restrict __valuep) __attribute__((__nothrow__, __leaf__, __nonnull__(1, 2, 3)));
#line 911 "/usr/include/stdlib.h"
extern int getloadavg(double __loadavg[], int __nelem) __attribute__((__nothrow__, __leaf__, __nonnull__(1)));
#line 5 "/home/kiv/projects/c_ext/tests/1.c"
typedef struct A
{
#line 5 "/home/kiv/projects/c_ext/tests/1.c"
  const struct A_VTable
  {
#line 5 "/home/kiv/projects/c_ext/tests/1.c"
    const void *__parent__;
#line 5 "/home/kiv/projects/c_ext/tests/1.c"
    const char *__name__;
#line 8 "/home/kiv/projects/c_ext/tests/1.c"
    void (*destroy)(struct A *const this);
    void (*print_text)(struct A *const this, const char *fmt, ...);
  } *__vtable__;
} A;
#line 5 "/home/kiv/projects/c_ext/tests/1.c"
extern const struct A_VTable A_vtable;
extern int A_i;
extern void A_construct(struct A *const this);
extern void A_destroy(struct A *const this);
#line 10 "/home/kiv/projects/c_ext/tests/1.c"
extern void A_test();
#line 13 "/home/kiv/projects/c_ext/tests/1.c"
typedef struct B
{
#line 13 "/home/kiv/projects/c_ext/tests/1.c"
  const struct B_VTable
  {
#line 13 "/home/kiv/projects/c_ext/tests/1.c"
    const struct A_VTable *__parent__;
#line 13 "/home/kiv/projects/c_ext/tests/1.c"
    const char *__name__;
#line 8 "/home/kiv/projects/c_ext/tests/1.c"
    void (*destroy)(struct A *const this);
#line 15 "/home/kiv/projects/c_ext/tests/1.c"
    void (*print_text)(struct B *const this, const char *fmt, ...);
  } *__vtable__;
} B;
#line 13 "/home/kiv/projects/c_ext/tests/1.c"
extern const struct B_VTable B_vtable;
extern void B_construct(struct B *const this);
extern void B_print_text(struct B *const this, const char *fmt, ...);
#line 18 "/home/kiv/projects/c_ext/tests/1.c"
int A_i = 0;
#line 20 "/home/kiv/projects/c_ext/tests/1.c"
void A_construct(struct A *const this)
{
#line 20 "/home/kiv/projects/c_ext/tests/1.c"
  this->__vtable__ = & A_vtable;
  A_i++;
  printf("A::construct(i == %i)\n", A_i);
}

#line 20 "/home/kiv/projects/c_ext/tests/1.c"
const struct A_VTable A_vtable = {0, "A", A_destroy, 0};
#line 25 "/home/kiv/projects/c_ext/tests/1.c"
void A_destroy(struct A *const this)
{
#line 26 "/home/kiv/projects/c_ext/tests/1.c"
  printf("Object destroyed\n");
}

void B_print_text(struct B *const this, const char *fmt, ...)
{
#line 30 "/home/kiv/projects/c_ext/tests/1.c"
  va_list args;
  __builtin_va_start(args, fmt);
  vprintf(fmt, args);
  __builtin_va_end(args);
}

void B_construct(struct B *const this)
{
#line 37 "/home/kiv/projects/c_ext/tests/1.c"
  A_construct((struct A *const ) this);
#line 36 "/home/kiv/projects/c_ext/tests/1.c"
  this->__vtable__ = & B_vtable;
#line 38 "/home/kiv/projects/c_ext/tests/1.c"
  printf("B::construct(i == %i)\n", A_i);
}

#line 36 "/home/kiv/projects/c_ext/tests/1.c"
const struct B_VTable B_vtable = {& A_vtable, "B", A_destroy, B_print_text};
#line 41 "/home/kiv/projects/c_ext/tests/1.c"
void A_test()
{
#line 42 "/home/kiv/projects/c_ext/tests/1.c"
  printf("Test!\n");
}

B b;
A *b_ptr = (struct A *) (& b);
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
struct __lambda_0___ClosureData
{
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
  void (*__fn__)(void *const __closure__);
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
  const char *s;
};
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
static void __lambda_0__(void *const __closure__)
{
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
  struct __lambda_0___ClosureData
  {
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
    void (*__fn__)(void *const __closure__);
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
    const char *s;
  } *const __closure_data__ = __closure__;
#line 50 "/home/kiv/projects/c_ext/tests/1.c"
  printf("%s\n", __closure_data__->s);
}

#line 48 "/home/kiv/projects/c_ext/tests/1.c"
void (**make_print_func(const char *s))()
{
#line 48 "/home/kiv/projects/c_ext/tests/1.c"
  struct __lambda_0___ClosureData *const __lambda_0___data = malloc(sizeof(struct __lambda_0___ClosureData));
  __lambda_0___data->__fn__ = __lambda_0__;
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
  __lambda_0___data->s = s;
#line 49 "/home/kiv/projects/c_ext/tests/1.c"
  return (void *) __lambda_0___data;
}

#line 54 "/home/kiv/projects/c_ext/tests/1.c"
int main()
{
#line 55 "/home/kiv/projects/c_ext/tests/1.c"
  B_construct(& b);
  b_ptr->__vtable__->print_text(b_ptr, "%s\n", "Hello world!");
  b_ptr->__vtable__->destroy(b_ptr);
  A_test();
  void (**print_func)() = make_print_func("Test");
#line 54 "/home/kiv/projects/c_ext/tests/1.c"
  void (**__tmp_closure_0__)() = print_func;
#line 60 "/home/kiv/projects/c_ext/tests/1.c"
  (* __tmp_closure_0__)(__tmp_closure_0__);
  free(print_func);
  return 0;
}

