import requests


def compare_languages(url, languages):
    results = {}
    for language in languages:
        payload = {'text': f'{language} разработчик',
                   'area': 1,
                   'period': 30}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        found = response.json().get('found')
        results[language] = found
    return results


def get_salary(url, language):
    payload = {'text': f'{language} разработчик',
               'area': 1,
               'period': 1}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    vacancies = response.json().get('items')
    salary_result = []
    for vacancy in vacancies:
        salary = vacancy['salary']
        salary_result.append(salary)
    return salary_result


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


def hh_language_average_salary(languages):
    url = 'https://api.hh.ru/vacancies'
    language_data = {}
    for language in languages:
        total_vacancies_found = 0
        all_salary_results = []
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
            vacancies_found_amount = response.json().get('found')
            vacancies = response.json().get('items')
            salary_result = []
            for vacancy in vacancies:
                salary = vacancy['salary']
                salary_result.append(salary)
            total_vacancies_found += vacancies_found_amount
            all_salary_results.extend(salary_result)
            pages_number = response.json().get('pages')
            page += 1
        average_different_vacancies = []

        for salary in all_salary_results:
            average = predict_rub_salary(salary)
            if average:
                average_different_vacancies.append(average)

        if average_different_vacancies:
            average_language_salary = int(
                sum(average_different_vacancies) / len(
                    average_different_vacancies))
        else:
            average_language_salary = 0

        language_data[language] = {
            'vacancies_found': total_vacancies_found,
            'vacancies_processed': len(all_salary_results),
            'average_salary': average_language_salary
        }

    return language_data
