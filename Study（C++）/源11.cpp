#include<iostream>
#include<string>
using namespace std;

class Person {
public:
	Person(string name1, string id_number1, int age1);
	~Person();
	void show();
private:
	string name;
	string id_number;
	int age;
};

Person::Person(string name1,string id_nubmer1, int age1) {

	name = name1;
	id_number = id_nubmer1;
	age = age1;
}

Person::~Person() {

}

void Person::show()
{
	cout << "������ " << name << endl;
	cout << "���֤�ţ�" << id_number << endl;
	cout << "���䣺 " << age << endl;

}

class Student:public Person {
public:
	Student(string name1, string id_number1, int age1, int cret1);
	~Student();
	void show();
private:
	int cret;
};

Student::Student(string name1, string id_number1, int age1, int cret1) :Person(name1, id_number1, age1) {
	cret = cret1;
}
Student::~Student() {
	cout << "��������" << endl;
}
void Student::show()
{
	Person::show();
	cout << "ѧ�֣�" << cret<<endl;

}
int main()
{
	Student stu1("С��", "11324621144543434", 20, 233);
	stu1.show();
	return 0;


}
