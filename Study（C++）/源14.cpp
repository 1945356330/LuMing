#include<iostream>
using namespace std;

class Complex {
public:
	Complex(double r = 0.0, double i = 0.0);
	friend Complex operator+(Complex& a, Complex& b);
	void display();
private:
	double real;
	double imag;
};
Complex::Complex(double r, double i) {
	real = r;
	imag = i;
}

Complex operator+(Complex& a, Complex& b) {
	Complex temp;
	temp.real = a.real + b.real;
	temp.imag = a.imag + b.imag;
	return temp;
}
void Complex::display() {
	cout << "real: " << real << endl;
	cout << "imag: " << imag << endl;

}

int main()
{
	Complex A1(2.2,3.3), A2(1.0, 3.0), A3;
	A1.display();
	A2.display();
	A3 = A1 + A2;
	A3.display();
	return 0;

}