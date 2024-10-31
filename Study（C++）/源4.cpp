#include<iostream>

using namespace std;

class Score {
public:
	Score(int m = 0, int f = 0);
	void setScore(int m, int f);
	void showScore();
private:
	int mid_exam;
	int fin_exam;

};

Score::Score(int m, int f) :mid_exam(m), fin_exam(f)
{
	cout << "构造函数使用中。。。。" << endl;
}
void Score::setScore(int m, int f)
{
	mid_exam = m;
	fin_exam = f;
}

inline void Score::showScore()
{
	cout << "期末成绩" << fin_exam << endl;

}

int main()
{
	Score op1(20, 20);
	Score op2(30, 30);
	op1.showScore();
	op2.showScore();
	return 0;
}
