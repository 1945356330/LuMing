#include<iostream>
#include<string>

using namespace std;

int main()
{
	string str1 = "ABC";
	string str2 = "DEF";
	string str("GHI");
	string str4, str5;
	str4 = str1;
	cout << "str4 is " << str4 << endl;
	str5 = str1 + str2;
	cout << "str1+str2 is " << str5 << endl;
	str5 = str1 + "123";
	cout << "str5-new" << str5 << endl;
	return 0;

}