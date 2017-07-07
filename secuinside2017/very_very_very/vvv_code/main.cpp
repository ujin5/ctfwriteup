#include <stdlib.h>
#include <stdio.h>
#include <cstring>
#include <iostream>
#include "State.h"
#include "Type.h"
#include "Utils.h"
State *state;
BOOL DefineVariable();
BOOL UsingVariable();
int main(){
    char buf[100];
    state = new State();
    while(1){
        memset(buf,0x00,100);
        ReadLine(1,buf);
        switch(*buf){
            case 0x20:{
                DefineVariable();
            }
                break;
            case 0x17:{
                UsingVariable();
            }
                break;
            case 0x00:{
                delete state;
                return 0;
            }break;
            default:{
                exit(-1);
            }
        }
    }
}
BOOL UsingVariable(){
    char buf[100];
    if(!state->NumOf())
        return false;
    memset(buf,0x00,100);
    ReadLine(1,buf);
    switch(*buf){
        case 0x13:{              // IntBox
            ReadLine(8,buf);    // dest index
            UINT64 dest_index = *(UINT64*) buf;
            ReadLine(8,buf);    // src index
            UINT64 src_index = *(UINT64*) buf;
            ReadLine(8,buf);    // index
            UINT64 index = *(UINT64*) buf;
            state->IntBox(dest_index,src_index,index);
            }break;
        case 0x37:{              // Box
            ReadLine(8,buf);    // dest index
            UINT64 dest_index = *(UINT64*) buf;
            ReadLine(8,buf);    // src index
            UINT64 src_index = *(UINT64*) buf;
            ReadLine(8,buf);    // index
            UINT64 index = *(UINT64*) buf;
            state->ObjectBox(dest_index,src_index,index);
            }break;
        case 0x11:{              // Output
            ReadLine(8,buf);    // src index
            UINT64 src_index = *(UINT64*) buf;
            ReadLine(8,buf);    // index
            UINT64 index = *(UINT64*) buf;
            Object *temp = state->GetItem(src_index);
            if(!Array::Type(temp))
                return 0;
            Array *pSrcArray = reinterpret_cast<Array*>(temp);
            if(NativeArray::Type(pSrcArray)){
                UINT64 Get = ((NativeArray*)pSrcArray)->GetItem(index);
                if(Get & (UINT64)0x1000000000000000)
                    state->SetIntItem((UINT32)Get);
                else if((UINT32)Get == (UINT32)MISSING )
                    return 0;
                else {
                    state->SetItem((UINT64 *) Get);
                }
              }
             else{
                UINT32 Get = ((NativeIntArray*)pSrcArray)->GetItem(index);
                state->SetIntItem(Get);
             }
            }break;
        case 0x33:{             // Concat
            ReadLine(8,buf);    // dest index
            UINT64 dest_index = *(UINT64*) buf;
            Object * dst = state->GetItem(dest_index);
            if(!Array::Type(dst)){
              std::cout<<"Concat is Array function \n"<<std::endl;
              exit(-1);
            }
            if(!NativeArray::Type((Array *)dst)){
                std::cout<<"we don't support ConvertToArray \n"<<std::endl;
                exit(-1);
            }
            NativeArray *temp = reinterpret_cast<NativeArray*>(dst);
            ReadLine(8,buf);    // src index
            UINT64 src_index = *(UINT64*) buf;
            Object *src =  state->GetItem(src_index);
            if(!Array::Type(src)){
              std::cout<<"Concat is Array function \n"<<std::endl;
              exit(-1);
            }
            NativeArray *src_ = reinterpret_cast<NativeArray*>(src);
            NativeArray *pDestArray = temp->Concat(src_);
            state->SetItem((UINT64*)pDestArray);
            }break;
        case 0x77:{             // BigNumber Function
            ReadLine(8,buf);
            UINT64 dest_index = *(UINT64*) buf;
            Object *temp = state->GetItem(dest_index);
            if(!BigNumber::Type(temp)){
              exit(-1);
            }
            BigNumber *dst = reinterpret_cast<BigNumber*>(temp);
            ReadLine(8,buf);    // src index
            UINT64 src_index = *(UINT64*) buf;
            BigNumber *src = reinterpret_cast<BigNumber*>(state->GetItem(src_index));
            ReadLine(1,buf);
            switch(*buf){
                case 0x1:{
                    dst->Add(src);
                    }break;
                case 0x2:{
                    dst->Sub(src);
                    }break;
                case 0x3:{
                    dst->Mul(src);
                    }break;
                case 0x4:{
                    dst->Div(src);
                    }break;
                default:{
                    }break;
                    
            }
            }break;
         case 0x22:{
              ReadLine(8,buf);
              UINT64 index = *(UINT64 *)buf;
              Object *temp = state->GetItem(index);
              if(Array::Type(temp)){
                  Array *array = reinterpret_cast<Array*>(temp);
                  if(NativeArray::Type((NativeArray*)array))
                      ((NativeArray*)array)->PrintAll();
                  else
                      ((NativeIntArray*)array)->PrintAll();
              }
              else if(String::Type(temp)){
                  String *str = reinterpret_cast<String*>(temp);
                  str->Print();
              }
              else if(BigNumber::Type(temp)){
                  BigNumber *bnum = reinterpret_cast<BigNumber*>(temp);
                  bnum->Print();
              }
              else{
                  return false;
              }
            }break;
         default:{
            }break;
      }
    return true;
}
BOOL DefineVariable(){
    if(state->NumOf() == (STATE_MAX-1))
        return false;
    char buf[0x100];
    memset(buf,0x00,0x100);
    ReadLine(4,buf);
    if( *(UINT32*)buf == 0x10001000) {  // Array
        ReadLine(1,buf);
        switch(*buf){
            case 0x20:{ // Int Array
                ReadLine(8,buf);
                if( *(UINT64*)buf > 100){
                    std::cout<<"Too Long..."<<std::endl;
                    exit(-1);
                }
                UINT64 idx = state->SetItem((UINT64*)new NativeIntArray(*(UINT64*) buf));
                std::cout<<"Box index : ["<<idx<<"]"<<std::endl;
            }
                break;
            case 0x17:{ // Array
                ReadLine(8,buf);
                if( *(UINT64*)buf > 100){
                    std::cout<<"Too Long..."<<std::endl;
                    exit(-1);
                }
                UINT64 idx = state->SetItem((UINT64*)new NativeArray(*(UINT64*) buf));
                std::cout<<"Box index : ["<<idx<<"]"<<std::endl;
            }
                break;
            default:{
                std::cout<<"We don't support FloatArray'"<<std::endl;
                exit(-1);
            }
        }
    }
    else if( *(UINT32*)buf == 0x20002000){ // String
        ReadLine(100,buf);
        UINT64 idx = state->SetItem((UINT64*)new String(buf));
        std::cout<<"Box index : ["<<idx<<"]"<<std::endl;
    }
    else{
        if(*(UINT32*)buf > 0x80000000){
            UINT64 idx = state->SetItem((UINT64*)new BigNumber( *(UINT64*) buf ) );
            std::cout<<"Box index : ["<<idx<<"]"<<std::endl;
        }
        else{
            UINT64 idx = state->SetIntItem( *(UINT32*) buf );
            std::cout<<"IntBox index : ["<<idx<<"]"<<std::endl;
        }
    }
}
