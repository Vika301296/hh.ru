import requests


def predict_rub_salary_for_superJob(vacancy):
    if vacancy and vacancy['currency'] == 'rub':
        from_salary = vacancy.get('payment_from')
        to_salary = vacancy.get('payment_to')
        if from_salary and to_salary:
            average_salary = int((from_salary + to_salary) / 2)
        elif from_salary:
            average_salary = int(from_salary * 1.2)
        elif to_salary:
            average_salary = int(to_salary * 0.8)
        else:
            return None
        return average_salary
    else:
        return None


def count_sj_language_average_salary(languages, api_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    language_statistics = {}
    for language in languages:
        total_vacancies_found = 0
        different_vacancies_salary = []
        page = 0
        pages_number = 1
        while page < pages_number:
            payload = {
                'keyword': f'{language} разработчик',
                'catalogues': 48,
                'town': 4,
                'page': page,
                'count': 100
            }
            headers = {'X-Api-App-Id': api_key}
            response = requests.get(url, params=payload, headers=headers)
            response.raise_for_status()
            vacancies_found = response.json().get('objects')
            vacancy_salary = []
            for vacancy in vacancies_found:
                salary = predict_rub_salary_for_superJob(vacancy)
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
