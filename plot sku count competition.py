import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Указываем путь к файлу
file_path = "/home/vlad/Projects/Соискательство вакансий/Project_9_-_sobesedovanie_liga_group/Интерактивные панели 2 уровень.xlsx"


# Загружаем данные для первого графика
df_sku = pd.read_excel(file_path, sheet_name="sku_count_competition")
company_counts = df_sku['Наименование'].value_counts().reset_index()
company_counts.columns = ['Наименование', 'Количество']

# Сортируем: наибольшие значения сверху, «ООО Лига Смарт» первой среди равных
company_counts['is_liga_smart'] = company_counts['Наименование'].apply(
    lambda x: 1 if x == 'ООО Лига Смарт' else 0
)
company_counts_sorted = company_counts.sort_values(
    by=['Количество', 'is_liga_smart'],
    ascending=[True, True]
).reset_index(drop=True)

# Задаём цвета: Лига Смарт — зелёный, остальные — голубые
colors_sku = ['#50C878' if name == 'ООО Лига Смарт' else 'skyblue'
           for name in company_counts_sorted['Наименование']]

# Создаём фигуру для первого графика
fig1 = go.Figure()

# Добавляем столбчатую диаграмму
fig1.add_trace(go.Bar(
    y=company_counts_sorted['Наименование'],
    x=company_counts_sorted['Количество'],
    orientation='h',
    text=company_counts_sorted['Количество'],
    textposition='outside',
    marker_color=colors_sku
))

# Настройка макета графика
fig1.update_layout(
    title=dict(
        text='Количество панелей 75″ на рынке',
        font=dict(size=13, color='black')
    ),
    height=600,
    width=900,
    margin=dict(l=150, r=50, t=50, b=50),
    showlegend=False
)

# Настройка осей с корректным синтаксисом Plotly
fig1.update_yaxes(
    title=dict(
        text='Компании',
        font=dict(size=11, color='rgb(55, 83, 109)')
    ),
    tickfont=dict(size=9, color='rgb(55, 83, 109)'),
    categoryorder='total descending'  # Сортировка по убыванию
)

fig1.update_xaxes(
    title=dict(
        text='Количество панелей',
        font=dict(size=11, color='rgb(55, 83, 109)')
    ),
    tickfont=dict(size=9, color='rgb(55, 83, 109)'),
    gridcolor='lightgray',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='black'
)

# Отображаем график для проверки
#fig1.show()










#####################################################################


import pandas as pd
import plotly.graph_objects as go


# Указываем путь к файлу
file_path = "/home/vlad/Projects/Соискательство вакансий/Project_9_-_sobesedovanie_liga_group/Интерактивные панели 2 уровень.xlsx"


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

# Сортируем: малые значения сверху, наибольшие — снизу
df_sales_sorted = df_sales.sort_values(
    'Кол-во записей о закупках',
    ascending=True  # Сортировка по возрастанию: малые значения первыми
).reset_index(drop=True)

# Задаём цвета: ООО Лига Смарт — зелёный, остальные — светло‑коралловые
colors_sales = ['#50C878' if name == 'ООО Лига Смарт' else 'lightcoral'
             for name in df_sales_sorted['Наименование']]

# Создаём фигуру для второго графика
fig2 = go.Figure()

# Добавляем столбчатую диаграмму
fig2.add_trace(go.Bar(
    y=df_sales_sorted['Наименование'],
    x=df_sales_sorted['Кол-во записей о закупках'],
    orientation='h',
    text=df_sales_sorted['Кол-во записей о закупках'],
    textposition='outside',
    marker_color=colors_sales
))

# Настройка макета графика
fig2.update_layout(
    title=dict(
        text='Закупки по ФЗ 44/223 (с 2020 г.)',
        font=dict(size=13, color='black')
    ),
    height=600,
    width=900,
    margin=dict(l=150, r=50, t=50, b=50),
    showlegend=False
)

