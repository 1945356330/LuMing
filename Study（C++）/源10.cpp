#include<iostream>

using namespace std;

class X {
public:
	X(int a1, double b1) {
		a = a1;
		b = b1;
	}
	void display() {
		cout << "a = " << a<<endl;
		cout << "b = " << b<<endl;
	}
private:
	int a;
	double b;
};
class Y {
public:
	Y(int a1, double b1, int c1):cc(a1,b1) 
	{
		c = c1;
	}
	void disp() {
		cc.display();
		cout << "c: " << c << endl;
	}
private:
	X cc;
	int c;


};

int main()
{
	Y b(123, 456, 789);
	b.disp();
	return 0;

}