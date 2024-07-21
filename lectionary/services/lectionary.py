from datetime import date, timedelta

from dateutil.easter import easter
from dateutil.relativedelta import SU, relativedelta


def get_lectionary_data(my_date: date) -> tuple[str, str, list[str]]:
    moveable_days = get_moveable_days(my_date)
    liturgical_year = get_liturgical_year(my_date, moveable_days)
    liturgical_season = get_liturgical_season(my_date, moveable_days)
    liturgical_days = get_liturgical_days(my_date, moveable_days, liturgical_season)

    return (
        liturgical_year,
        liturgical_season,
        list(filter(lambda day: day is not None, liturgical_days)),
    )


def get_moveable_days(my_date: date) -> dict[str, date]:
    easter_day = easter(my_date.year)
    principal_days = {
        "easter_day": easter_day,
        "ash_wednesday": easter_day - timedelta(days=46),
        "pentecost": easter_day + timedelta(days=49),
        "advent_sunday": date(my_date.year, 12, 25)
        + relativedelta(days=-1, weekday=SU(-4)),
    }
    return principal_days


def get_liturgical_year(my_date: date, moveable_days: dict[str, date]) -> str:
    if my_date >= moveable_days["advent_sunday"]:
        start_year = my_date.year
    else:
        start_year = my_date.year - 1

    if start_year % 3 == 0:
        return "A"
    if start_year % 3 == 1:
        return "B"
    return "C"


def get_liturgical_season(my_date: date, moveable_days: dict[str, date]) -> str:
    if my_date < date(my_date.year, 1, 6):
        return "CH"
    if my_date < moveable_days["ash_wednesday"]:
        return "EP"
    if my_date < moveable_days["easter_day"]:
        return "LE"
    if my_date < moveable_days["pentecost"]:
        return "EA"
    if my_date < moveable_days["advent_sunday"]:
        return "PE"
    if my_date < date(my_date.year, 12, 25):
        return "AD"
    return "CH"


def get_liturgical_days(
    my_date: date, moveable_days: dict[str, date], liturgical_season: str
) -> list[str]:
    liturgical_days = []
    liturgical_days.append(_check_principal_feasts(my_date, moveable_days))
    liturgical_days.append(_check_ash_wednesday(my_date, moveable_days))
    liturgical_days.append(_check_holy_week(my_date, moveable_days))
    liturgical_days.append(_check_easter_week(my_date, moveable_days))
    liturgical_days.append(_check_sundays(my_date, moveable_days, liturgical_season))
    liturgical_days.append(_check_red_letter_days(my_date))
    return liturgical_days


def _check_principal_feasts(
    my_date: date, moveable_days: dict[str, date]
) -> str | None:
    if my_date == moveable_days["easter_day"]:
        return "Easter Day"
    if my_date == moveable_days["easter_day"] + timedelta(days=39):
        return "Ascension Day"
    if my_date == moveable_days["pentecost"]:
        return "Day of Pentecost"
    if my_date == moveable_days["easter_day"] + timedelta(days=56):
        return "Trinity Sunday"
    if my_date == date(my_date.year, 12, 25):
        return "Christmas Day"
    if my_date == date(my_date.year, 1, 6):
        return "The Epiphany"
    if my_date == date(my_date.year, 11, 1):
        return "All Saints' Day"


def _check_ash_wednesday(my_date: date, moveable_days: dict[str, date]) -> str | None:
    if my_date == moveable_days["ash_wednesday"]:
        return "Ash Wednesday"


def _check_holy_week(my_date: date, moveable_days: dict[str, date]) -> str | None:
    date_delta = moveable_days["easter_day"] - my_date
    if date_delta.days == 7:
        return "Palm Sunday"
    if date_delta.days == 6:
        return "Monday in Holy Week"
    if date_delta.days == 5:
        return "Tuesday in Holy Week"
    if date_delta.days == 4:
        return "Wednesday in Holy Week"
    if date_delta.days == 3:
        return "Maundy Thursday"
    if date_delta.days == 2:
        return "Good Friday"
    if date_delta.days == 1:
        return "Holy Saturday"


