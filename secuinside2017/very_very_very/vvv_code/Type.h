#ifndef __TYPE_H__
#define __TYPE_H__

#define MISSING 0x80000002
#define Type_Array 0x10001000
#define Type_String 0x20002000
#define Type_BigNumber 0x30003000
#define Type_NativeIntArray 0x1
#define Type_NativeArray 0x2

typedef void BUFFER;
typedef unsigned int UINT32;
typedef int INT32;
typedef unsigned long long UINT64;
typedef long long INT64;
typedef unsigned int BOOL;
class Object {
    public: 
        UINT32 type_id;
        virtual BOOL gap();
};
class Array: public Object {
    public:
        UINT32 Array_type;
        UINT64 length;
        UINT64 capacity;
        Array();
        static BOOL Type(Object *src);
        UINT32 GetType();
        virtual BOOL gap();
        BOOL expand(UINT64 n);
        ~Array();
};
class NativeIntArray: public Array{
    public:
        UINT32 *buf;
        NativeIntArray(UINT64 n);
        BOOL init();
        static BOOL Type(Array *array);
        virtual BOOL SetItem(UINT64 index, UINT32 value);
        UINT32 GetItem(UINT64 index);
        BOOL PrintAll();
        ~NativeIntArray();
};
class NativeArray: public Array{
    public:
        UINT64 *buf;
        NativeArray(UINT64 n);
        BOOL init();
        static BOOL Type(Array *array);
        NativeArray * Concat(NativeArray *array);
        virtual BOOL SetObjectItem(UINT64 index, Object *value);
        virtual BOOL SetIntItem(UINT64 index, UINT32 value);
        UINT64 GetItem(UINT64 index);
        BOOL PrintAll();
        ~NativeArray();
};
class String: public Object{
    private:
        char *buf;
        UINT64 length;
    public:
        String(char *src);
        static BOOL Type(Object *src);
        virtual UINT64 EditString(char *src);
        BOOL Print();
        ~String();
};
class BigNumber: public Object{
    private:
        UINT64 ability;
    public:
        BigNumber(UINT64 ability);
        static BOOL Type(Object *src);
        virtual BOOL Add(BigNumber *operand);
        virtual BOOL Sub(BigNumber *operand);
        virtual BOOL Mul(BigNumber *operand);
        virtual BOOL Div(BigNumber *opernad);
        BOOL Print();
        ~BigNumber();
};
#endif
