#include<iostream>
using namespace std;
using namespace std;
class Score {
public:
	Score(int m, int f);
	Score(const Score &p);
	void showScore();
private:
	int mid_exam;
	int fin_exam;


};

Score::Score(int m, int f)
{
	cout << "构造函数使用中" << endl;
	mid_exam = m;
	fin_exam = f;
}

Score::Score(const Score& p)
{
	mid_exam = p.mid_exam;
	fin_exam = p.fin_exam;
	cout << "拷贝构造函数使用中。。。" << endl;

}
void Score::showScore()
{
	cout << "期中成绩： " << mid_exam << endl;
	cout << "期末成绩：  " << fin_exam << endl;
	cout << "总成绩：  " << (mid_exam) * 0.7 + (fin_exam) * 0.3 << endl;
	
}

void fun1(Score p)
{
	p.showScore();
}

Score fun2()
{
	Score p4(80, 80);
	return p4;
}

int main()
{
	Score p1(80,80);
	p1.showScore();
	Score p2(p1);
	p2.showScore();
	Score p3=p1;
	p3.showScore();
	fun1(p1);

	p2 = fun2();
	p2.showScore();


	return 0;

}