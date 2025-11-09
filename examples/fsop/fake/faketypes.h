
typedef unsigned long size_t;
typedef long __off_t;
typedef long long __off64_t;
typedef unsigned short uint16_t;
typedef signed int int32_t;
typedef int32_t wchar_t;
typedef long __mbstate_t;
/* forward decls used in the structs */
struct _IO_marker;
struct __codecvt;
struct _IO_wide_data;
struct _IO_lock_t;

/* _IO_FILE layout (LP64) - comments show requested offsets */
struct _IO_FILE {
    int32_t _flags;               /* 0x00 */
    int32_t __pad_flags;          /* padding to 8 */
    char * _IO_read_ptr;          /* 0x08 */
    char * _IO_read_end;          /* 0x10 */
    char * _IO_read_base;         /* 0x18 */
    char * _IO_write_base;        /* 0x20 */
    char * _IO_write_ptr;         /* 0x28 */
    char * _IO_write_end;         /* 0x30 */
    char * _IO_buf_base;          /* 0x38 */
    char * _IO_buf_end;           /* 0x40 */
    char * _IO_save_base;         /* 0x48 */
    char * _IO_backup_base;       /* 0x50 */
    char * _IO_save_end;          /* 0x58 */
    struct _IO_marker * _markers; /* 0x60 */
    struct _IO_FILE * _chain;     /* 0x68 */
    int32_t _fileno;              /* 0x70 */
    int32_t _flags2;              /* 0x74 */
    __off_t _old_offset;          /* 0x78 */
    uint16_t _cur_column;         /* 0x80 */
    char _vtable_offset;          /* 0x82 */
    char _shortbuf[1];            /* 0x83 */
    /* padding -> 0x88 */
    struct _IO_lock_t * _lock;    /* 0x88 */
    __off64_t _offset;            /* 0x90 */
    struct __codecvt * _codecvt;/* 0x98 */
    struct _IO_wide_data * _wide_data; /* 0xa0 */
    struct _IO_FILE * _freeres_list; /* 0xa8 */
    void * _freeres_buf;          /* 0xb0 */
    size_t __pad5;                /* 0xb8 */
    int32_t _mode;                /* 0xc0 */
    char _unused2[0x14];          /* 0xc4 */
    /* (additional padding/fields may follow in real glibc versions) */
};

/* _IO_wide_data layout (LP64) */
struct _IO_wide_data {
    wchar_t * _IO_read_ptr;       /* 0x00 */
    wchar_t * _IO_read_end;       /* 0x08 */
    wchar_t * _IO_read_base;      /* 0x10 */
    wchar_t * _IO_write_base;     /* 0x18 */
    wchar_t * _IO_write_ptr;      /* 0x20 */
    wchar_t * _IO_write_end;      /* 0x28 */
    wchar_t * _IO_buf_base;       /* 0x30 */
    wchar_t * _IO_buf_end;        /* 0x38 */
    wchar_t * _IO_save_base;      /* 0x40 */
    wchar_t * _IO_backup_base;    /* 0x48 */
    wchar_t * _IO_save_end;       /* 0x50 */
    __mbstate_t _IO_state;     /* 0x58 */
    __mbstate_t _IO_last_state;/* 0x60 */
    unsigned char _codecvt[0x70];    /* 0x68 */
    /* note: size of _codecvt and layout may vary by libc */
    wchar_t _shortbuf[1];         /* expected near 0xd8 in your layout */
    void * _wide_vtable;          /* expected near 0xe0 */
};
struct _IO_jump_t
{
    size_t __dummy;
    size_t __dummy2;
    long * __finish;
    long * __overflow;
    long * __underflow;
    long * __uflow;
    long * __pbackfail;
    long * __xsputn;
    long * __xsgetn;
    long * __seekoff;
    long * __seekpos;
    long * __setbuf;
    long * __sync;
    long * __doallocate;
    long * __read;
    long * __write;
    long * __seek;
    long * __close;
    long * __stat;
    long * __showmanyc;
    long * __imbue;
};

struct _IO_FILE_plus
{
  struct _IO_FILE file;
  const struct _IO_jump_t *vtable;
};