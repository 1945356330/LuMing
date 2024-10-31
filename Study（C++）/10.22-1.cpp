#include<iostream>

using namespace std;

int a[] = { 1,3,5,7,9 };
int& index(int);

int main()
{
    cout << index(2) << endl;
    index(2) = 25;
    cout << index(2) << endl;
    return 0;

}