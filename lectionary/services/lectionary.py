import datetime as dt

from dateutil.easter import easter
from dateutil.relativedelta import SU, relativedelta

from lectionary.models import Day


class Lectionary:
    def __init__(self, date: dt.date):
        self.date = date
        self.moveable = self._get_moveable()
        self.year = self._get_year()
        self.season = self._get_season()
        self.days = self._get_days()

    def readable_date(self):
        return self.date.strftime("%A — %D")

    def _get_moveable(self) -> dict[str, dt.date]:
        easter_day = easter(self.date.year)
        moveable = {
            "easter_day": easter_day,
            "ash_wednesday": easter_day - dt.timedelta(days=46),
            "pentecost": easter_day + dt.timedelta(days=49),
            "advent_sunday": dt.date(self.date.year, 12, 25)
            + relativedelta(days=-1, weekday=SU(-4)),
        }
        return moveable

    def _get_year(self) -> str:
        if self.date >= self.moveable["advent_sunday"]:
            start_year = self.date.year
        else:
            start_year = self.date.year - 1

        if start_year % 3 == 0:
            return "A"
        if start_year % 3 == 1:
            return "B"
        return "C"

    def _get_season(self) -> str:
        if self.date < dt.date(self.date.year, 1, 6):
            return "Christmas"
        if self.date < self.moveable["ash_wednesday"]:
            return "Epiphany"
        if self.date < self.moveable["easter_day"]:
            return "Lent"
        if self.date < self.moveable["pentecost"]:
            return "Easter"
        if self.date < self.moveable["advent_sunday"]:
            return "Pentecost"
        if self.date < dt.date(self.date.year, 12, 25):
            return "Advent"
        return "Christmas"

    def _get_days(self) -> list[Day]:
        names = []
        names.append(self._check_principal_feasts())
        names.append(self._check_ash_wednesday())
        names.append(self._check_holy_week())
        names.append(self._check_easter_week())
        names.append(self._check_sundays())
        names.append(self._check_red_letter_days())

        days = []
        for name in names:
            if name is None:
                continue
            matches = Day.objects.filter(name=name, year=self.year)
            for match in matches:
                days.append(match)
        return days

    def _check_principal_feasts(self) -> str | None:
        if self.date == self.moveable["easter_day"]:
            return "Easter Day"
        if self.date == self.moveable["easter_day"] + dt.timedelta(days=39):
            return "Ascension Day"
        if self.date == self.moveable["pentecost"]:
            return "Day of Pentecost"
        if self.date == self.moveable["easter_day"] + dt.timedelta(days=56):
            return "Trinity Sunday"
        if self.date == dt.date(self.date.year, 12, 25):
            return "Christmas Day"
        if self.date == dt.date(self.date.year, 1, 6):
            return "The Epiphany"
        if self.date == dt.date(self.date.year, 11, 1):
            return "All Saints' Day"

    def _check_ash_wednesday(self) -> str | None:
        if self.date == self.moveable["ash_wednesday"]:
            return "Ash Wednesday"

    def _check_holy_week(self) -> str | None:
        date_delta = self.moveable["easter_day"] - self.date
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

    def _check_easter_week(self) -> str | None:
        date_delta = self.date - self.moveable["easter_day"]
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

    def _check_sundays(self) -> str | None:
        if self.date.weekday() != 6:
            return None

        if self.season == "Advent":
            return self._check_advent_sundays()
        if self.season == "Christmas":
            return self._check_christmas_sundays()
        if self.season == "Epiphany":
            return self._check_epiphany_sundays()
        if self.season == "Lent":
            return self._check_lent_sundays()
        if self.season == "Easter":
            return self._check_easter_sundays()
        if self.season == "Pentecost":
            return self._check_pentecost_sundays()

    def _check_advent_sundays(self) -> str | None:
        date_delta = self.date - self.moveable["advent_sunday"]
        if date_delta.days == 0:
            return "First Sunday of Advent"
        if date_delta.days == 7:
            return "Second Sunday of Advent"
        if date_delta.days == 14:
            return "Third Sunday of Advent"
        if date_delta.days == 21:
            return "Fourth Sunday of Advent"

    def _check_christmas_sundays(self) -> str | None:
        christmas_day = dt.date(self.date.year, 12, 25)
        if christmas_day < self.date <= christmas_day + dt.timedelta(days=7):
            return "First Sunday after Christmas"
        else:
            return "Second Sunday after Christmas"

    def _check_epiphany_sundays(self) -> str | None:
        first_sunday_of_epiphany = dt.date(self.date.year, 1, 6) + relativedelta(
            days=+1, weekday=SU(+1)
        )
        date_delta = self.date - first_sunday_of_epiphany

        # The number of Sundays after Epiphany can range from 4 to 9.
        # To account for this, check for the final two Sundays first.
        if self.date == self.moveable["easter_day"] - dt.timedelta(days=56):
            return "Second to Last Sunday after Epiphany"
        if self.date == self.moveable["easter_day"] - dt.timedelta(days=49):
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

    def _check_lent_sundays(self) -> str | None:
        date_delta = self.moveable["easter_day"] - self.date
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

    def _check_easter_sundays(self) -> str | None:
        date_delta = self.date - self.moveable["easter_day"]
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

    def _check_pentecost_sundays(self) -> str | None:
        date_delta = self.moveable["advent_sunday"] - self.date
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

    def _check_red_letter_days(self) -> str | None:
        if self.date == dt.date(self.date.year, 11, 30):
            return "Saint Andrew"
        if self.date == dt.date(self.date.year, 12, 21):
            return "Saint Thomas"
        if self.date == dt.date(self.date.year, 12, 26):
            return "Saint Stephen"
        if self.date == dt.date(self.date.year, 12, 27):
            return "Saint John"
        if self.date == dt.date(self.date.year, 12, 28):
            return "Holy Innocents"
        if self.date == dt.date(self.date.year, 1, 1):
            return "Holy Name"
        if self.date == dt.date(self.date.year, 1, 18):
            return "Confession of Saint Peter"
        if self.date == dt.date(self.date.year, 1, 25):
            return "Conversion of Saint Paul"
        if self.date == dt.date(self.date.year, 2, 2):
            return "The Presentation"
        if self.date == dt.date(self.date.year, 2, 24):
            return "Saint Matthias"
        if self.date == dt.date(self.date.year, 3, 19):
            return "Saint Joseph"
        if self.date == dt.date(self.date.year, 3, 25):
            return "The Annunciation"
        if self.date == dt.date(self.date.year, 4, 25):
            return "Saint Mark"
        if self.date == dt.date(self.date.year, 5, 1):
            return "Saint Philip and Saint James"
        if self.date == dt.date(self.date.year, 5, 31):
            return "The Visitation"
        if self.date == dt.date(self.date.year, 6, 11):
            return "Saint Barnabas"
        if self.date == dt.date(self.date.year, 6, 24):
            return "Nativity of Saint John the Baptist"
        if self.date == dt.date(self.date.year, 6, 29):
            return "Saint Peter and Saint Paul"
        if self.date == dt.date(self.date.year, 7, 22):
            return "Saint Mary Magdalene"
        if self.date == dt.date(self.date.year, 7, 25):
            return "Saint James"
        if self.date == dt.date(self.date.year, 8, 6):
            return "The Transfiguration"
        if self.date == dt.date(self.date.year, 8, 15):
            return "Saint Mary the Virgin"
        if self.date == dt.date(self.date.year, 8, 24):
            return "Saint Bartholomew"
        if self.date == dt.date(self.date.year, 9, 14):
            return "Holy Cross Day"
        if self.date == dt.date(self.date.year, 9, 21):
            return "Saint Matthew"
        if self.date == dt.date(self.date.year, 9, 29):
            return "Saint Michael and All Angels"
        if self.date == dt.date(self.date.year, 10, 18):
            return "Saint Luke"
        if self.date == dt.date(self.date.year, 10, 23):
            return "Saint James of Jerusalem"
        if self.date == dt.date(self.date.year, 10, 28):
            return "Saint Simon and Saint Jude"
