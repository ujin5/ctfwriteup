#include "Type.h"
#include <iostream>
#include <cstring>
#include <stdlib.h>
#include <stdio.h>
BOOL Object::gap(){
  return 0;
}
Array::Array(){}
Array::~Array(){}
BOOL Array::Type(Object *src){
    return (src->type_id == Type_Array);
}
BOOL Array::gap(){
  return 0;
}
UINT32 Array::GetType(){
  return Array_type;
}
BOOL Array::expand(UINT64 n){
    if(NativeIntArray::Type(this)){
        ((NativeIntArray *)this)->buf = (UINT32 *)malloc(sizeof(UINT32) * (n));
        length = n;
        capacity = n;
        return true;
    }
    else{
        ((NativeArray *)this)->buf = (UINT64 *)malloc(sizeof(UINT64) * (n));
        length = n;
        capacity = n;
        return true;
    }
    return false;
}
NativeIntArray::NativeIntArray(UINT64 n){
    buf = (UINT32 *)malloc(sizeof(UINT32) * n);
    length = 0;
    capacity = n;
    this->init();
    Array_type = Type_NativeIntArray;
    type_id = Type_Array;    
}
NativeIntArray::~NativeIntArray(){
    free(buf);
}
BOOL NativeIntArray::init(){
    for(int i = 0 ; i < this->capacity ; i++){
        this->buf[i] = (UINT32) 0x80000002;
    }
}
BOOL NativeIntArray::SetItem(UINT64 index, UINT32 value){
  if(index > 0){
      if(index < capacity){
          buf[index-1] = value;
          if(index > length)
            length = index;
      }
      else{
          this->expand(index);
          buf[index-1] = value;
      }
      return true;
  }
  else 
      return false;
}
UINT32 NativeIntArray::GetItem(UINT64 index){
  if(index > 0){
      if(index < length)
          return buf[index-1];
      else
          return MISSING;
   }
   else{
      exit(-1);
   }
}
BOOL NativeIntArray::PrintAll(){
    std::cout<<"[";
    for(int i = 0; i<length; i++){
        if(buf[i] == MISSING)
            std::cout<<" Undefined,";
        else
            std::cout<<buf[i]<<",";
    }
    std::cout<<"]\n"<<std::endl;
    return true;
}
BOOL NativeIntArray::Type(Array *array){
    return (array->GetType() == Type_NativeIntArray);
}
NativeArray::NativeArray(UINT64 n){
    buf = (UINT64 *)malloc(sizeof(UINT64) * n);
    length = 0;
    capacity = n;
    this->init();
    Array_type = Type_NativeArray;
    type_id = Type_Array;    
}
NativeArray::~NativeArray(){
    free(buf);
}
BOOL NativeArray::init(){
    for(int i = 0 ; i < this->capacity ; i++){
        this->buf[i] = (UINT64) 0x8000000280000002;
    }
}
BOOL NativeArray::SetObjectItem(UINT64 index, Object *value){
  if(index > 0){
      if(index < capacity){
          buf[index-1] = (UINT64)value;
          if(index > length)
            length = index;
      }
      else{
          this->expand(index);
          buf[index-1] = (UINT64)value;
      }
      return true;
  }
  else 
      exit(-1);
}
BOOL NativeArray::SetIntItem(UINT64 index, UINT32 value){
  if(index > 0){
      if(index < capacity){
          if(index > length)
            length = index;
          buf[index-1] = (UINT64)( 0x1000000000000000 | value );
      }
      else{
          this->expand(index);
          buf[index-1] = (UINT64)( 0x1000000000000000 | value );
      }
      return true;
  }
  else 
      exit(-1);
}
UINT64 NativeArray::GetItem(UINT64 index){
  if(index > 0){
      if(index < length)
          return buf[index-1];
      else
          return MISSING;
  }
  else 
      exit(-1);
}
BOOL NativeArray::PrintAll(){
    std::cout<<"[";
    for(int i = 0; i<length ; i++){
        if((UINT32)(buf[i]) == (UINT32)MISSING)
            std::cout<<" Undefined,";
        else if(buf[i] & (UINT64)0x1000000000000000){
            std::cout<<(UINT32)buf[i]<<",";
        }
        else{
            std::cout<<" [Object],";
        }
    }
    std::cout<<"]\n"<<std::endl;
    return true;
}
BOOL NativeArray::Type(Array *array){
    return (array->GetType() == Type_NativeArray);
}
NativeArray * NativeArray::Concat(NativeArray *array){
    NativeArray *pDestArray = new NativeArray(length + array->length);
    pDestArray->length = length + array->length;
    memcpy(pDestArray->buf, buf, sizeof(UINT64)*length);
    memcpy(pDestArray->buf+length, array->buf, sizeof(UINT64)*array->length);
    return pDestArray;
}
String::String(char *src){
   buf = (char *)malloc(strlen(src)+1);
  strncpy(buf,src,strlen(src));
   length = strlen(src); 
   type_id = Type_String;
}
BOOL String::Type(Object *src){
    return (src->type_id == Type_String);
}
UINT64 String::EditString(char *src){
    UINT64 src_length = strlen(src);
    if(src_length <= length)
        strncpy(buf,src,src_length);
    else{
        length = src_length;
        buf = (char *)malloc(src_length + 1);
        strncpy(buf,src,src_length);
   }
   return src_length;
}
BOOL String::Print(){
   std::cout<<"\""<<buf<<"\""<<std::endl; 
   return true;
}
String::~String(){
    free(buf);
}
BigNumber::BigNumber(UINT64 ability){
    type_id = Type_BigNumber;
    this->ability = ability;
}
BOOL BigNumber::Type(Object *src){
    return (src->type_id == Type_BigNumber);
}
BOOL BigNumber::Add(BigNumber *operand){
    ability += operand->ability;
    return true;
}
BOOL BigNumber::Sub(BigNumber *operand){
    ability -= operand->ability;
    return true;
}
BOOL BigNumber::Mul(BigNumber *operand){
    ability *= operand->ability;
    return true;
}
BOOL BigNumber::Div(BigNumber *operand){
    ability /= operand->ability;
    return true;
}
BOOL BigNumber::Print(){
    std::cout<<"["<<this->ability<<"]"<<std::endl;
}
BigNumber::~BigNumber(){
}
