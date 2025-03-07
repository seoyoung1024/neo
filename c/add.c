#include <stdio.h>

int x =5;

int add(int);

int main(){
    int y = 3;
    printf("%d + %d = %d\n",x,y,add(y));
    return 0;
}

int add(int y){
    return x + y;
    }
