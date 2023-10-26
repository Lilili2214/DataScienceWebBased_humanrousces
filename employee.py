class Employee:
    def __init__(self, row):
        self.employee_id = row.iloc[0]['EMPLOYEE_ID']
        self.name = row.iloc[0]['NAME']
        self.age = row.iloc[0]['AGE']
        self.department = row.iloc[0]['DEPARTMENT']
        self.marital_status = row.iloc[0]['MARITALSTATUS']
        self.gender = row.iloc[0]['GENDER']
        self.hire_date = row.iloc[0]['HIREDATE']
        self.annual_income = row.iloc[0]['ANNUAL_INCOME']
        self.salary_range = row.iloc[0]['SALARY_RANGE']
        self.education = row.iloc[0]['EDUCATION']
        self.work_schedule_translation = row.iloc[0]['WORKSCHEDULE_TRANSLATION']
        self.education_level = row.iloc[0]['EDUCATION_LEVEL']
        self.job_role = row.iloc[0]['JOBROLE']
        self.status = row.iloc[0]['STATUS']

    # Getter methods
    def get_employee_id(self):
        return self.employee_id

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_department(self):
        return self.department

    def get_marital_status(self):
        return self.marital_status

    def get_gender(self):
        return self.gender

    def get_hire_date(self):
        return self.hire_date

    def get_annual_income(self):
        return self.annual_income

    def get_salary_range(self):
        return self.salary_range

    def get_education(self):
        return self.education

    def get_work_schedule_translation(self):
        return self.work_schedule_translation

    def get_education_level(self):
        return self.education_level

    def get_job_role(self):
        return self.job_role

    def get_status(self):
        return self.status

    # Setter methods
    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_department(self, department):
        self.department = department

    def set_marital_status(self, marital_status):
        self.marital_status = marital_status

    def set_gender(self, gender):
        self.gender = gender

    def set_hire_date(self, hire_date):
        self.hire_date = hire_date

    def set_annual_income(self, annual_income):
        self.annual_income = annual_income

    def set_salary_range(self, salary_range):
        self.salary_range = salary_range

    def set_education(self, education):
        self.education = education

    def set_work_schedule_translation(self, work_schedule_translation):
        self.work_schedule_translation = work_schedule_translation

    def set_education_level(self, education_level):
        self.education_level = education_level

    def set_job_role(self, job_role):
        self.job_role = job_role

    def set_status(self, status):
        self.status = status
