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
	cout << "this��ָ��λ�ã�" << this << "     ��ĩ�ɼ�"<<this->fin_exam << endl;
	cout << "��ӡ" << endl;
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
