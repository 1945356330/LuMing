#include<iostream>
using namespace std;

class Shape {
protected:
	int r;

public:
	Shape(double x) {
		r = x;
	}
	virtual void area() = 0;
	virtual void perimeter() = 0;

};

class Circle :public Shape {
public:
	Circle(double x) :Shape(x) {
	}
	void area();
	void perimeter();

};

void Circle::area()
{
	cout << "计算面积为： " << endl;
	cout << 3.14 * r * r << endl;

}
void Circle::perimeter() {
	cout << "周长为:" << endl;
	cout << 2 * 3.14 * r << endl;

}
int main()
{
	Circle c1(3.14);
	c1.area();
	c1.perimeter();
	return 0;

}