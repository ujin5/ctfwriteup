#include "User.h"
#include <stdint.h>
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
uint32_t read_delim( uint32_t fd, char *buf, char delim, uint32_t maxlen )
{ 
  uint32_t index = 0;
  char c;

  if ( buf == NULL ) {
    return 0;
  }

  while ( index < maxlen ) {
    if ( read( fd, &c, 1) <= 0 ) {
      std::cout<<"[ERROR] failed to read bytes\n"<<std::endl;
      exit(0);
    }

    if ( c == delim ) {
      return index;
    }

    buf[index] = c;

    index++;
  }

  return index;
}
uint32_t readline( char * buf, uint32_t length ){
	return read_delim( 0, buf, '\n', length);
}
bool Item::CheckItem( char * id, char * password){
  if( !strcmp( this->id, id ) ){
    if( !strcmp( this->password, password ) )
      return true;
  }
  return false;
}
char * Item::GetName( ){ return this->name; }
uint32_t Item::GetType( ){ return this->type; }
User::User( ){
  char id[256];
  char password[256];
  char name[256];
  memset( id, 0x00, 256 );
  memset( password, 0x00, 256 );
  memset( name, 0x00, 256 );
  memset( this->play_box , 0x00, sizeof( Smart_ptr<Box> ) );
  memset( this->music_list , 0x00, sizeof( Smart_ptr<Music> ) );
  this->numOfmusic = 0;
  this->type = 1;

  std::cout<< " ID : ";
  readline( id, 256 - 1 );
  std::cout<< " PW : ";
  readline( password, 256 - 1 );
  
  uint32_t id_len = strlen( id );
  uint32_t pw_len = strlen( password );
  this->id = new char[ id_len + 1 ];
  this->password = new char[ pw_len + 1 ];
  
  strncpy( this->id, id, id_len );
  this->id[id_len] = '\0';
  strncpy( this->password, password, pw_len );
  this->password[pw_len] = '\0';
  std::cout<< " Name : ";
  readline( name, 256 - 1 );
  
  uint32_t name_len = strlen( name );
  
  this->name = new char[ name_len + 1];
  
  strncpy( this->name, name, name_len );
  this->name[name_len] = '\0';
} 

