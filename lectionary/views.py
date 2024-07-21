import datetime as dt

from django.shortcuts import render, get_object_or_404

from lectionary.models import Day
from lectionary.services.lectionary import get_lectionary_data
from lectionary.services.scripture import get_esv_html


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
        lectionary_data.append(info)

    days = []
    for datum in lectionary_data:
        year, _, day_list = datum
        for name in day_list:
            matches = Day.objects.filter(name=name, year=year)
            for day in matches:
                days.append(day)

    return render(request, "lectionary/index.html", {"days": days})


def detail(request, pk):
    day = get_object_or_404(Day, pk=pk)

    lessons = []
    for lesson in day.lesson_set.all():
        lessons.append(
            {
                "reference": lesson.reference,
                "scripture": get_esv_html(lesson.reference),
            }
        )

    context = {
        "day": day,
        "lessons": lessons,
    }

    return render(request, "lectionary/detail.html", context=context)
