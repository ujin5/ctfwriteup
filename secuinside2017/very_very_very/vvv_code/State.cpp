#include "Type.h"
#include "State.h"

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cstring>
State::State(){
  numOf = 0;
  int_numOf = 0;
  for(int i = 0; i < STATE_MAX; i++)
    Defined[i] = (UINT64 *)0x8000000280000002;
  for(int j = 0; j < 100; j++)
    Intger[j] = 0x80000002;
}
State::~State(){}
UINT64 State::NumOf(){ return this->numOf; }
BOOL State::SetItem(UINT64 *src){
  for(int i = 0; i < STATE_MAX; i++){
    if(Defined[i] == (UINT64 *)0x8000000280000002){
      this->numOf++;
      Defined[i] = src;
      return i;
    }
  }
  std::cout<<"exceed "<<std::endl;
  exit(-1);
}
BOOL State::SetIntItem(UINT32 src){
  for(int i = 0; i < 100; i++){
    if(Intger[i]==0x80000002){
      this->int_numOf++;
      Intger[i] = src;
      return i;
    }
  }
  std::cout<<"exceed "<<std::endl;
  exit(-1);
}
Object *State::GetItem(UINT64 index){
  if(index > numOf){
    std::cout<<"OOB error\n"<<std::endl;
    exit(-1);
  }
  return (Object*)Defined[index];
}
UINT32 State::GetIntItem(UINT64 index){
  if(index > int_numOf){
    std::cout<<"OOB error\n"<<std::endl;
    exit(-1);
  }
  return Intger[index];
}
BOOL State::IntBox(UINT64 dest_index, UINT64 src_index, UINT64 index){
  if(index > 100){
    std::cout<<"Too Long :( \n"<<std::endl;
    exit(-1);
  }
  Array * dest = dynamic_cast<Array*>(this->GetItem(dest_index));
  
  if(dest){
    if(NativeIntArray::Type(dest)){
      return ((NativeIntArray *)dest)->SetItem(index, this->GetIntItem(src_index));
    }
    else if(NativeArray::Type(dest)){
      return ((NativeArray *)dest)->SetIntItem(index,this->GetIntItem(src_index));
    }
    else{
      std::cout<<"Type Confusion ! \n"<<std::endl;
      exit(-1);
    }
  }
  else
    return 0;
}
BOOL State::ObjectBox(UINT64 dest_index, UINT64 src_index, UINT64 index){
  if(index > 100){
    std::cout<<"Too Long :( \n"<<std::endl;
    exit(-1);
  }
  Array *dest = dynamic_cast<Array*>(this->GetItem(dest_index));
  if(dest){
    if(NativeIntArray::Type(dest)){
      std::cout<<"we don't support ConvertToArray\n"<<std::endl;
      exit(-1);
    }
    else if(NativeArray::Type(dest)){
      return ((NativeArray *)dest)->SetObjectItem(index,this->GetItem(src_index));
    }
    else{
      std::cout<<"Type Confusion ! \n"<<std::endl;
      exit(-1);
    }
  }
  return 0;
}