bool User::MakeBox( ){
  char name[256] = { 0, };
  std::cout<<"Box Name :";
  readline( name, 256 - 1 );
  for( uint32_t i = 0; i < 32; i++ ){
    if( !this->play_box[i] ){
      this->play_box[i] = new Smart_ptr<Box>(new Box( name ));
      return true;  
     }
  }
  return false;
}
bool User::DeleteBox( uint32_t index ){
  if( index < 32){
    if( !this->play_box[index] )
      return false;
    delete this->play_box[index];
    this->play_box[index] = NULL;
    return true;
  }
  return false;
}
bool User::BuyMusic( Smart_ptr<Music> * Item ){
  for( uint32_t i = 0; i < 32; i++ ){
    if( !this->music_list[i] ){
      this->music_list[i] = new Smart_ptr<Music>(*Item);
      this->numOfmusic++;
      return true;  
     }
  }
  return false;
}
bool User::PutInBox( uint32_t index ){
  uint32_t src = 0;
  if( index < 32 && this->play_box[index] ){
    std::cout<< " What will you put in the box? > ";
    std::cin>>src;
    if( this->music_list[src] ){
      (*this->play_box[index])->AddMusic( this->music_list[src] );
    }
    return false;
  }
  return false;
}
bool User::BoxToBox( uint32_t dest, uint32_t src ){
  uint32_t dest_index = 0;
  uint32_t src_index = 0;
  if( dest < 32 && src < 32){
    if( this->play_box[dest] && this->play_box[src] ){
      std::cout<< " What will you copy in the box? >"<<std::endl;
      std::cout<<" x :";
      std::cin>>src_index;
      std::cout<<" y :";
      std::cin>>dest_index;
      return (*this->play_box[dest])->Put( dest_index, (*this->play_box[src])->GetMusic( src_index ));
    }
    return false;
  }
  return false;
}
bool User::BoxList( ){
  for( uint32_t i = 0; i < 32; i++){
    Smart_ptr<Box> * tmp = this->play_box[i];
    if( tmp ){
      std::cout<< i <<". "<<(*tmp)->GetName( )<<std::endl;
      std::cout<<"----------------------------"<<std::endl;
      (*tmp)->List( );
      std::cout<<"----------------------------"<<std::endl;
    }
  }
  return true;
}
bool User::MusicList( ){
  for( uint32_t i = 0; i < 32; i++){
    Smart_ptr<Music> * tmp = this->music_list[i];
    if( tmp ){
      std::cout<< i <<". "<<(*tmp)->GetName( )<<std::endl;
      std::cout<< "Lyrics : "<<(*tmp)->GetLyrics( )<<std::endl;
    }
  }
  return true;
}
bool User::DeleteMusic( uint32_t index ){
  if( index < 32 && this->music_list[index]){
    delete music_list[index];
    music_list[index] = NULL;
    this->numOfmusic--;
    return true;
  }
  return false;
}
Composer::Composer( ){
  char id[256];
  char password[256];
  char name[256];
  char profile[256];
  memset( id, 0x00, 256 );
  memset( password, 0x00, 256 );
  memset( name, 0x00, 256 );
  memset( profile, 0x00, 256 );
  this->numOfmusic = 0;
  this->type = 2;

  std::cout<< " ID : ";
  readline( id, 256 - 1 );
  std::cout<< " PW : ";
  readline( password, 256 - 1);
  
  uint32_t id_len = strlen( id );
  uint32_t pw_len = strlen( password );
  this->id = new char[ id_len + 1 ];
  this->password = new char[ pw_len + 1 ];
  
  strncpy( this->id, id, id_len );
  strncpy( this->password, password, pw_len );
  this->id[id_len] = '\0';
  this->password[pw_len] = '\0';
  std::cout<< " Name : ";
  readline( name, 256 - 1);
  
  uint32_t name_len = strlen( name );
  
  this->name = new char[ name_len + 1];
  
  strncpy( this->name, name, name_len );
  this->name[name_len] = '\0';
  std::cout<< " Profile : "; 
  readline( profile, 256 - 1);

  uint32_t profile_len = strlen( profile );
  
  this->profile = new char[ profile_len + 1 ];

  strncpy( this->profile, profile, profile_len );
  this->profile[profile_len] = '\0';
}
bool Composer::WriteMusic( ){
  char song_name[32] = { 0, };
  char song_lyrics[64] = { 0, };
  std::cout<<" Song Name : ";
  readline( song_name, 32 - 1 );
  std::cout<<" Song Lyrics : ";
  readline( song_lyrics, 64 - 1 );
  for( int i = 0; i < 1024; i++ ){
    if( !Very_Chart[i] ){
      Very_Chart[i] = new Smart_ptr<Music>(new Music( song_name, song_lyrics, this));
      this->numOfmusic++;
      std::cout<<" Success"<<std::endl;
      return true;
    }
  }
  std::cout<<" Very_Chart is full"<<std::endl;
  return false;
}
bool Composer::DeleteMusic( ){
  uint32_t song_index = 0;
  std::cout<<" Song Index : ";
  std::cin>>song_index;
  if( song_index < 1024 && Very_Chart[song_index] ){
    if( (*Very_Chart[song_index])->GetComposer( ) == this ){
      delete Very_Chart[song_index];
      Very_Chart[song_index] = NULL;
      std::cout<<" Ok, Success "<<std::endl;
      return true;
    }
  }
  std::cout<<" Fail "<<std::endl;
  return false;
}
bool Composer::EditProfile( )
{
  uint32_t length = strlen( this->profile );
  std::cout<<" Edit Profile : ";
  readline( this->profile, length);
  return true;
}
bool Composer::EditMusic( uint32_t index)
{
  if( index < 1024 && Very_Chart[index] ){
      uint32_t lyrics_len = strlen((*Very_Chart[index])->GetLyrics( ));
      readline( (*Very_Chart[index])->GetLyrics( ), lyrics_len );
      std::cout<<" Ok, Success "<<std::endl;
      return true;
  }
}
Music::Music( char * song_name, char * song_lyrics, Composer * composer)
{
  uint32_t name_len = strlen( song_name );
  uint32_t lyrics_len = strlen( song_lyrics );
  
  this->name = new char[ name_len + 1 ];
  this->lyrics = new char[ lyrics_len + 1 ];
  this->composer = composer;
  
  strncpy( this->name, song_name, name_len );
  this->name[name_len] = '\0';
  strncpy( this->lyrics, song_lyrics, lyrics_len );
  this->lyrics[lyrics_len] = '\0';
}
Music::~Music( ){
  delete name;
  delete lyrics;
}
Composer * Music::GetComposer( ){ 
  return this->composer; 
}
char * Music::GetName( ){
  return this->name;
}
char * Music::GetLyrics( ){
  return this->lyrics;
}
Box::Box( char * name){
 uint32_t name_len = strlen( name ); 
 this->name = new char[ name_len + 1 ];
 strncpy( this->name, name, name_len );
 this->name[name_len] = '\0';
 this->num = 0;
}
Box::~Box( ){
  for( uint32_t i = 0; i<32; i++ ){
    if( this->music_list[i] )
      delete this->music_list[i];
  }
  delete name;
}
bool Box::AddMusic( Smart_ptr<Music> * Item ){
  for( uint32_t i = 0; i < 32; i++ ){
    Smart_ptr<Music> * tmp = this->music_list[i];
    if( !tmp ){
      this->music_list[i] = new Smart_ptr<Music>(*Item);
      this->num++;
      return true;
    }
  }
  return false;
}
bool Box::DeleteMusic( uint32_t index){
  if( index < 32 && this->music_list[index] != NULL){
    delete this->music_list[index];
    this->music_list[index] = NULL;
    this->num--;
    return true;
  }
  return false;
}
Smart_ptr<Music> * Box::GetMusic( uint32_t index ){
  if( index > 31 && !this->music_list[index])
    exit( -1 );
  return this->music_list[index];
}
bool Box::Put( uint32_t index, Smart_ptr<Music> * Item ){
  if( index > 31)
    exit(-1);
  else if(this->music_list[index])
    *(this->music_list[index]) = *(Item);
  else
    this->music_list[index] = new Smart_ptr<Music>(*Item);
  return true;
}
bool Box::List( ){
  for( uint32_t i = 0; i < 32; i++){
    if( this->music_list[i] ){
      printf("%d. %s\n",i,(*(this->music_list[i]))->GetName( ) );
      printf("Lyrics : %s",(*(this->music_list[i]))->GetLyrics( ) );
    }
  }
  return true; 
}
char * Box::GetName( ){
  return this->name;
}
uint32_t Box::GetNum( ){
  return this->num;
}
