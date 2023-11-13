import os

from dotenv import load_dotenv
from hh import hh_language_average_salary
from statistics_into_table import statistics_into_table
from superjob import sj_language_average_salary


LANGUAGES = ['TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell', 'Go',
             'C#', 'C', 'CSS', 'C++', 'PHP', 'Ruby', 'Python', 'Java',
             'JavaScript']


def main():
    load_dotenv()
    superjob_api_token = os.getenv('SUPERJOB_API_KEY')

    hh_statistics = hh_language_average_salary(LANGUAGES)
    table = statistics_into_table('HeadHunter Moscow', hh_statistics)
    print(table)

    sj_statistics = sj_language_average_salary(LANGUAGES, superjob_api_token)
    table = statistics_into_table('SuperJob Moscow', sj_statistics)
    print(table)


if __name__ == '__main__':
    main()
