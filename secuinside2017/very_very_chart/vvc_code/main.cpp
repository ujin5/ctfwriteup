#include <iostream>
#include <stdint.h>
#include "User.h"
#include <stdlib.h>
Smart_ptr<Music> * Very_Chart[1024] = { 0, };
Item * ItemList[32] = { 0, };
uint32_t numOfItem = 0;
void print( char * out ){
  std::cout<<out;
}
bool Composer_main( Composer * Item );
void Composer_menu( );
bool User_main( User * Item );
void User_menu( );
void Very_Chart_List( );
void Register( ){
  uint32_t n = 0;
  Item * new_item = NULL; 
  if( numOfItem > 31 ){
    print( " Stop register!\n" );
    return;
  }
  print( "1. User\n");
  print( "2. Composer\n");
  print( "Type :" );
  std::cin>>n;
  switch( n ){
    case 1:{
      new_item = (Item *) new User( );
      break;
    };
    case 2:{
      new_item = (Item *) new Composer( );
      break;
    };
    default:{
      print( "Invaild Type\n" );
      return;
    };
  }
  ItemList[numOfItem++] = new_item;
  print( "Success\n" );
  return;
}
void Login( ){
  char id[256] = { 0, };
  char password[256] = { 0, };
  print( "ID :");
  readline( id, 256 - 1 );
  print( "PW :" );
  readline( password, 256 -1 );
  for( uint32_t i = 0; i < numOfItem; i++){
    if( ItemList[i]->CheckItem( id, password ) ){
      switch( ItemList[i]->GetType( ) ){
        case 1:{
          User_main( (User *) ItemList[i] );
          return;
        };
        case 2:{
          Composer_main( (Composer *) ItemList[i] );
          return;
        };
        default:{
          exit(-1);
          return;
        };
      }
    }
  }
}
void Composer_menu( ){
  print( "1. Write Music\n" );
  print( "2. Delete Music\n" );
  print( "3. Edit Profile\n" );
  print( "4. Edit Music\n" );
  print( "5. Exit");
  print( ">" );
  return;
}
bool Composer_main( Composer * Item ){
  uint32_t n = 0;
  bool loop = true;
  while( loop ){
    Composer_menu( );
    std::cin>>n;
    switch( n ){
      case 1:{
        Item->WriteMusic( );
        break;
      };
      case 2:{
        Item->DeleteMusic( );
        break;
      };
      case 3:{
        Item->EditProfile( );
        break;
      };
      case 4:{
        uint32_t index;
        print( "Index :" );
        std::cin>>index;
        Item->EditMusic( index );
        break;
      };
      case 5:{
        loop = false;
        break;
      };
      default:{
        break;
      };
    }
  }
  return true;
}
void User_menu( ){
  print( "1. Create VeryBox\n" );
  print( "2. Delete VeryBox\n" );
  print( "3. Buy Music\n" );
  print( "4. Put Music in Box\n" );
  print( "5. Move Box to Box\n");
  print( "6. Box List\n" );
  print( "7. My Music List\n" );
  print( "8. Delete Music\n" );
  print( "9. Exit\n" );
  print( ">" );
}
void Very_Chart_List( ){
  print( "[ Very Very Music Chart ! ]\n");
  for( uint32_t i = 0; i<1024; i++ ){
    if( Very_Chart[i] != NULL ){
      std::cout<<i<<". "<<(*Very_Chart[i])->GetName( )<<std::endl;
    }
  }
}
bool User_main( User * Item ){
  uint32_t n = 0;
  bool loop = true;
  while( loop ){
    User_menu( );
    std::cin>>n;
    switch( n ){
      case 1:{
        Item->MakeBox( );
        break;
      };
      case 2:{
        uint32_t index;
        print( "Index :" );
        std::cin>>index;
        Item->DeleteBox( index );
        break;
      };
      case 3:{
        Very_Chart_List( );
        uint32_t index;
        print( "Index :");
        std::cin>>index;
        if( index < 1024 && Very_Chart[index] != NULL )
          Item->BuyMusic( Very_Chart[index] );
        else
          print( "Invaild Index\n");
        break;
      };
      case 4:{
        uint32_t index;
        print( "Select your box :");
        std::cin>>index;
        Item->PutInBox( index );
        break;
      };
      case 5:{
        uint32_t dest_index;
        uint32_t src_index;
        print( "Dest index :");
        std::cin>>dest_index;
        print( "Src index :");
        std::cin>>src_index;
        Item->BoxToBox( dest_index, src_index );
        break;
      };
      case 6:{
        Item->BoxList( );
        break;
      };
      case 7:{
        Item->MusicList( );
        break;
      };
      case 8:{
        uint32_t index;
        print( "Index :" );
        std::cin>>index;
        Item->DeleteMusic( index );
        break;
      }
      case 9:{
        loop = false;
        break;
      };
      default:{
        print( "Invaild Command\n" );
        break;
      };
    }
  }
  return true;
}
void show_menu( ){
  print( "1. Login\n" );
  print( "2. Register\n" );
  print( "3. Exit\n" );
  print( ">" );
  return;
}
int main(){
  setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
  uint32_t button = 0;
  uint32_t loop = true;
  while( loop ){
    show_menu( );
    std::cin>>button;
    switch( button ){
      case 1:{
        Login( );
        break;
      };
      case 2:{
        Register( );
        break;
      };
      case 3:{
        loop = false;
        break;
      };
      default:{
        print( "Invaild Command\n" );
        break;
      };
    }
  }
  return 0;
}
