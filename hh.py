import requests

from average_salary import count_average_salary


def count_hh_language_average_salary(languages):
    url = 'https://api.hh.ru/vacancies'
    moscow_id = 1
    days_for_search = 1
    language_statistics = {}
    for language in languages:
        page = 0
        pages_number = 1
        while page < pages_number:
            payload = {
                'text': f'{language} разработчик',
                'area': moscow_id,
                'period': days_for_search,
                'page': page
            }
            response = requests.get(url, params=payload)
            response.raise_for_status()
            response = response.json()
            vacancies_found_amount = response.get('found')
            vacancies = response.get('items')
            vacancy_salaries = [vacancy['salary'] for vacancy in vacancies]
            pages_number = response.get('pages')
            page += 1
        average_salary_for_vacancies = []

        for salary in vacancy_salaries:
            if salary and salary['currency'] == 'RUR':
                from_salary = salary.get('from')
                to_salary = salary.get('to')
                average = count_average_salary(from_salary, to_salary)
                if average:
                    average_salary_for_vacancies.append(average)
        if average_salary_for_vacancies:
            average_language_salary = int(
                sum(average_salary_for_vacancies) / len(
                    average_salary_for_vacancies))
        else:
            average_language_salary = 0

        language_statistics[language] = {
            'vacancies_found': vacancies_found_amount,
            'vacancies_processed': len(vacancy_salaries),
            'average_salary': average_language_salary
        }

    return language_statistics
