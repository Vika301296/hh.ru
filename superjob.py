import requests

from average_salary import average_salary


def count_sj_language_average_salary(languages, api_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    moscow_id = 4
    development_sphere = 48
    vacancies_per_page = 100
    language_statistics = {}
    for language in languages:
        total_vacancies_found = 0
        different_vacancies_salary = []
        page = 0
        pages_number = 1
        while page < pages_number:
            payload = {
                'keyword': f'{language} разработчик',
                'catalogues': development_sphere,
                'town': moscow_id,
                'page': page,
                'count': vacancies_per_page
            }
            headers = {'X-Api-App-Id': api_key}
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
            vacancies_found = response.json().get('objects')
            vacancy_salary = []
            for vacancy in vacancies_found:
                if vacancy and vacancy['currency'] == 'rub':
                    from_salary = vacancy.get('payment_from')
                    to_salary = vacancy.get('payment_to')
                    salary = average_salary(from_salary, to_salary)
                    if salary:
                        vacancy_salary.append(salary)
            total_vacancies_found += len(vacancies_found)
            different_vacancies_salary.extend(vacancy_salary)
            page += 1
            pages_number = len(vacancies_found) / payload['count']
        if different_vacancies_salary:
            average_language_salary = int(
                sum(different_vacancies_salary) / len(
                    different_vacancies_salary))
        else:
            average_language_salary = 0

        language_statistics[language] = {
            'vacancies_found': total_vacancies_found,
            'vacancies_processed': len(different_vacancies_salary),
            'average_salary': average_language_salary
        }

    return language_statistics
