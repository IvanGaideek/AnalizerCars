import pandas as pd
import matplotlib.pyplot as plt


xls = pd.ExcelFile('data_cars.xlsx')
df = xls.parse(xls.sheet_names[0])
labels = df['Бренд'].tolist()[:-1]
values = df['Объем продаж'].tolist()[:-1]
print(df.to_dict())


def bar_graph():
    plt.figure(figsize=(13, 8))
    plt.bar(labels, values)
    plt.xticks(rotation=90)
    plt.show()


def pie_graph():
    plt.figure(figsize=(14, 14))
    plt.pie(values)
    plt.legend(labels)
    plt.axis('equal')
    plt.show()


def main():
    bar_graph()
    pie_graph()


if __name__ == "__main__":
    main()
