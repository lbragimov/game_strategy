import numpy as np
import pandas as pd
import json

from collections import defaultdict
import matplotlib.pyplot as plt


def gen_express(coef, dispersion, max_coef):

    def exp_mapping(x, A=0.0223, B=0.015, C=0.00):
        return A * np.exp(B * x) + C

    sum_coef = 1.0
    if max_coef:
        while sum_coef < max_coef:
            current_coef = np.random.uniform(coef - dispersion, coef + dispersion)
            current_prob = 1.0 / current_coef

            real_prob = current_prob - exp_mapping(current_prob*100.0)
            test_prob = np.random.uniform(0.0, 1.0)
            if test_prob <= real_prob:
                sum_coef *= current_coef
            else:
                sum_coef = 0.0
                return sum_coef
    else:
        current_coef = np.random.uniform(coef - dispersion, coef + dispersion)
        current_prob = 1.0 / current_coef

        real_prob = current_prob - exp_mapping(current_prob * 100.0)
        test_prob = np.random.uniform(0.0, 1.0)
        if test_prob > real_prob:
            sum_coef = 0.0
            return sum_coef
    return sum_coef


def simulation(coef, dispersion, max_coef, bet_size_coef):
    start_sum = 20.0
    current_sum = start_sum
    win_sum = 1000.0
    steps = 70
    for step in range(steps):
        coef_exp = gen_express(coef, dispersion, max_coef)
        bet_size = round(current_sum * bet_size_coef, 2)
        if bet_size < 0.45:
            bet_size = 0.45
        elif bet_size > 250.0:
            bet_size = 250.0
        if coef_exp > 0:
            win_size = round(bet_size * coef_exp, 2)
            if win_size >= 300.0:
                win_size = win_size * 0.85
            current_sum += win_size
        else:
            current_sum -= bet_size
        if current_sum < 2.5:
            return "pass", step
        elif current_sum > win_sum:
            return "win", step
    return "pass", step


