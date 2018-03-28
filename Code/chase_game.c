#include <unistd.h>
#include <stdlib.h>
extern char **environ;

int main(int argc, char *argv[]){
  execve("../.Code/dist/chase_game/chase_game", argv, environ);
}
