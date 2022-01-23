import random

from datacenter.models import Mark, Chastisement, Lesson, Commendation, Schoolkid, Subject


COMMENDATIONS = [
    "Молодец!",
    "Отлично!",
    "Хорошо!",
    "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!",
    "Великолепно!",
    "Прекрасно!",
    "Ты меня очень обрадовал!",
    "Именно этого я давно ждал от тебя!",
    "Сказано здорово – просто и ясно!",
    "Ты, как всегда, точен!",
    "Очень хороший ответ!",
    "Талантливо!",
    "Ты сегодня прыгнул выше головы!",
    "Я поражен!",
    "Уже существенно лучше!",
    "Потрясающе!",
    "Замечательно!",
    "Прекрасное начало!",
    "Так держать!",
    "Ты на верном пути!",
    "Здорово!",
    "Это как раз то, что нужно!",
    "Я тобой горжусь!",
    "С каждым разом у тебя получается всё лучше!",
    "Мы с тобой не зря поработали!",
    "Я вижу, как ты стараешься!",
    "Ты растешь над собой!",
    "Ты многое сделал, я это вижу!",
    "Теперь у тебя точно все получится!",
]


def get_schoolkid(name):
    if not name:
        raise ValueError('Имя не может быть пустым')
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name)
    except Schoolkid.DoesNotExist:
        raise ValueError(f'Ошибка. Ученика с именем {name} не найдено.')
    except Schoolkid.MultipleObjectsReturned:
        raise ValueError(f'Ошибка. Имени {name} соответвует несколько учеников.')
    return schoolkid


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def get_subject(subject_title, year_of_study):
    try:
        subject = Subject.objects.get(title=subject_title, year_of_study=year_of_study)
    except (Subject.DoesNotExist, Subject.MultipleObjectsReturned) as e:
        raise ValueError(f'Проверьте написание предмета ({subject_title}). Оно должно быть в точности как на сайте.')
    return subject


def create_commendation(schoolkid_name, subject_title):
    schoolkid = get_schoolkid(schoolkid_name)
    subject = get_subject(subject_title, schoolkid.year_of_study)

    commendations_dates = (
        Commendation.objects.filter(
            schoolkid=schoolkid,
            subject=subject
        )
        .values_list('created', flat=True)
    )
    last_lesson_without_commendation = (
        Lesson.objects
        .filter(
            year_of_study=schoolkid.year_of_study, 
            group_letter=schoolkid.group_letter,
            subject=subject,
        )
        .exclude(date__in=commendations_dates)
        .order_by('-date')
        .first()
    )
    if not last_lesson_without_commendation:
        raise ValueError('По заданному предмету не найдены уроки без похвалы')
    Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=last_lesson_without_commendation.date,
        schoolkid=schoolkid,
        subject=last_lesson_without_commendation.subject,
        teacher=last_lesson_without_commendation.teacher
    )


if __name__ == '__main__':
    pass