def enumeration_of_options():
    # dict_result = {}
    dict_result = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    list_bet_size = [0.25]
    list_max_coef = [1.15, 1.3]#, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.5, 3.0]
    list_coef = [1.15]#, 1.2, 1.25]#, 1.3]#, 1.4, 1.5, 1.6, 1.7, 1.8]
    list_dispersion = [0.00]#, 0.02]#, 0.03, 0.04]
    list_type = ['Win', 'Count win step', 'Loss', 'Count loss step']
    # df_list_bet_size = [0.1, 0.2, 0.3, 0.4, 0.5]
    # df_list_max_coef = [1.5, 2.0, 2.5, 3.0]
    # df_list_coef = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    # df_list_dispersion = [0.01, 0.02, 0.03, 0.04]
    # # temp = list(itertools.chain(*zip(my_list, my_list)))
    # df_list_type = ['Win', 'Count win step', 'Loss', 'Count loss step'] * 320
    # # Создание уровней заголовков
    # arrays = [
    #     list_bet_size,  # Первый уровень (основные столбцы)
    #     list_max_coef,  # Второй уровень (подстолбцы)
    #     list_coef,  # Третий уровень (подстолбцы)
    #     list_type  # Четвертый уровень (подстолбцы)
    # ]
    #
    # # Создание MultiIndex из уровней заголовков
    # multi_columns = pd.MultiIndex.from_arrays(arrays, names=('Bet size', 'Max coefficient', 'Сoefficient', 'Result'))
    #
    # df = pd.DataFrame(columns=multi_columns)
    #
    # df.index = list_dispersion

    for bet_size in list_bet_size:
        print(bet_size)
        for max_coef in list_max_coef:
            print("    " + f"{max_coef}")
            for cur_coef in list_coef:
                print("        " + f"{cur_coef}")
                if max_coef:
                    if cur_coef > max_coef:
                        continue

                win_percent = 0.0
                aver_win_sum_count_step = 0.0
                aver_loss_sum_count_step = 0.0

                for dispersion in list_dispersion:
                    dis_win_count = 0
                    win_sum_count_step = 0.0
                    loss_sum_count_step = 0.0
                    steps = 10000
                    for n in range(1, steps + 1):
                        result, count_step = simulation(cur_coef, dispersion, max_coef, bet_size)
                        if result == "win":
                            dis_win_count += 1
                            win_sum_count_step += count_step
                        else:
                            loss_sum_count_step += count_step
                    dis_win_percent = float(dis_win_count * 100.0 / steps)
                    if dis_win_count > 0:
                        dis_aver_win_sum_count_step = float(win_sum_count_step / dis_win_count)
                    else:
                        dis_aver_win_sum_count_step = float(0)
                    if steps == dis_win_count:
                        dis_aver_loss_sum_count_step = float(0)
                    else:
                        dis_aver_loss_sum_count_step = float(loss_sum_count_step / (steps - dis_win_count))

                    win_percent += dis_win_percent
                    aver_win_sum_count_step += dis_aver_win_sum_count_step
                    aver_loss_sum_count_step += dis_aver_loss_sum_count_step

                    # df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Win')] = win_percent
                    # df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Count win step')] = aver_win_sum_count_step
                    # df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Loss')] = 100.0 - win_percent
                    # df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Count loss step')] = aver_loss_sum_count_step

                win_percent = win_percent/len(list_dispersion)
                aver_win_sum_count_step = aver_win_sum_count_step/len(list_dispersion)
                aver_loss_sum_count_step = aver_loss_sum_count_step/len(list_dispersion)

                if win_percent < 65.0:
                    continue
                if aver_win_sum_count_step > 100:
                    continue
                dict_result[bet_size][max_coef][cur_coef] = {
                    "win": [round(win_percent, 1), round(aver_win_sum_count_step, 1)],
                    "pass": [round(100.0 - win_percent, 1), round(aver_loss_sum_count_step, 1)]
                }

    df = pd.DataFrame(dict_result)
    df.to_csv(result_csv_path, index=False)
    # df.to_json(result_json_path, orient='records', lines=True)
    with open(result_json_path, 'w') as json_file:
        json.dump(dict_result, json_file)


def grafic_1():
    # Функция нелинейной зависимости
    def nonlinear_mapping(x, L=0.1, x0=50, k=0.1):
        return L / (1 + np.exp(-k * (x - x0)))

    # Генерация значений для x от 0 до 100
    x_values = np.linspace(0, 100, 500)

    # Применение функции к значениям x
    y_values = nonlinear_mapping(x_values)

    # Построение графика
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label='Nonlinear Mapping', color='b')
    plt.title('Нелинейная зависимость')
    plt.xlabel('Значение (x)')
    plt.ylabel('Нелинейная функция f(x)')
    plt.grid(True)
    plt.axhline(y=0.05, color='r', linestyle='--', label='y = 0.05')
    plt.axhline(y=0.1, color='g', linestyle='--', label='y = 0.1')
    plt.legend()
    plt.show()
    print('hi')


def grafic_2():
    def exp_mapping(x, A=0.0223, B=0.015, C=0.00):
        return A * np.exp(B * x) + C

    # Генерация значений для x от 0 до 100
    x_values = np.linspace(0, 100, 500)

    # Применение функции к значениям x
    y_values = exp_mapping(x_values)

    # Построение графика
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, label='Exponential Mapping', color='b')
    plt.title('Экспоненциальная зависимость')
    plt.xlabel('Значение (x)')
    plt.ylabel('Значение функции f(x)')
    plt.grid(True)
    plt.axhline(y=0.05, color='r', linestyle='--', label='y = 0.05')
    plt.axhline(y=0.1, color='g', linestyle='--', label='y = 0.1')
    plt.legend()
    plt.show()
    print('hi')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result_json_path = "C:/Users/Kamil/code_others/game_strategy/result.json"
    result_csv_path = "C:/Users/Kamil/code_others/game_strategy/result.csv"
    # df = pd.read_json(result_json_path)
    # grafic_2()
    # print('hi')
    enumeration_of_options()
#
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
