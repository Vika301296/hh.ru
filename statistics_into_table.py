from terminaltables import AsciiTable


def statistics_into_table(title, language_data):
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
