import numpy as np
import pandas as pd
import json


def gen_express(coef, dispersion, max_coef):
    sum_coef = 1.0
    while sum_coef < max_coef:
        current_coef = np.random.uniform(coef - dispersion, coef + dispersion)
        current_prob = 1.0 / current_coef
        real_prob = current_prob - 0.035
        test_prob = np.random.uniform(0.0, 1.0)
        if test_prob <= real_prob:
            sum_coef *= current_coef
        else:
            sum_coef = 0.0
            return sum_coef
    return sum_coef


def simulation(coef, dispersion, max_coef, bet_size):
    start_sum = 100.0
    current_sum = start_sum
    vin_sum = 10000.0
    steps = 10
    for step in range(steps):
        coef_exp = gen_express(coef, dispersion, max_coef)
        if coef_exp > 0:
            current_sum += (current_sum * bet_size) * coef_exp
        else:
            current_sum -= current_sum * bet_size
        if current_sum < 5.0:
            return "pass", step
        if current_sum > vin_sum:
            return "win", step
    return "win", step


def enumeration_of_options():
    dict_result = {}
    list_coef = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    list_dispersion = [0.01, 0.02, 0.03, 0.04]
    list_max_coef = [1.5, 2.0, 2.5, 3.0]
    list_bet_size = [0.1, 0.2, 0.3, 0.4, 0.5]
    list_type = ['Win', 'Count win step', 'Loss', 'Count loss step']
    df_list_coef = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]
    df_list_dispersion = [0.01, 0.02, 0.03, 0.04]
    df_list_max_coef = [1.5, 2.0, 2.5, 3.0]
    df_list_bet_size = [0.1, 0.2, 0.3, 0.4, 0.5]
    # temp = list(itertools.chain(*zip(my_list, my_list)))
    df_list_type = ['Win', 'Count win step', 'Loss', 'Count loss step'] * 320
    # Создание уровней заголовков
    arrays = [
        list_bet_size,  # Первый уровень (основные столбцы)
        list_max_coef,  # Второй уровень (подстолбцы)
        list_coef,  # Третий уровень (подстолбцы)
        list_type  # Четвертый уровень (подстолбцы)
    ]

    # Создание MultiIndex из уровней заголовков
    multi_columns = pd.MultiIndex.from_arrays(arrays, names=('Bet size', 'Max coefficient', 'Сoefficient', 'Result'))

    df = pd.DataFrame(columns=multi_columns)

    df.index = list_dispersion

    for bet_size in list_bet_size:
        for max_coef in list_max_coef:
            for cur_coef in list_coef:
                if cur_coef > max_coef:
                    continue
                for dispersion in list_dispersion:
                    win_count = 0
                    win_sum_count_step = 0
                    loss_sum_count_step = 0
                    steps = 20
                    for n in range(steps):
                        result, count_step = simulation(cur_coef, dispersion, max_coef, bet_size)
                        if result == "win":
                            win_count += 1
                            win_sum_count_step += count_step
                        else:
                            loss_sum_count_step += count_step
                    win_percent = win_count * 100 / steps
                    aver_win_sum_count_step = win_sum_count_step / win_count
                    aver_loss_sum_count_step = loss_sum_count_step / (steps - win_count)

                    df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Win')] = win_percent
                    df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Count win step')] = aver_win_sum_count_step
                    df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Loss')] = 100.0 - win_percent
                    df.loc[dispersion, (bet_size, max_coef, cur_coef, 'Count loss step')] = aver_loss_sum_count_step

                    # dict_result[f"{opt}/{dispersion}"] = {
                    #     "win": [win_percent, aver_win_sum_count_step],
                    #     "pass": [100.0 - win_percent, aver_pass_sum_count_step]
                    # }

    df.to_csv(result_csv_path, index=False)
    df.to_json(result_json_path, orient='records', lines=True)
    # with open(result_path, 'w') as json_file:
    #     json.dump(dict_result, json_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    result_json_path = "C:/Users/Kamil/code_others/game_strategy/result.json"
    result_csv_path = "C:/Users/Kamil/code_others/game_strategy/result.json"
    enumeration_of_options()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
