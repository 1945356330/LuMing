#include<iostream>

using namespace std;

struct Score
{
	int mid_exam;
	int fin_exam;
};

int main()
{
	Score score1;
	score1.mid_exam = 90;
	score1.fin_exam = 80;
	cout << "���гɼ��� " << score1.mid_exam << endl;
	cout << "��ĩ�ɼ��� " << score1.fin_exam << endl;
	cout << "�ܳɼ��� " << (score1.fin_exam)*0.7+(score1.mid_exam)*0.3 << endl;
	return 0;

}