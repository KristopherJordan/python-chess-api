X_CONVERTER = dict(
    a=0,
    b=1,
    c=2,
    d=3,
    e=4,
    f=5,
    g=6,
    h=7,
)

X_INVERTER = {
    "0": "a",
    "1": "b",
    "2": "c",
    "3": "d",
    "4": "e",
    "5": "f",
    "6": "g",
    "7": "h",
}


Y_CONVERTER = {
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
    "8": 0,
}


Y_INVERTER = {
    "0": 8,
    "1": 7,
    "2": 6,
    "3": 5,
    "4": 4,
    "5": 3,
    "6": 2,
    "7": 1,
}


def convert_position(position):
    if len(position) != 2:
        raise Exception("Position in wrong format. Example 'e4'. Not: %s" % position)

    x = X_CONVERTER[position[0].lower()]
    y = Y_CONVERTER[position[1].lower()]
    return (y, x)


def readable_position(position):
    x = X_INVERTER[str(position[1])]
    y = Y_INVERTER[str(position[0])]
    return "%s%s" % (y, x)
