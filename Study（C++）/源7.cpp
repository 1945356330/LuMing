#include<iostream>

using namespace std;

class Score {
public:
	Score(int m, int f);
	void show();



private:
	int mid_exam;
	int fin_exam;
};

Score::Score(int m, int f)
{
	mid_exam = m;
	fin_exam = f;
}
void Score::show()
{
	cout << "this的指针位置：" << this << "     期末成绩"<<this->fin_exam << endl;
	cout << "打印" << endl;
}
int main()
{
	Score op[3] = {
		Score(30,30),
		Score(60,60),
		Score(90,50)
	};
	op[0].show();
	op[1].show();
	op[2].show();
	return 0;

}
