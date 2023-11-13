import requests


def predict_rub_salary(salary_result):
    if salary_result and salary_result['currency'] == 'RUR':
        from_salary = salary_result.get('from')
        to_salary = salary_result.get('to')

        if from_salary and to_salary:
            average_salary = (from_salary + to_salary) / 2
        elif from_salary:
            average_salary = from_salary * 1.2
        elif to_salary:
            average_salary = to_salary * 0.8
        return int(average_salary)
    return None


def count_hh_language_average_salary(languages):
    url = 'https://api.hh.ru/vacancies'
    language_statistics = {}
    for language in languages:
        total_vacancies_found = 0
        different_vacancies_salary = []
        page = 0
        pages_number = 1
        while page < pages_number:
            payload = {
                'text': f'{language} разработчик',
                'area': 1,
                'period': 1,
                'page': page
            }
            response = requests.get(url, params=payload)
            response.raise_for_status()
            response = response.json()
            vacancies_found_amount = response.get('found')
            vacancies = response.get('items')
            vacancy_salary = [vacancy['salary'] for vacancy in vacancies]
            total_vacancies_found += vacancies_found_amount
            different_vacancies_salary.extend(vacancy_salary)
            pages_number = response.get('pages')
            page += 1
        average_different_vacancies = []

        for salary in different_vacancies_salary:
            average = predict_rub_salary(salary)
            if average:
                average_different_vacancies.append(average)

        if average_different_vacancies:
            average_language_salary = int(
                sum(average_different_vacancies) / len(
                    average_different_vacancies))
        else:
            average_language_salary = 0

        language_statistics[language] = {
            'vacancies_found': total_vacancies_found,
            'vacancies_processed': len(different_vacancies_salary),
            'average_salary': average_language_salary
        }

    return language_statistics
