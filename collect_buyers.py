import os
import pandas as pd
import csv

def detect_encoding(file_path):
    """Определяет кодировку файла."""
    encodings = ['utf-8', 'cp1251', 'windows-1251']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                f.read(1000)
            return encoding
        except UnicodeDecodeError:
            continue
    return 'utf-8'  # запасной вариант


def detect_delimiter(file_path, encoding):
    """Автоматически определяет разделитель в CSV-файле."""
    with open(file_path, 'r', encoding=encoding) as f:
        sample = f.read(2048)
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        return delimiter

def collect_customer_names(directory_path):
    all_customers = []

    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.csv'):
            file_path = os.path.join(directory_path, filename)

            try:
                # Определяем кодировку
                encoding = detect_encoding(file_path)

                # Определяем разделитель
                delimiter = detect_delimiter(file_path, encoding)

                # Читаем CSV с обработкой ошибок
                df = pd.read_csv(
                    file_path,
                    encoding=encoding,
                    sep=delimiter,
                    on_bad_lines='skip',  # пропускаем проблемные строки
                    quoting=csv.QUOTE_MINIMAL,  # минимальная обработка кавычек
                    engine='python'  # более гибкий парсер
                )

                # Проверяем наличие столбца (с учётом возможных вариаций названия)
                possible_columns = [
                    'Наименование Заказчика',
                    'наименование заказчика',
                    'НАИМЕНОВАНИЕ ЗАКАЗЧИКА',
                    'Заказчик',
                    'заказчик'
                ]

                found_column = None
                for col in possible_columns:
                    if col in df.columns:
                        found_column = col
                        break

                if found_column:
                    # Добавляем все непустые значения
                    customers_from_file = df[found_column].dropna().astype(str).tolist()
                    all_customers.extend(customers_from_file)
                    print(f"Обработан файл: {filename} (найдено {len(customers_from_file)} записей)")
                else:
                    print(f"Столбец 'Наименование Заказчика' не найден в файле: {filename}")

            except Exception as e:
                print(f"Критическая ошибка при обработке файла {filename}: {e}")

    # Удаляем дубликаты и сортируем
    unique_customers = sorted(set(all_customers))

    # Сохраняем результат
    output_filename = 'Список_заказчиков.csv'
    output_path = os.path.join(directory_path, output_filename)

    result_df = pd.DataFrame({'Наименование Заказчика': unique_customers})
    result_df.to_csv(output_path, index=False, encoding='utf-8')

    print(f"\nГотово! Список сохранён в: {output_path}")
    print(f"Всего уникальных заказчиков: {len(unique_customers)}")

# Пример использования
if __name__ == '__main__':
    target_directory = r'/home/vlad/Projects/Соискательство вакансий/Project_9_-_sobesedovanie_liga_group/Закупки конкурентов (ЕИС 44 ⁄ 223 ФЗ)/'
    collect_customer_names(target_directory)

