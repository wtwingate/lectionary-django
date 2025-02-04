import datetime as dt
import json
import logging

from django.shortcuts import get_object_or_404, render

from lectionary.models import Day, DayLesson
from lectionary.services.lectionary import Lectionary


def index(request):
    logger = logging.getLogger("django")

    start_date = None
    end_date = None

    date_format = "%Y-%m-%d"

    try:
        start_date = dt.datetime.strptime(request.GET.get("start"), date_format).date()
    except (TypeError, ValueError) as e:
        logger.error(e)
    try:
        end_date = dt.datetime.strptime(request.GET.get("end"), date_format).date()
    except (TypeError, ValueError) as e:
        logger.error(e)

    if not start_date:
        start_date = dt.date.today()
    if not end_date:
        end_date = start_date + dt.timedelta(weeks=4)

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += dt.timedelta(days=1)

    calendar = {}
    for date in dates:
        lectionary = Lectionary(date)
        hr_date = date.strftime("%A, %D")
        calendar[hr_date] = []
        for name in lectionary.names:
            for day in Day.objects.filter(name=name, year=lectionary.year):
                lessons = [d.lesson for d in DayLesson.objects.filter(day=day)]
                calendar[hr_date].append(
                    {
                        "day": day,
                        "year": lectionary.year,
                        "season": lectionary.season,
                        "lessons": lessons,
                    }
                )

    # Remove all dates from calendar which have no lectionary data
    calendar = {k: v for k, v in calendar.items() if len(v) != 0}

    return render(request, "lectionary/index.html", {"calendar": calendar})


def detail(request, pk):
    day = get_object_or_404(Day, pk=pk)

    lessons = []
    for lesson in [d.lesson for d in DayLesson.objects.filter(day=day)]:
        html = lesson.get_html()
        text = lesson.get_text()

        lessons.append(
            {
                "ref": lesson.reference,
                "html": html,
                "text": text,
            }
        )

    collects = [collect.text for collect in day.collects.all()]

    texts = json.dumps("\n".join([lesson["text"] for lesson in lessons]))

    context = {
        "day": day,
        "collects": collects,
        "lessons": lessons,
        "texts": texts,
    }

    return render(request, "lectionary/detail.html", context=context)


def about(request):
    return render(request, "lectionary/about.html")
