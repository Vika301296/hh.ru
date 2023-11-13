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


def sj_language_average_salary(languages, api_key):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    language_data = {}
    for language in languages:
        total_vacancies_found = 0
        all_salary_results = []
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
            salary_result = []
            for vacancy in vacancies_found:
                salary = predict_rub_salary_for_superJob(vacancy)
                if salary:
                    salary_result.append(salary)
            total_vacancies_found += len(vacancies_found)
            all_salary_results.extend(salary_result)
            page += 1
            pages_number = len(vacancies_found) / payload['count']
        if all_salary_results:
            average_language_salary = int(
                sum(all_salary_results) / len(all_salary_results))
        else:
            average_language_salary = 0

        language_data[language] = {
            'vacancies_found': total_vacancies_found,
            'vacancies_processed': len(all_salary_results),
            'average_salary': average_language_salary
        }

    return language_data