def _check_easter_week(my_date: date, moveable_days: dict[str, date]) -> str | None:
    date_delta = my_date - moveable_days["easter_day"]
    if date_delta.days == 1:
        return "Monday in Easter Week"
    if date_delta.days == 2:
        return "Tuesday in Easter Week"
    if date_delta.days == 3:
        return "Wednesday in Easter Week"
    if date_delta.days == 4:
        return "Thursday in Easter Week"
    if date_delta.days == 5:
        return "Friday in Easter Week"
    if date_delta.days == 6:
        return "Saturday in Easter Week"


def _check_sundays(
    my_date: date, moveable_days: dict[str, date], liturgical_season: str
) -> str | None:
    if my_date.weekday() != 6:
        return None

    if liturgical_season == "AD":
        return _check_advent_sundays(my_date, moveable_days)
    if liturgical_season == "CH":
        return _check_christmas_sundays(my_date)
    if liturgical_season == "EP":
        return _check_epiphany_sundays(my_date, moveable_days)
    if liturgical_season == "LE":
        return _check_lent_sundays(my_date, moveable_days)
    if liturgical_season == "EA":
        return _check_easter_sundays(my_date, moveable_days)
    if liturgical_season == "PE":
        return _check_pentecost_sundays(my_date, moveable_days)


def _check_advent_sundays(my_date: date, moveable_days: dict[str, date]) -> str | None:
    date_delta = my_date - moveable_days["advent_sunday"]
    if date_delta.days == 0:
        return "First Sunday of Advent"
    if date_delta.days == 7:
        return "Second Sunday of Advent"
    if date_delta.days == 14:
        return "Third Sunday of Advent"
    if date_delta.days == 21:
        return "Fourth Sunday of Advent"


def _check_christmas_sundays(my_date: date) -> str | None:
    christmas_day = date(my_date.year, 12, 25)
    if christmas_day < my_date <= christmas_day + timedelta(days=7):
        return "First Sunday after Christmas"
    else:
        return "Second Sunday after Christmas"


def _check_epiphany_sundays(
    my_date: date, moveable_days: dict[str, date]
) -> str | None:
    first_sunday_of_epiphany = date(my_date.year, 1, 6) + relativedelta(
        days=+1, weekday=SU(+1)
    )
    date_delta = my_date - first_sunday_of_epiphany

    # The number of Sundays after Epiphany can range from 4 to 9.
    # To account for this, check for the final two Sundays first.
    if my_date == moveable_days["easter_day"] - timedelta(days=56):
        return "Second to Last Sunday after Epiphany"
    if my_date == moveable_days["easter_day"] - timedelta(days=49):
        return "Last Sunday after Epiphany"
    if date_delta.days == 0:
        return "First Sunday after Epiphany"
    if date_delta.days == 7:
        return "Second Sunday after Epiphany"
    if date_delta.days == 14:
        return "Third Sunday after Epiphany"
    if date_delta.days == 21:
        return "Fourth Sunday after Epiphany"
    if date_delta.days == 28:
        return "Fifth Sunday after Epiphany"
    if date_delta.days == 35:
        return "Sixth Sunday after Epiphany"
    if date_delta.days == 42:
        return "Seventh Sunday after Epiphany"
    if date_delta.days == 49:
        return "Eighth Sunday after Epiphany"


def _check_lent_sundays(my_date: date, moveable_days: dict[str, date]) -> str | None:
    date_delta = moveable_days["easter_day"] - my_date
    if date_delta.days == 42:
        return "First Sunday in Lent"
    if date_delta.days == 35:
        return "Second Sunday in Lent"
    if date_delta.days == 28:
        return "Third Sunday in Lent"
    if date_delta.days == 21:
        return "Fourth Sunday in Lent"
    if date_delta.days == 14:
        return "Fifth Sunday in Lent"


def _check_easter_sundays(my_date: date, moveable_days: dict[str, date]) -> str | None:
    date_delta = my_date - moveable_days["easter_day"]
    if date_delta.days == 7:
        return "Second Sunday of Easter"
    if date_delta.days == 14:
        return "Third Sunday of Easter"
    if date_delta.days == 21:
        return "Fourth Sunday of Easter"
    if date_delta.days == 28:
        return "Fifth Sunday of Easter"
    if date_delta.days == 35:
        return "Sixth Sunday of Easter"
    if date_delta.days == 42:
        return "Sunday after Ascension Day"


