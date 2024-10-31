#include<iostream>

using namespace std;

class Sample {
public:
	Sample(int i = 0, int j = 0)
	{
		x = i;
		y = j;
	}
	void copy(Sample& xy);
	void print() {
		cout << x << "," <<y<< endl;
	}
private:
	int x, y;

};

void Sample::copy(Sample& xy)
{
	if (this == &xy) return;  
	*this = xy;
}

int main() {
	Sample p1, p2(5,5);
	p1.copy(p2);
	p1.print();
	return 0;

}