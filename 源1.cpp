#include<iostream>
using namespace std;

int main()
{
	int i = 10;
	int& j = i;
	cout << "i=" << i << " j=" << j<<endl;
	cout << "����i�ĵ�ַ" << &i << endl;
	cout << "����j�ĵ�ַ" << &j << endl;
	return 0;

}