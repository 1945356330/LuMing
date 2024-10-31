#include<iostream>
#include<string>

using namespace std;

class Person {
public:
	Person(string name1, string id_number1, int age1);
	~Person();
	void show();
protected:
	string name;
	string id_number;
	int age;

};

Person::Person(string name1, string id_number1, int age1) {
	name = name1;
	id_number = id_number1;
	age = age1;
}

Person::~Person() {
	cout << "��������ʹ����" << endl;

}
void Person::show()
{
	cout << endl;
	cout << "������ " << name << endl;
	cout << "���֤�ţ� " << id_number << endl;
	cout << "���䣺 " << age << endl;

}
class Student :public virtual Person {
public:
	Student(string name1, string id_number1, int age1, string stu_number1, int credit1);
	~Student();
	void show();
protected:
	string stu_number;
	int credit;

};

Student::Student(string name1, string id_number1, int age1, string stu_number1, int credit1) :Person(name1, id_number1, age1) {
	stu_number = stu_number1;
	credit = credit1;
}
Student::~Student() {
	cout << "Student��������" << endl;
}
void Student::show() {
	Person::show();
	cout << "ѧ�ţ� " << stu_number << endl;
	cout << "�ɼ��� " << credit << endl;

}

class Teacher :public virtual Person
{
public:
	Teacher(string name1, string id_number1, int age1, string te_number1, int salary1) :Person(name1, id_number1, age1) {
		te_number = te_number1;
		salary = salary1;
	}
	~Teacher() {
		cout << "Teacher��������" << endl;
	}
	void show() {
		Person::show();
		cout << "���ţ� " << te_number << endl;
		cout << "���ʣ� " << salary << endl;
	}
protected:
	string te_number;
	int salary;

};

class Grastudent :public Student, public Teacher {
public:
	Grastudent(string name1, string id_number1, int age1, string stu_number1, int credit1, string te_number1, int salary1, string super1) :
		Person(name1, id_number1, age1), Student(name1, id_number1, age1, stu_number1, credit1),
		Teacher(name1, id_number1, age1, te_number1, salary1)
	{
		supervisoner = super1;
	}
		~Grastudent() {
			cout << "Grastudet��������" << endl;
		}
		void show()
		{
			cout << "������ " << name << endl;
			cout << "���֤�ţ� " << id_number << endl;
			cout << "���䣺 " << age << endl;
			cout << "ѧ�ţ� " << stu_number << endl;
			cout << "�ɼ��� " << credit << endl;
			cout << "���ţ� " << te_number << endl;
			cout << "���ʣ� " << salary << endl;
			cout << "ָ����ʦ�� " << supervisoner << endl;

	}
	
private:
	string supervisoner;

};
int main() {
	Person per1("xiaowang", "2232146", 20);
	per1.show();

	Student stu1("xiao", "34215431254", 20, "2202", 90);
	stu1.show();

	Teacher tea1("С", "620502211313434", 30, "32402", 5000);

	Grastudent gra1("xiao", "2145353212433523", 60, "22023030",30, "2031313", 6000, "��ַ");
	gra1.show();

	return 0;

}
















