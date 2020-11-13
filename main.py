import PySimpleGUI as sg
from math import floor
import copy

payout = {
    6: 10000,
    7: 36,
    8: 720,
    9: 360,
    10: 80,
    11: 252,
    12: 108,
    13: 72,
    14: 54,
    15: 180,
    16: 72,
    17: 180,
    18: 119,
    19: 36,
    20: 306,
    21: 1080,
    22: 144,
    23: 1800,
    24: 3600,
}


def create_window():
    sg.theme("Default1")

    inputs = ["", 1, 2, 3, 4, 5, 6, 7, 8, 9]
    input_vars = ["a1", "a2", "a3", "b1", "b2", "b3", "c1", "c2", "c3"]
    output_vars = ["row1", "row2", "row3", "col1", "col2", "col3", "diag1", "diag2"]

    col1 = [
        [sg.Text("Diag \\", key="diag1", size=(6, 1))],
        [sg.Text("Row 1", key="row1", size=(6, 1))],
        [sg.Text("Row 2", key="row2", size=(6, 1))],
        [sg.Text("Row 3", key="row3", size=(6, 1))],
    ]

    col2 = [
        [sg.Text("Col 1", key="col1", size=(6, 1))],
        [sg.Combo(inputs, default_value="", key="a1", size=(1, 1),)],
        [sg.Combo(inputs, default_value="", key="b1", size=(1, 1),)],
        [sg.Combo(inputs, default_value="", key="c1", size=(1, 1),)],
    ]

    col3 = [
        [sg.Text("Col 2", key="col2", size=(6, 1))],
        [sg.Combo(inputs, default_value="", key="a2", size=(1, 1),)],
        [sg.Combo(inputs, default_value="", key="b2", size=(1, 1),)],
        [sg.Combo(inputs, default_value="", key="c2", size=(1, 1),)],
    ]

    col4 = [
        [sg.Text("Col 3", key="col3", size=(6, 1))],
        [sg.Combo(inputs, default_value="", key="a3", size=(1, 1),)],
        [sg.Combo(inputs, default_value="", key="b3", size=(1, 1),)],
        [sg.Combo(inputs, default_value="", key="c3", size=(1, 1),)],
    ]

    col5 = [
        [sg.Text("Diag /", key="diag2", size=(6, 1))],
        [sg.Text()],
        [sg.Text()],
        [sg.Text()],
    ]

    col6 = [[sg.Button("Update", bind_return_key=True)]]

    layout = [
        [
            sg.Column(col1, element_justification="center"),
            sg.Column(col2, element_justification="center"),
            sg.Column(col3, element_justification="center"),
            sg.Column(col4, element_justification="center"),
            sg.Column(col5, element_justification="center"),
            sg.Column(
                col6, element_justification="center", vertical_alignment="center"
            ),
        ],
        [sg.Button("Instructions"), sg.HorizontalSeparator(), sg.Button("Exit",),],
    ]

    window = sg.Window("Cactpot Solver", layout)

    while True:  # Event Loop
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Instructions":
            sg.popup_annoying(
                "Instructions:",
                'Enter the numbers that appear on the Mini Cactpot board into the appropriate squares. Click the "Update" button and two things will happen:',
                "1. The suggested next square will highlight",
                "2. The row, diag, col values will reflect estimated prize winnings if selected",
            )
        elif event == "Update":
            for val in inputs:
                if inputs.count(val) > 1 and val != "":
                    sg.popup_annoying("Duplicates not allowed!")
                    continue
            output_values = estimate_values(values)
            for out in output_vars:
                window[out].update(output_values[out][3])

            loc = next_guess(output_values)

    window.close()


def estimate_values(values):
    table = {
        "row1": [values["a1"], values["a2"], values["a3"]],
        "row2": [values["b1"], values["b2"], values["b3"]],
        "row3": [values["c1"], values["c2"], values["c3"]],
        "col1": [values["a1"], values["b1"], values["c1"]],
        "col2": [values["a2"], values["b2"], values["c2"]],
        "col3": [values["a3"], values["b3"], values["c3"]],
        "diag1": [values["a1"], values["b2"], values["c3"]],
        "diag2": [values["a3"], values["b2"], values["c1"]],
    }

    next_table = copy.deepcopy(table)

    used_numbers = set([int(x) for x in values.values() if x != ""])
    used_numbers.discard("")
    one_ten = set([x + 1 for x in range(9)])
    unused_numbers = one_ten - used_numbers

    for group in table:
        for loc in range(len(table[group])):
            if table[group][loc] == "":
                table[group][loc] = list(unused_numbers)
            else:
                table[group][loc] = [int(table[group][loc])]

    for group in table:
        comb = [
            [i, j, k]
            for i in table[group][0]
            for j in table[group][1]
            if j != i
            for k in table[group][2]
            if k != j and k != i
        ]
        for ele in range(len(comb)):
            comb[ele] = sorted(comb[ele])
        comb = set(tuple(i) for i in comb)

        sums = []
        for item in comb:
            # print(item)
            sums.append(payout[sum(item)])
        table[group].append(floor(sum(sums) / len(sums)))

    # for group in next_table:
    #     comb = [
    #         [i, j, k]
    #         for i in table[group][0]
    #         for j in table[group][1]
    #         if j != i
    #         for k in table[group][2]
    #         if k != j and k != i
    #     ]
    #
    #     sums = []
    #     for item in comb:
    #         sums.append(item + payout[sum(item)])
    #
    #     next_table[group].append(sums[0])
    #
    # print(next_table)

    return table


def next_guess(estimates):
    loc = ""
    return loc


if __name__ == "__main__":
    create_window()