# Настройка осей с корректным синтаксисом Plotly
fig2.update_yaxes(
    title=dict(
        text='Компании',
        font=dict(size=11, color='rgb(55, 83, 109)')
    ),
    tickfont=dict(size=9, color='rgb(55, 83, 109)'),
    categoryorder='array'  # Используем порядок из отсортированного DataFrame
)

fig2.update_xaxes(
    title=dict(
        text='Кол-во записей о закупках',
        font=dict(size=11, color='rgb(55, 83, 109)')
    ),
    tickfont=dict(size=9, color='rgb(55, 83, 109)'),
    gridcolor='lightgray',
    zeroline=True,
    zerolinewidth=2,
    zerolinecolor='black'
)

# Отображаем график для проверки
# fig2.show()









##################################################################################


import pandas as pd
import plotly.graph_objects as go

# Указываем путь к файлу
file_path = "/home/vlad/Projects/Соискательство вакансий/Project_9_-_sobesedovanie_liga_group/Интерактивные панели 2 уровень.xlsx"

# Загружаем данные для третьего графика
df_industries = pd.read_excel(file_path, sheet_name="type_of_economic_segment")
df_industries.columns = ['Отрасль', 'Количество организаций', 'Доля (%)']

# Создаём фигуру только для таблицы
fig3 = go.Figure()

# Создаём таблицу с данными
table = go.Table(
    header=dict(
        values=['Отрасль', 'Количество организаций', 'Доля (%)'],
        font=dict(size=14, color='white'),
        fill_color='rgb(55, 83, 109)',  # Тёмно‑синий фон заголовка
        align='center',
        height=40
    ),
    cells=dict(
        values=[
            df_industries['Отрасль'],
            df_industries['Количество организаций'],
            df_industries['Доля (%)']
        ],
        font=dict(size=12),
        fill_color=[
            ['lightgray' if i % 2 == 0 else 'white' for i in range(len(df_industries))]
        ],  # Чередование цветов строк
        align=['left', 'center', 'center'],  # Выравнивание: текст влево, числа по центру
        height=35
    ),
    columnwidth=[200, 150, 100]  # Ширина колонок: отрасль шире всего
)

fig3.add_trace(table)

# Финальная настройка макета
fig3.update_layout(
    title=dict(
        text='Распределение организаций по отраслям',
        font=dict(size=13, color='rgb(55, 83, 109)'),
        x=0.5,  # Центрирование заголовка
        xanchor='center'
    ),
    height=500 + len(df_industries) * 35,  # Динамическая высота в зависимости от числа строк
    width=900,
    margin=dict(l=50, r=50, t=80, b=50),
    template='plotly_white'  # Чистый белый фон
)

# Отображаем итоговую таблицу
# fig3.show()










########################################################################










# Загружаем данные из Excel: основной лист (для первой таблицы) и 'categories' (для второй)
df_categories = pd.read_excel(file_path, sheet_name='categories')


df_categories.columns = ['Категория', 'Количество', 'Доля (%)']

# Создаём фигуру только для таблицы
fig4 = go.Figure()

# Создаём таблицу с данными
table = go.Table(
    header=dict(
        values=['Категория', 'Количество', 'Доля (%)'],
        font=dict(size=14, color='white'),
        fill_color='rgb(55, 83, 109)',  # Тёмно‑синий фон заголовка
        align='center',
        height=40
    ),
    cells=dict(
        values=[
            df_categories['Категория'],
            df_categories['Количество'],
            df_categories['Доля (%)']
        ],
        font=dict(size=12),
        fill_color=[
            ['lightgray' if i % 2 == 0 else 'white' for i in range(len(df_categories))]
        ],  # Чередование цветов строк
        align=['left', 'center', 'center'],  # Выравнивание: текст влево, числа по центру
        height=35
    ),
    columnwidth=[200, 150, 100]  # Ширина колонок: отрасль шире всего
)

fig4.add_trace(table)

# Финальная настройка макета
fig4.update_layout(
    title=dict(
        text='Распределение организаций по отраслям',
        font=dict(size=13, color='rgb(55, 83, 109)'),
        x=0.5,  # Центрирование заголовка
        xanchor='center'
    ),
    height=500 + len(df_categories) * 35,  # Динамическая высота в зависимости от числа строк
    width=900,
    margin=dict(l=50, r=50, t=80, b=50),
    template='plotly_white'  # Чистый белый фон
)

