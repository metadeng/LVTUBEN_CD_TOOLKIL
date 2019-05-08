# coding:utf-8


def flag2action(flag):
    switcher = {
        1: "ADDITION",
        2: "CHANGE",
        3: "DELETION",
        4: "GRANT",
    }
    return switcher.get(flag, '')
