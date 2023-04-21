GOOD_COMMENDATIONS = [
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


def handle_schoolkid_exceptions(name, Schoolkid):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        print(f"Человека '{name}', нет в вашей школе. Введите другое имя, фамилию")
        raise Schoolkid.DoesNotExist
    except Schoolkid.MultipleObjectsReturned:
        print(f"Нашлось несколько людей чье имя совпадает с введенным, уточните имя,"
              f" желательно ввести полностью ФИО")
        raise Schoolkid.MultipleObjectsReturned
    return schoolkid


def fix_marks(name):
    from datacenter.models import Schoolkid
    from datacenter.models import Mark

    try:
        schoolkid = handle_schoolkid_exceptions(name, Schoolkid)
    except (Schoolkid.MultipleObjectsReturned, Schoolkid.DoesNotExist):
        return
    bud_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    bud_marks.update(points=5)
    print('Оценки исправлены')


def remove_chastisements(name):
    from datacenter.models import Schoolkid
    from datacenter.models import Chastisement

    try:
        schoolkid = handle_schoolkid_exceptions(name, Schoolkid)
    except (Schoolkid.MultipleObjectsReturned, Schoolkid.DoesNotExist):
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

    try:
        schoolkid = handle_schoolkid_exceptions(name, Schoolkid)
    except (Schoolkid.MultipleObjectsReturned, Schoolkid.DoesNotExist):
        return

    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter
    try:
        subject = Subject.objects.get(
            title=lesson,
            year_of_study=year_of_study
        )
    except Subject.DoesNotExist:
        print(f"Предмета '{lesson}' нет. Введите корректно название предмета")
        return

    math_lessons = Lesson.objects.filter(
        subject=subject,
        year_of_study=year_of_study,
        group_letter=group_letter
    )
    if not math_lessons:
        print(f"В вашей параллели предмет '{lesson}' есть, но"
              f" ваш класс его не проходит. Введите другой предмет")
        return

    random_lesson = random.choice(math_lessons)
    Commendation.objects.create(
        text=random.choice(GOOD_COMMENDATIONS),
        created=random_lesson.date,
        schoolkid=schoolkid,
        subject=subject,
        teacher=random_lesson.teacher
    )
    print('Похвала добавлена')