# fig4.show()




















########################################################################



from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Создаём дашборд с 3 строками и 2 колонками
dashboard = make_subplots(
    rows=4,
    cols=2,
    column_widths=[0.5, 0.5],  # 75 % ширины для первого графика, 25 % для второго
    subplot_titles=(
        'Предложение интерактивных панелей с диагональю 75″',
        'Закупки по ФЗ 44/223 (с 2020 г.)',
        '',  # Пустой заголовок для блока выводов
        'Распределение по отраслям',  # Заголовок для первой таблицы (row=3, col=1)
        'Распределение по категориям',  # Заголовок для второй таблицы (row=3, col=2)
        ''  # Новый заголовок для 4‑й строки
    ),
    vertical_spacing=0.02,  # Минимум отступа между строками
    horizontal_spacing=0.4,   # Отступ между графиками
    specs=[
        # [  # Строка 1: два XY‑графика
        #     {"secondary_y": False},
        #     {"secondary_y": False}
        # ],
        # [  # Строка 2: блок выводов (занимает обе колонки)
        #     {"colspan": 2, "rowspan": 1},
        #     None  # Заполнитель для второй колонки
        # ],
        # [  # Строка 3: таблица (занимает обе колонки)
        #     {"type": "table", "colspan": 2, "rowspan": 1},
        #     None  # Заполнитель для второй колонки
        # ]
        [{"secondary_y": False}, {"secondary_y": False}],  # Строка 1: два графика
        [{"colspan": 2, "rowspan": 1}, None],             # Строка 2: блок выводов
        [{"type": "table"}, {"type": "table"}],            # Строка 3: две таблицы рядом
        [{"colspan": 2, "rowspan": 1, "secondary_y": False}, None]  # Строка 4: текстовый блок на всю ширину
    ]
)

# Добавляем общий заголовок
dashboard.add_annotation(
    x=0.5,
    y=1.08,  # Располагаем над графиками первой строки
    xref='paper',
    yref='paper',
    text='<b>Анализ конкурентов</b>',
    showarrow=False,
    font=dict(size=20, color='rgb(55, 83, 109)'),
    align='center'
)

# Добавляем fig1 (график 1) в ячейку (1,1)
for trace in fig1.data:
    if hasattr(trace, 'showlegend'):
        trace.showlegend = False
    dashboard.add_trace(trace, row=1, col=1)

# Добавляем fig2 (график 2) в ячейку (1,2)
for trace in fig2.data:
    if hasattr(trace, 'showlegend'):
        trace.showlegend = False
    dashboard.add_trace(trace, row=1, col=2)

# Добавляем блок текстовых выводов в строку 2 (занимает обе колонки) — используем 'paper' для привязки
dashboard.add_annotation(
    x=0.5,
    y=0.65,  # Позиция внутри дашборда (под графиками)
    xref='paper',  # Корректный формат: 'paper'
    yref='paper',  # Корректный формат: 'paper'
    text=(
        "<b>Ключевые выводы:</b><br><br>"
        "• НЕКС-Т, КВАНТ и ИНТЕРТАЧ — лидеры по количеству моделей интерактивных панелей 75″<br>"
        "• Лидеры по количеству закупок по ФЗ 44 / 223 - Т-ГЕККО, УТС и БИЭМ групп (за период с 2020 г. по 22.02.2026 по данным <a href='https://zakupki.gov.ru/epz/main/public/home.html' style='color: blue; text-decoration: underline;'>ЕИС</a>)<br>"
        
    ),
    showarrow=False,
    font=dict(size=12, color='rgb(55, 83, 109)'),
    align='left',
    borderpad=6,
    bgcolor='rgba(240, 248, 255, 0.7)',
    bordercolor='rgb(55, 83, 109)',
    borderwidth=1
)

