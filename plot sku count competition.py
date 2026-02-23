import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

file_path = "/home/vlad/Projects/Соискательство вакансий/Project_9_-_sobesedovanie_liga_group/Интерактивные панели 2 уровень.xlsx"


# Загрузка данных для первого графика (панели 75")
df_sku = pd.read_excel(file_path, sheet_name="sku_count_competition")
company_counts = df_sku['Наименование'].value_counts().reset_index()
company_counts.columns = ['Наименование', 'Количество']

# Сортировка: наибольшие значения сверху, "ООО Лига Смарт" первой среди равных
company_counts['is_liga_smart'] = company_counts['Наименование'].apply(
    lambda x: 1 if x == 'ООО Лига Смарт' else 0
)
company_counts_sorted = company_counts.sort_values(
    by=['Количество', 'is_liga_smart'],
    ascending=[True, True]
).reset_index(drop=True)

colors_sku = ['#50C878' if name == 'ООО Лига Смарт' else 'skyblue'
           for name in company_counts_sorted['Наименование']]



# Загрузка данных для второго графика
df_sales = pd.read_excel(file_path, sheet_name="count sales")

# Оставляем только первые 12 строк
df_sales = df_sales.iloc[:12].copy()

# Переименование столбцов с помощью rename()
df_sales = df_sales.rename(columns={
    df_sales.columns[0]: 'Наименование',
    df_sales.columns[1]: 'Кол-во записей о закупках'
}, inplace=False)



# Исправление типов данных
df_sales['Кол-во записей о закупках'] = pd.to_numeric(
    df_sales['Кол-во записей о закупках'],
    errors='coerce'
)

df_sales = df_sales.dropna(subset=['Кол-во записей о закупках'])

df_sales_sorted = df_sales.sort_values(
    'Кол-во записей о закупках',
    ascending=True
).reset_index(drop=True)

colors_sales = ['#50C878' if name == 'ООО Лига Смарт' else 'lightcoral'
             for name in df_sales_sorted['Наименование']]




# Создаём фигуру с двумя подграфиками (в одной строке)
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=(
        'Количество панелей 75″ у конкурентов',
        'Закупки по ФЗ 44/223 (с 2020 г.)'
    ),
    horizontal_spacing=0.2  # Уменьшили расстояние между графиками
)

# Добавляем первый график (левый)
fig.add_trace(
    go.Bar(
        y=company_counts_sorted['Наименование'],
        x=company_counts_sorted['Количество'],
        orientation='h',
        text=company_counts_sorted['Количество'],
        textposition='outside',
        marker_color=colors_sku,
        marker_line_color='navy',
        marker_line_width=1,
        width=0.6
    ),
    row=1, col=1
)

# Добавляем второй график (правый)
fig.add_trace(
    go.Bar(
        y=df_sales_sorted['Наименование'],
        x=df_sales_sorted['Кол-во записей о закупках'],
        orientation='h',
        text=df_sales_sorted['Кол-во записей о закупках'],
        textposition='outside',
        marker_color=colors_sales,
        marker_line_color='darkred',
        marker_line_width=1,
        width=0.6
    ),
    row=1, col=2
)

# Настройка общего макета — увеличили ширину до 1600 px
fig.update_layout(
    height=600,
    width=1600,  # Увеличили ширину с 1200 до 1600 px
    showlegend=False,
    title_text="Анализ конкурентного положения: ассортимент и закупки",
    title_x=0.5,
    margin=dict(l=150, r=50, t=80, b=80)  # Оставили прежние отступы
)


# Общие настройки для обеих осей Y (чтобы подписи не обрезались)
fig.update_yaxes(
    tickfont=dict(size=10),
    title_font=dict(size=12),
    categoryorder='total ascending',
    automargin=True
)

# Индивидуальные настройки для осей X
fig.update_xaxes(title_text='Количество моделей', row=1, col=1)
fig.update_xaxes(title_text='Кол-во закупок', row=1, col=2)

# Отображение графика
fig.show()

