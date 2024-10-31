#include<iostream>

using namespace std;

int main()
{
	int a=10;
	void* p;

	p = &a;
	cout << "p=" << *(int*)p << endl;
	return 0;

}