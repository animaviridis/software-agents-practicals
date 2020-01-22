def validate(message, t=float):
    val = 0

    while True:
        val_str = input(message)
        if not val_str:
            continue

        try:
            val = t(val_str)
        except ValueError:
            print(f'Invalid input: {val} for conversion to {t}')
        else:
            break

    return val
