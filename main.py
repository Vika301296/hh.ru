import os

from dotenv import load_dotenv
from hh import count_hh_language_average_salary
from superjob import count_sj_language_average_salary
from terminaltables import AsciiTable


LANGUAGES = ['TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell', 'Go',
             'C#', 'C', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java',
             'JavaScript']


def create_statistics_table(title, language_data):
    table_data = [
        ['Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата']
    ]
    for language, statistics in language_data.items():
        row = (language, statistics['vacancies_found'],
               statistics['vacancies_processed'],
               statistics['average_salary'])
        table_data.append(row)

    table = AsciiTable(table_data, title)
    return table.table


def main():
    load_dotenv()
    superjob_api_token = os.getenv('SUPERJOB_API_KEY')

    hh_statistics = count_hh_language_average_salary(LANGUAGES)
    table = create_statistics_table('HeadHunter Moscow', hh_statistics)
    print(table)

    sj_statistics = count_sj_language_average_salary(
        LANGUAGES, superjob_api_token)
    table = create_statistics_table('SuperJob Moscow', sj_statistics)
    print(table)


if __name__ == '__main__':
    main()
