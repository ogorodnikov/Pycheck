NOW = '01.01.2018'
WORK_PREFIXES = {'female': 'She is a', 'male': 'He is a', 'other': 'Is a'}

class Person:
    def __init__(self, first_name, last_name, birth_date, job, working_years, salary, country, city, gender='other'):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.job = job
        self.working_years = working_years
        self.salary = salary
        self.country = country
        self.city = city
        self.gender = gender

    def name(self):
        return f'{self.first_name} {self.last_name}'

    def age(self):
        now_day, now_month, now_year = map(int, NOW.split('.'))
        birth_day, birth_month, birth_year = map(int, self.birth_date.split('.'))

        stuffed_day = birth_month > now_month and birth_day > now_day
        year_delta = now_year - birth_year - stuffed_day

        return year_delta

    def work(self):
        return WORK_PREFIXES[self.gender] + ' ' + self.job




if __name__ == '__main__':

    p1 = Person("John", "Smith", "19.09.1979", "welder", 15, 3600, "Canada", "Vancouver", "male")
    p2 = Person("Hanna Rose", "May", "05.12.1995", "designer", 2.2, 2150, "Austria", "Vienna")
    assert p1.name() == "John Smith", "Name"
    assert p1.age() == 38, "Age"
    assert p2.work() == "Is a designer", "Job"
    assert p1.money() == "648 000", "Money"
    assert p2.home() == "Lives in Vienna, Austria", "Home"