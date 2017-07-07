#ifndef __USER_H__
#define __USER_H__
#include <stdint.h>
class Music;
class Box;
template <class T>
class Object{
  public:
    void INC_REF( ){
      this->ref_count++;
    }
    void DEC_REF( ){
      this->ref_count--;
    }
    Object( T * ptr ){
      this->ref_count = 1;
      this->ptr = ptr;
    }
    ~Object( ){
      delete ptr;
    };
    unsigned int GET_REF( ){
      return this->ref_count;
    }
    T * GET_PTR( ){
      return this->ptr;
    }
  private:
    T * ptr; 
    unsigned int ref_count;
};
template <class T>
class Smart_ptr{
  public:
    Smart_ptr( ){
      this->ptr = 0;
    }
    ~Smart_ptr( ){
      this->Remove_ref();
    }
    Smart_ptr( T * ptr ){
      this->object = new Object<T>( ptr );
    }
    Smart_ptr( const Smart_ptr<T>& op ){
      this->object = op.object;
      this->object->INC_REF();
    }
    
		bool operator!=(const Smart_ptr<T>& other) const {
			return this->object != other.object;
		}
    Smart_ptr<T>& operator=( const Smart_ptr<T>& op){
      if( this->object ){
        this->Remove_ref();
      }
      this->object = op.object;
      this->object->INC_REF();
      return *this;
    }
    Smart_ptr<T>& operator=( Smart_ptr<T> *op){
      if( this->object ){
        this->Remove_ref();
      }
      this->object = op->object;
      this->object->INC_REF();
      return *this;
    }
    T * operator->( ){
      return this->object->GET_PTR( );
    }
    void Remove_ref( ){
      this->object->DEC_REF();
      if( this->object->GET_REF() == 0 ){
        delete this->object;
      }
    }
    Object<T> * object;
};


class Item{
  public:
    bool CheckItem( char * id, char * password );
    char * GetName( );
    uint32_t GetType( );
  protected:
    char * name;
    char * id;
    char * password;
    uint32_t type;
};
class User: public Item{
  public:
    User();
    ~User();
    bool MakeBox( );
    bool DeleteBox( uint32_t index ); 
    bool BuyMusic( Smart_ptr<Music> * Item );
    bool PutInBox( uint32_t index );
    bool BoxToBox( uint32_t dest, uint32_t src );
    bool DeleteMusic( uint32_t index );
    bool BoxList( );
    bool MusicList( );
  private:
    Smart_ptr<Box> * play_box[32] = { 0, };
    Smart_ptr<Music> * music_list[32] = { 0, };
    uint32_t numOfmusic;
};
class Composer: public Item {
  public:
    Composer( );
    ~Composer( );
    bool WriteMusic( );
    bool DeleteMusic( );
    bool EditProfile( );
    bool EditMusic( uint32_t index );    
  private:
    char * profile;
    uint32_t numOfmusic;
};
class Music{
  public:
    Music( char * song_name, char * song_lyrics, Composer * composer );
    ~Music( );
    Composer * GetComposer( );
    char * GetName( );
    char * GetLyrics( );
  private:
    char * name;
    char * lyrics;
    uint32_t fame;
    Composer * composer;
};
class Box{
  public:
    Box( char * name );
    ~Box( );
    bool AddMusic( Smart_ptr<Music> * Item );
    bool DeleteMusic( uint32_t index );
    Smart_ptr<Music> * GetMusic( uint32_t index );
    bool Put( uint32_t index, Smart_ptr<Music> * Item );
    bool List( );
    char * GetName( );
    uint32_t GetNum( );
  private:
    Smart_ptr<Music> * music_list[32] = { 0, };
    char * name;
    uint32_t num;
};
uint32_t readline( char * buf, uint32_t length );
extern Smart_ptr<Music> * Very_Chart[1024];
#endif
