#include <iostrem>
#include <memory.h>
#include <vector>
#define MISSNGITEM 0x20172017

#define ARRAY 0x1
#define INTGER 0x2
#define STRING 0x3
class Object{
  public:
    Object(){};
  protected:
    void * buffer;
    unsigned int size;
    int type_id;
}
class Array public:Object{
  private:
    int length;
    int numOf;
  public:
    Array(unsigned int size){
      this.buffer = (void *) malloc(size);
      this.size = size;
      this.length = size;
      this.type_id = ARRAY;
    }
    Array(){
      this.buffer = (void *) malloc(0x8);
      this.size = 0x8;
      this.length = 1;
      this.type_id = ARRAY;
    }
    virtual void expand(unsigned int size){
      this.buffer = (void *) realloc(this.buffer,this.8*(this.length+size));
      this.size += size;
    }
    virtual bool Add_Element(int index, Object *src){
      if(index<0)
        return false;
      else if(index>size){
        expand(index-size);
        this.buffer[index] = src;
      }
      else
        this.buffer[index] = src;
    }
}
class String public:Object{
  private:
    int length;
  public:
    String(char * src){
      this.buffer = (void *)malloc(strlen(src));
      memcpy(this.buffer,src,strlen(src));
      this.length = strlen(src);
      this.type_id = STRING;
    }
    virtual void clear(){
      free(this.buffer);
      this.buffer = NULL;
      this.length = 0;
    }
}
