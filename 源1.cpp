#include<iostream>
using namespace std;

int main()
{
	int i = 10;
	int& j = i;
	cout << "i=" << i << " j=" << j<<endl;
	cout << "变量i的地址" << &i << endl;
	cout << "变量j的地址" << &j << endl;
	return 0;

}