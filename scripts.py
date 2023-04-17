def fix_marks(full_name):
    from datacenter.models import Schoolkid
    from datacenter.models import Mark
    from django.core.exceptions import ObjectDoesNotExist
    from django.core.exceptions import MultipleObjectsReturned

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    except ObjectDoesNotExist:
        print(f"Человека '{full_name}', нет в вашей школе. Введите другое имя, фамилию")
        return
    except MultipleObjectsReturned:
        print(f"Нашлось несколько людей чье имя совпадает с введенным, уточните имя, желательно ввести полностью ФИО")
        return
    marks = Mark.objects.filter(schoolkid=schoolkid)
    bud_marks = marks.filter(points__in=[2, 3])
    bud_marks.update(points=5)
    print('Оценки исправлены')


def remove_chastisements(full_name):
    from datacenter.models import Schoolkid
    from datacenter.models import Chastisement
    from django.core.exceptions import ObjectDoesNotExist
    from django.core.exceptions import MultipleObjectsReturned

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=full_name)
    except ObjectDoesNotExist:
        print(f"Человека '{full_name}', нет в вашей школе. Введите другое имя, фамилию")
        return
    except MultipleObjectsReturned:
        print(f"Нашлось несколько людей чье имя совпадает с введенным, уточните имя, желательно ввести полностью ФИО")
        return

    remarks = Chastisement.objects.filter(schoolkid=schoolkid)
    remarks.delete()
    print('Жалобы удалены')


def create_commendation(name, lesson):
    import random
    from datacenter.models import Lesson
    from datacenter.models import Subject
    from datacenter.models import Schoolkid
    from datacenter.models import Commendation
    from django.core.exceptions import ObjectDoesNotExist
    from django.core.exceptions import MultipleObjectsReturned


    good_commendations = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]

    lessons = Lesson.objects.all()
    try:
        math_subject = Subject.objects.get(
            title=lesson,
            year_of_study=6
        )
    except ObjectDoesNotExist:
        print(f"Предмета '{lesson}' нет. Введите корректно название предмета")
        return

    try:
        math_lessons = lessons.filter(
            subject=math_subject,
            year_of_study=6,
            group_letter='А'
        )
    except ObjectDoesNotExist:
        print(f"В вашей параллели предмет '{lesson}' есть, но ваш класс его не проходит. Введите другой предмет")
        return

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except ObjectDoesNotExist:
        print(f"Человека '{name}', нет в вашей школе. Введите другое имя, фамилию")
        return
    except MultipleObjectsReturned:
        print(f"Нашлось несколько людей чье имя совпадает с введенным, уточните имя, желательно ввести полностью ФИО")
        return

    random_lesson = random.choice(math_lessons)
    Commendation.objects.create(
        text=random.choice(good_commendations),
        created=random_lesson.date,
        schoolkid=schoolkid,
        subject=math_subject,
        teacher=random_lesson.teacher
    )
    print('Похвала добавлена')