def _check_pentecost_sundays(
    my_date: date, moveable_days: dict[str, date]
) -> str | None:
    date_delta = moveable_days["advent_sunday"] - my_date
    if date_delta.days == 203:
        return "Proper 1"
    if date_delta.days == 196:
        return "Proper 2"
    if date_delta.days == 189:
        return "Proper 3"
    if date_delta.days == 182:
        return "Proper 4"
    if date_delta.days == 175:
        return "Proper 5"
    if date_delta.days == 168:
        return "Proper 6"
    if date_delta.days == 161:
        return "Proper 7"
    if date_delta.days == 154:
        return "Proper 8"
    if date_delta.days == 147:
        return "Proper 9"
    if date_delta.days == 140:
        return "Proper 10"
    if date_delta.days == 133:
        return "Proper 11"
    if date_delta.days == 126:
        return "Proper 12"
    if date_delta.days == 119:
        return "Proper 13"
    if date_delta.days == 112:
        return "Proper 14"
    if date_delta.days == 105:
        return "Proper 15"
    if date_delta.days == 98:
        return "Proper 16"
    if date_delta.days == 91:
        return "Proper 17"
    if date_delta.days == 84:
        return "Proper 18"
    if date_delta.days == 77:
        return "Proper 19"
    if date_delta.days == 70:
        return "Proper 20"
    if date_delta.days == 63:
        return "Proper 21"
    if date_delta.days == 56:
        return "Proper 22"
    if date_delta.days == 49:
        return "Proper 23"
    if date_delta.days == 42:
        return "Proper 24"
    if date_delta.days == 35:
        return "Proper 25"
    if date_delta.days == 28:
        return "Proper 26"
    if date_delta.days == 21:
        return "Proper 27"
    if date_delta.days == 14:
        return "Proper 28"
    if date_delta.days == 7:
        return "Proper 29"


def _check_red_letter_days(my_date: date) -> str | None:
    if my_date == date(my_date.year, 11, 30):
        return "Saint Andrew"
    if my_date == date(my_date.year, 12, 21):
        return "Saint Thomas"
    if my_date == date(my_date.year, 12, 26):
        return "Saint Stephen"
    if my_date == date(my_date.year, 12, 27):
        return "Saint John"
    if my_date == date(my_date.year, 12, 28):
        return "Holy Innocents"
    if my_date == date(my_date.year, 1, 1):
        return "Holy Name"
    if my_date == date(my_date.year, 1, 18):
        return "Confession of Saint Peter"
    if my_date == date(my_date.year, 1, 25):
        return "Conversion of Saint Paul"
    if my_date == date(my_date.year, 2, 2):
        return "The Presentation"
    if my_date == date(my_date.year, 2, 24):
        return "Saint Matthias"
    if my_date == date(my_date.year, 3, 19):
        return "Saint Joseph"
    if my_date == date(my_date.year, 3, 25):
        return "The Annunciation"
    if my_date == date(my_date.year, 4, 25):
        return "Saint Mark"
    if my_date == date(my_date.year, 5, 1):
        return "Saint Philip and Saint James"
    if my_date == date(my_date.year, 5, 31):
        return "The Visitation"
    if my_date == date(my_date.year, 6, 11):
        return "Saint Barnabas"
    if my_date == date(my_date.year, 6, 24):
        return "Nativity of Saint John the Baptist"
    if my_date == date(my_date.year, 6, 29):
        return "Saint Peter and Saint Paul"
    if my_date == date(my_date.year, 7, 22):
        return "Saint Mary Magdalene"
    if my_date == date(my_date.year, 7, 25):
        return "Saint James"
    if my_date == date(my_date.year, 8, 6):
        return "The Transfiguration"
    if my_date == date(my_date.year, 8, 15):
        return "Saint Mary the Virgin"
    if my_date == date(my_date.year, 8, 24):
        return "Saint Bartholomew"
    if my_date == date(my_date.year, 9, 14):
        return "Holy Cross Day"
    if my_date == date(my_date.year, 9, 21):
        return "Saint Matthew"
    if my_date == date(my_date.year, 9, 29):
        return "Saint Michael and All Angels"
    if my_date == date(my_date.year, 10, 18):
        return "Saint Luke"
    if my_date == date(my_date.year, 10, 23):
        return "Saint James of Jerusalem"
    if my_date == date(my_date.year, 10, 28):
        return "Saint Simon and Saint Jude"