# Добавляем заголовок «Целевая аудитория» в строку 3
dashboard.add_annotation(
    x=0.5,
    y=0.55,  # Позиция под блоком выводов
    xref='paper',
    yref='paper',
    text='<b>Целевая аудитория</b>',
    showarrow=False,
    font=dict(size=20, color='rgb(55, 83, 109)'),
    align='center'
)

# Добавляем fig3 (таблица 3) в строку 3 (занимает обе колонки)
for trace in fig3.data:
    dashboard.add_trace(trace, row=3, col=1)


for trace in fig4.data:
    dashboard.add_trace(trace, row=3, col=2)


# Добавляем блок текстовых данных о географии заказчиков
dashboard.add_annotation(
    x=0.5,
    y=0.43,  # Позиция внутри дашборда (под графиками)
    xref='paper',  # Корректный формат: 'paper'
    yref='paper',  # Корректный формат: 'paper'
    text=(
        "<b>Топ‑5 регионов по количеству заказчиков:</b><br><br>"
        "1) Санкт‑Петербург и ЛО — 45+ организаций (детские сады, школы, колледжи, соццентры).<br>"
        "2) Москва и МО — 35+ организаций (школы, вузы, департаменты).<br>"
        "3) Вологодская область — 15+ организаций (соццентры, училища).<br>"
        "4) Удмуртия — 12+ организаций (больницы, колледжи).<br>"
        "5) Калининградская область — 10+ организаций (школы‑интернаты, музеи).<br>"


    ),
    showarrow=False,
    font=dict(size=11, color='rgb(55, 83, 109)'),
    align='left',
    borderpad=6,
    bgcolor='rgba(240, 248, 255, 0.7)',
    bordercolor='rgb(55, 83, 109)',
    borderwidth=1
)




dashboard.add_annotation(
    x=0.5,
    y=0.1,
    xref='paper',
    yref='paper',
    text=(
        "<b>Рекомендации:</b><br><br>"
        "Фокус на образование и соцобслуживание — эти отрасли составляют 65 % ЦА.<br>"
        "Региональное развитие: <br>"
        "  * усилить присутствие в ЦФО (Москва, МО) и СЗФО (СПб, ЛО);<br>"
        "  * рассмотреть расширение в ПФО (Татарстан, Удмуртия) и СФО (Новосибирская, Омская области).<br>"
        "Адаптация продуктов: для школ — интерактивное оборудование, мебель, ПО; для больниц — медтехника российского производства; для соццентров — реабилитационное оборудование.<br>"
        " "
        "<b>Основные выводы по ЦА:</b><br><br>"  
        " "  
        "* ЦА распределена неравномерно: 60 % — ЦФО и СЗФО.<br>"
        "* Доминирующие отрасли: образование (45 %) и соцобслуживание (20 %).<br>"
        "* Основной тип заказчика — бюджетное учреждение (школа, больница, соццентр).<br>"
        "* Ключевые регионы для продаж: Москва, СПб, Вологодская, Калининградская, Удмуртская области.<br>"
    ),
    showarrow=False,
    font=dict(size=12, color='rgb(55, 83, 109)'),
    align='left',
    borderpad=10,
    bgcolor='rgba(240, 248, 255, 0.7)',
    bordercolor='rgb(55, 83, 109)',
    borderwidth=1,
    xanchor='center',
    yanchor='middle'
)




dashboard.update_xaxes(
    title_text="Количество моделей, шт.",  # Подпись для первого графика
    row=1,
    col=1
)
dashboard.update_xaxes(
    title_text="Количество закупок, ед.",  # Подпись для второго графика
    range=[0, 130],  # Минимум = 0, максимум = 100
    row=1,
    col=2
)



# Финальная настройка дашборда
dashboard.update_layout(
    height=1100,
    width=1700,
    title_text="",  # Убираем внутренний заголовок Plotly
    margin=dict(l=100, r=50, t=100, b=50),  # Минимум внешних отступов
    template='plotly_white',
    showlegend=False
)

# Отображаем итоговый дашборд
dashboard.show()

# Сохраняем в файлы
dashboard.write_html("дашборд_лига_групп_тестовое.html")
# dashboard.write_image("строгий_дашборд.png")
