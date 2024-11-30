import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from plottable import Table, ColumnDefinition
import imgkit

green_cmap = {
    "header": "#63d297",
    "color1": "#e7f9ef",
    "color2": "#ffffff",
    "footer": "#afe9ca"
}
yellow_cmap = {
    "header": "#f7cb4d",
    "color1": "#fef8e3",
    "color2": "#ffffff",
    "footer": "#fce8b2"
}

def plot_calls(df):
    col_defs = [
        ColumnDefinition(name="Сотрудник", textprops={"ha": "left"}, width=1),
        ColumnDefinition(name="Иш куни", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Келмаган куни", textprops={"ha": "right"}, width=0.5, title="Келмаган\nкуни"),
        ColumnDefinition(name="Қолган иш куни", textprops={"ha": "right"}, width=0.5, title="Қолган иш\nкуни"),
        ColumnDefinition(name="3 минут", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="30 секунд", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="исходящий", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Длительность разговора(мин)", textprops={"ha": "right"}, width=0.6, title="Длительность\nразговора(мин)"),
        ColumnDefinition(name="Долг (исходящие)", textprops={"ha": "right"}, width=0.5, title="Долг\n(исходящие)")
    ]
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_title("Kunlik qo'ng'iroqlar", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    # ax.set_facecolor(green_cmap["header"])
    # fig.set_facecolor(green_cmap["header"])
    table = Table(
        df,
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.3}
        )
    table.set_alternating_row_colors(color=green_cmap["color1"], color2=green_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(green_cmap["footer"])
    fig.savefig("data/processed/call_number.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/call_number.png"


def plot_productivity(df):
    red = "#ea4335"
    green = "#63d297"

    # Not working because of alternating rows
    cmap = LinearSegmentedColormap.from_list(
        name="rank_difference", colors=[red, "white", green], N=3
    )

    col_defs = [
        ColumnDefinition(name="Рейтинг", textprops={"ha": "center"}, width=0.4),
        ColumnDefinition(name="Рейтинг ўзгариши", textprops={"ha": "right"}, width=0.4, title="Рейтинг\nўзгариши"),
        ColumnDefinition(name="Прогноз", textprops={"ha": "right"}, width=1.2),
        ColumnDefinition(name="Сотув хозирги", textprops={"ha": "right"}, width=0.5, title="Сотув\nхозирги"),
        ColumnDefinition(name="Ўзгариш 17-дастурга нисбатан", textprops={"ha": "right"}, width=0.6, title="Ўзгариш\n17-дастурга\nнисбатан", cmap=cmap),
        ColumnDefinition(name="Унумдорлик", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Қўшимча сотув прогнози", textprops={"ha": "right"}, width=0.6, title="Қўшимча сотув\nпрогнози"),
        ColumnDefinition(name="Умумий сотув прогнози", textprops={"ha": "right"}, width=0.6, title="Умумий сотув\nпрогнози"),
        ColumnDefinition(name="Бонус прогноз%", textprops={"ha": "right"}, width=0.5, title="Бонус\nпрогноз%")
    ]
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.set_title("Sotuv unimdorligi", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    # fig.set_facecolor(green_cmap["header"])
    table = Table(
        df,
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.7}
        )
    table.set_alternating_row_colors(color=green_cmap["color1"], color2=green_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(green_cmap["footer"])
    fig.savefig("data/processed/productivity.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/productivity.png"
    


def plot_call_time(df):
    col_defs = [
        ColumnDefinition(name="Сотрудник", textprops={"ha": "left"}, width=1),
        ColumnDefinition(name="исходящий", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Длительность разговора (мин)", textprops={"ha": "right"}, width=0.7, title="Длительность\nразговора (мин)"),
        ColumnDefinition(name="Пришел(а)", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Время первого звонка", textprops={"ha": "right"}, width=0.7, title="Время первого\nnзвонка"),
        ColumnDefinition(name="с 10:00 до 13:00 исходящий", textprops={"ha": "right"}, width=0.7, title="с 10:00 до 13:00\nисходящий"),
        ColumnDefinition(name="с 10:00 до 13:00 (мин)", textprops={"ha": "right"}, width=0.7, title="с 10:00 до 13:00\n(мин)"),
        ColumnDefinition(name="с 13:00 до 16:00 исходящий", textprops={"ha": "right"}, width=0.7, title="с 13:00 до 16:00\nисходящий"),
        ColumnDefinition(name="с 13:00 до 16:00 (мин)", textprops={"ha": "right"}, width=0.7, title="с 13:00 до 16:00\n(мин)"),
        ColumnDefinition(name="после 16:00 исходящий", textprops={"ha": "right"}, width=0.7, title="после 16:00\nисходящий"),
        ColumnDefinition(name="после 16:00 (мин)", textprops={"ha": "right"}, width=0.7, title="после 16:00\n(мин)")
    ]

    fig, ax = plt.subplots(figsize=(20, 6))
    ax.set_title("Vaqt kesimi bo'yicha qo'ng'iroqlar", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    table = Table(
        df, 
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.3}
    )
    table.set_alternating_row_colors(color=green_cmap["color1"], color2=green_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(green_cmap["footer"])
    fig.savefig("data/processed/call_time.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/call_time.png"
    


def plot_leads(df):
    col_defs = [
        ColumnDefinition(name="Менежерлар", textprops={"ha": "left"}, width=1),
        ColumnDefinition(name="Лидлар сони", textprops={"ha": "right"}, width=0.3),
        ColumnDefinition(name="Қўнғироқ қилинмаган", textprops={"ha": "right"}, width=0.4, title="Қўнғироқ\nқилинмаган"),
        ColumnDefinition(name="Қўнғироқ қилинди", textprops={"ha": "right"}, width=0.4, title="Қўнғироқ\nқилинди"),
        ColumnDefinition(name="Ўртача қўнғироқ сони", textprops={"ha": "right"}, width=0.6, title="Ўртача\nқўнғироқ сони"),
        ColumnDefinition(name="Битта ҳам ижобий қўнғироқ бўлмаганлар", textprops={"ha": "right"}, width=0.8, title="Битта ҳам ижобий\nқўнғироқ бўлмаганлар"),
        ColumnDefinition(name=">30", textprops={"ha": "right"}, width=0.3),
        ColumnDefinition(name=">180", textprops={"ha": "right"}, width=0.3),
    ]
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_title("Leadlar bo'yicha hisobot", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    # fig.set_facecolor(green_cmap["header"])
    table = Table(
        df,
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.7}
        )
    table.set_alternating_row_colors(color=green_cmap["color1"], color2=green_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(green_cmap["footer"])
    table.rows[table.n_rows-2].set_facecolor(green_cmap["footer"])
    fig.savefig("data/processed/leads.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/leads.png"
    


def plot_tur(df):
    col_defs = [
        ColumnDefinition(name="Менежер", textprops={"ha": "left"}, width=0.7),
        ColumnDefinition(name="100% тўлов", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Қарздор", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Жами Сотув", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Қарз Сумма", textprops={"ha": "right"}, width=0.5)
    ]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Milliard tur", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    # ax.set_facecolor(yellow_cmap["header"])
    table = Table(
        df,
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.3}
        )
    table.set_alternating_row_colors(color=yellow_cmap["color1"], color2=yellow_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(yellow_cmap["footer"])
    fig.savefig("data/processed/tur.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/tur.png"
    

def plot_milliard(df):
    col_defs = [
        ColumnDefinition(name="Менежер", textprops={"ha": "left"}, width=0.7),
        ColumnDefinition(name="100% тўлов", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Қарздор", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Жами Сотув", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Қарз Сумма", textprops={"ha": "right"}, width=0.5)
    ]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title("Badal bo'yicha hisobot", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    # ax.set_facecolor(yellow_cmap["header"])
    table = Table(
        df,
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.3}
        )
    table.set_alternating_row_colors(color=yellow_cmap["color1"], color2=yellow_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(yellow_cmap["footer"])
    fig.savefig("data/processed/milliard.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/milliard.png"
    

def plot_dastur(df):
    col_defs = [
        ColumnDefinition(name="Менежер", textprops={"ha": "left"}, width=1.2),
        ColumnDefinition(name="100% тўлов", textprops={"ha": "right"}, width=0.4),
        ColumnDefinition(name="Бартер", textprops={"ha": "right"}, width=0.4),
        ColumnDefinition(name="5 mln +", textprops={"ha": "right"}, width=0.4),
        ColumnDefinition(name="3 mln-4,9 mln", textprops={"ha": "right"}, width=0.5, title="3 mln-4,9\nmln"),
        ColumnDefinition(name="3 mln -", textprops={"ha": "right"}, width=0.5),
        ColumnDefinition(name="Жами Сотув", textprops={"ha": "right"}, width=0.5, title="Жами\nСотув"),
        ColumnDefinition(name="Жами сотув сумма", textprops={"ha": "right"}, width=0.7, title="Жами сотув\nсумма"),
        ColumnDefinition(name="Тушган сумма", textprops={"ha": "right"}, width=0.7),
        ColumnDefinition(name="Қарз Сумма", textprops={"ha": "right"}, width=0.6)
    ]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title("18-Dastur bo'yicha to'lovlar", fontdict={'family':'serif','color':'black','size':20}, pad=20)
    # ax.set_facecolor(yellow_cmap["header"])
    table = Table(
        df,
        textprops={"fontsize": 10},
        column_definitions=col_defs,
        col_label_cell_kw={"height": 1.3}
        )
    table.set_alternating_row_colors(color=green_cmap["color1"], color2=green_cmap["color2"])
    table.rows[table.n_rows-1].set_facecolor(green_cmap["footer"])
    fig.savefig("data/processed/dastur.png", pad_inches=0.1, bbox_inches='tight', dpi=300)
    plt.close()
    return "data/processed/dastur.png"
    

def __create_table_html(table_data):
    def cell_style(style_dict):
        """Generate inline style string from style dictionary"""
        return f' style="background-color: {style_dict["bgcolor"]}; font-size: {style_dict["font_size"]}; color: {style_dict.get("color", "black")}"'
    
    return f"""
    <div class="table-container">
        <table>
            <tr>
                <td colspan="3"{cell_style(table_data['header_style'])}>
                    {table_data['header']}
                </td>
            </tr>
            <tr>
                <td colspan="2"{cell_style(table_data['merged_ab_style'])}>
                    {table_data['merged_ab']}
                </td>
                <td{cell_style(table_data['c2_style'])}>
                    {table_data['c2']}
                </td>
            </tr>
            <tr>
                <td{cell_style(table_data['a3_style'])}>
                    {table_data['a3']}
                </td>
                <td{cell_style(table_data['b3_style'])}>
                    {table_data['b3']}
                </td>
                <td rowspan="3"{cell_style(table_data['c3_c5_style'])}>
                    {table_data['c3_c5']}
                </td>
            </tr>
            <tr>
                <td{cell_style(table_data['a4_style'])}>
                    {table_data['a4']}
                </td>
                <td{cell_style(table_data['b4_style'])}>
                    {table_data['b4']}
                </td>
            </tr>
            <tr>
                <td{cell_style(table_data['a5_style'])}>
                    {table_data['a5']}
                </td>
                <td{cell_style(table_data['b5_style'])}>
                    {table_data['b5']}
                </td>
            </tr>
        </table>
    </div>
    """


def plot_weekly_sales(df):
    html = """
    <html>
    <head>
    <style>
    table {
        border-collapse: collapse;
        width: 600px;
        font-family: Arial, sans-serif;
        margin: 20px auto;
    }
    th, td {
        border: 1px solid black;
        padding: 15px;
        text-align: center;
    }
    .table-container {
        margin-bottom: 40px;
    }
    </style>
    </head>
    <body>
    """

    COMMON_STYLES = {
        'header_style': {
            'bgcolor': '#434343',
            'font_size': '14px',
            'color': "white"
        },
        'merged_ab_style': {
            'bgcolor': '#C5D3E8',
            'font_size': '14px'
        },
        'c2_style': {
            'bgcolor': '#C5D3E8',
            'font_size': '14px'
        },
        'a3_style': {
            'bgcolor': '#BAFFB4',
            'font_size': '14px'
        },
        'b3_style': {
            'bgcolor': '#BAFFB4',
            'font_size': '14px'
        },
        'a4_style': {
            'bgcolor': '#FFFDA2',
            'font_size': '14px'
        },
        'b4_style': {
            'bgcolor': '#FFFDA2',
            'font_size': '14px'
        },
        'a5_style': {
            'bgcolor': '#FF6363',
            'font_size': '14px'
        },
        'b5_style': {
            'bgcolor': '#FF6363',
            'font_size': '14px'
        },
        'c3_c5_style': {
            'bgcolor': '#4D96FF',
            'font_size': '30px'
        }
    }
    for table in df:
        table.update(COMMON_STYLES)
        html += __create_table_html(table_data=table)

    html += """
    </body>
    </html>
    """
    with open('data/processed/weekly_sales.html', 'w', encoding='utf-8') as f:
        f.write(html)

    options = {
        'format': 'png',
        'encoding': "UTF-8",
        'quality': 100,
        'width': 800,
    }

    imgkit.from_file('data/processed/weekly_sales.html', 'data/processed/weekly_sales.png', options=options)
    return "data/processed/weekly_sales.png"