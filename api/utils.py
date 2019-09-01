def get_day_name_from_int(day_integer):
    days = {
        1: "Pazartesi",
        2: "Salı",
        3: "Çarşamba",
        4: "Perşembe",
        5: "Cuma",
        6: "Cumartesi",
        7: "Pazar"
    }

    return days.get(day_integer, "")
