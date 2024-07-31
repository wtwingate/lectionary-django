import datetime as dt
import json
import re

from django.shortcuts import get_object_or_404, render

from lectionary.models import Day
from lectionary.services.lectionary import get_lectionary_data
from psalter.models import Psalm
from psalter.services import parse_psalm_num


def index(request):
    start_date = dt.date.today()
    end_date = start_date + dt.timedelta(weeks=2)

    try:
        format = "%Y-%m-%d"
        start_date = dt.datetime.strptime(request.GET.get("start"), format).date()
        end_date = dt.datetime.strptime(request.GET.get("end"), format).date()
    except (TypeError, ValueError):
        pass

    selected_dates = []
    current_date = start_date
    while current_date <= end_date:
        selected_dates.append(current_date)
        current_date += dt.timedelta(days=1)

    lectionary_data = []
    for sd in selected_dates:
        info = get_lectionary_data(sd)
        if info is not None:
            lectionary_data.append(info)

    lectionary = []
    for datum in lectionary_data:
        date, year, season, day_list = datum
        for name in day_list:
            matches = Day.objects.filter(name=name, year=year)
            for day in matches:
                lectionary.append({"date": date, "day": day})

    return render(request, "lectionary/index.html", {"lectionary": lectionary})


def detail(request, pk):
    day = get_object_or_404(Day, pk=pk)

    lessons = []
    texts = []
    for lesson in day.lesson_set.all():
        if lesson.reference.startswith("Psalm"):
            number = parse_psalm_num(lesson.reference)
            psalm = get_object_or_404(Psalm, number=number)
            scripture = psalm.get_html(lesson.reference)
            text = psalm.get_text(lesson.reference)
        else:
            scripture = lesson.get_html()
            text = lesson.get_text()

        lessons.append(
            {
                "reference": lesson.reference,
                "scripture": scripture,
            }
        )
        texts.append(text)

    context = {
        "day": day,
        "lessons": lessons,
        "texts": json.dumps(texts),
    }

    return render(request, "lectionary/detail.html", context=context)
