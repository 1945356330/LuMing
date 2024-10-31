#include<iostream>
using namespace std;

int main()
{
	void* pc;
	int i = 456;
	char c = 'a';
	pc = &i;
	cout << *(int*)pc << endl;
	pc = &c;
	cout << *(char*)pc << endl;
	return 0;


}