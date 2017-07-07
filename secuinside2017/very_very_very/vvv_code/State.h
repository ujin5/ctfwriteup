#ifndef __STATE_H__
#define __STATE_H__
#include "Type.h"
#define STATE_MAX 0x200
class State{
    private:
        UINT64 *Defined[STATE_MAX];
        UINT32 Intger[100];
        UINT64 numOf;
        UINT64 int_numOf;
    public:
        State();
        UINT64 NumOf();
        BOOL SetItem(UINT64 *src);
        BOOL SetIntItem(UINT32 value);
        //virtual DelItem(UINT64 index);
        virtual Object* GetItem(UINT64 index);
        virtual UINT32 GetIntItem(UINT64 index);
        //virtual PrintItem(Object *src);
        BOOL IntBox(UINT64 dest_index, UINT64 src_index, UINT64 index);
        BOOL ObjectBox(UINT64 dest_index, UINT64 src_index, UINT64 index);
//        virtual Clear();
        ~State();
};
#endif
