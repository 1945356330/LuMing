#include<iostream>

using namespace std;

class Score {
public:
	void setScore(int m, int f)
	{
		mid_exam = m;
		fin_exam = f;
	}
	void showScore()
	{
		cout << "���гɼ��� " << mid_exam << endl;
		cout << "��ĩ�ɼ��� " << fin_exam << endl;
		cout << "�ܳɼ��� " << (mid_exam) * 0.3 + (fin_exam) * 0.7 << endl;
	}

private:
	int mid_exam;
	int fin_exam;


};

int main()
{
	Score op1, op2;
	op1.setScore(80, 80);
	op2.setScore(90, 92);

	op1.showScore();
	op2.showScore();
	return 0;


}