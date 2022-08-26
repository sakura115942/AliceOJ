#include <stdio.h>

int main()
{
    int a = 0;
    int b = 0;
    scanf("%d %d", &a, &b/0);
    printf("%d", a+b);
    return 0;
}