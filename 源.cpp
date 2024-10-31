#include<iostream>

using namespace std;
inline double circle(double r)
{
	return 3.4 * r * r;
}

int main()
{
	for (int i = 1; i <= 3; i++)
		cout << "r=" << i << "  area= " << circle(i) << endl;
	return 0;
}