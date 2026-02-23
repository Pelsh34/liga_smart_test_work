import pandas as pd
import plotly.express as px

# Загрузка данных из Excel-файла
file_path = "/home/vlad/Projects/Соискательство вакансий/Project_9_-_sobesedovanie_liga_group/Интерактивные панели 2 уровень.xlsx"
sheet_name = "sku_count_competition"

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Подсчёт количества повторений для каждой компании
company_counts = df['Наименование'].value_counts().reset_index()
company_counts.columns = ['Наименование', 'Количество']

# Сортировка: сначала по количеству (по убыванию), затем «ООО Лига Смарт» первой среди равных
# Создаём вспомогательный столбец для сортировки
company_counts['sort_key'] = company_counts['Наименование'].apply(
    lambda x: 0 if x == 'ООО Лига Смарт' else 1
)

# Сначала сортируем по sort_key (чтобы «ООО Лига Смарт» была приоритетной), затем по количеству (по убыванию)
company_counts_sorted = company_counts.sort_values(
    by=['Количество', 'sort_key'],
    ascending=[False, True]  # Количество: убывание; sort_key: возрастание (0 < 1)
).reset_index(drop=True)

# Определяем цвета для столбцов: изумрудный для «ООО Лига Смарт», синий для остальных
colors = ['#50C878' if name == 'ООО Лига Смарт' else 'skyblue'
           for name in company_counts_sorted['Наименование']]  # #50C878 — изумруд

# Построение ГОРИЗОНТАЛЬНОГО столбчатого графика (оси поменяны местами)
fig = px.bar(
    company_counts_sorted,
    y='Наименование',      # Теперь наименования на вертикальной оси
    x='Количество',      # Количество на горизонтальной оси
    title='Количество позиций по компаниям (от большего к меньшему)',
    labels={'Наименование': 'Компания', 'Количество': 'Количество позиций'},
    text='Количество'      # Отображение значений на столбцах
)

# Настройка внешнего вида графика
fig.update_traces(
    texttemplate='%{text}',
    textposition='outside',
    marker_color=colors,    # Разные цвета для разных компаний
    marker_line_color='navy',
    marker_line_width=1,
    width=0.6,           # Ширина столбцов
    cliponaxis=False
)

# Дополнительные настройки макета
fig.update_layout(
    height=600,         # Высота графика
    width=900,        # Ширина графика
    yaxis=dict(
        tickfont=dict(size=10),  # Уменьшенный размер шрифта подписей на оси Y
        title='Компания',
        title_font=dict(size=12),
        categoryorder='total descending'  # Гарантирует сортировку по убыванию количества
    ),
    xaxis=dict(
        title='Количество позиций',
        title_font=dict(size=12),
        tickfont=dict(size=11)  # Размер шрифта меток на оси X
    ),
    showlegend=False,
    title_x=0.5,
    margin=dict(l=120, r=50, t=60, b=80)  # Увеличен отступ слева для длинных названий
)

# Отображение графика
fig.show()

# Дополнительная информация: выводим отсортированные данные в консоль
print("\nОтсортированные данные (компании по количеству позиций):")
print(company_counts_sorted[['Наименование', 'Количество']])
