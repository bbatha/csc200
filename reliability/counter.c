#include<stdio.h>
#include<limits.h>

int main() {
    long count;
    for(count = 0; count < 1000000000000; count++) {
        if(count % 1000000000 == 0 && count != 0) {
            printf("%ld\n", count);
        }
    }
    return 0;
}
