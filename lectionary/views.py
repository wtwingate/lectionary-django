import datetime as dt
import json

from django.shortcuts import get_object_or_404, render

from lectionary.models import Day
from lectionary.services.lectionary import Lectionary


def index(request):
    start_date = dt.date.today()
    end_date = start_date + dt.timedelta(weeks=4)

    try:
        format = "%Y-%m-%d"
        start_date = dt.datetime.strptime(request.GET.get("start"), format).date()
        end_date = dt.datetime.strptime(request.GET.get("end"), format).date()
    except (TypeError, ValueError):
        pass

    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += dt.timedelta(days=1)

    calendar = []
    for date in dates:
        calendar.append(Lectionary(date))

    return render(request, "lectionary/index.html", {"calendar": calendar})


def detail(request, pk):
    day = get_object_or_404(Day, pk=pk)

    lessons = []
    for lesson in day.lesson_set.all():
        html = lesson.get_html()
        text = lesson.get_text()

        lessons.append(
            {
                "ref": lesson.reference,
                "html": html,
                "text": text,
            }
        )

    texts = json.dumps("\n".join([lesson["text"] for lesson in lessons]))

    context = {
        "day": day,
        "lessons": lessons,
        "texts": texts,
    }

    return render(request, "lectionary/detail.html", context=context)


def about(request):
    return render(request, "lectionary/about.html")
