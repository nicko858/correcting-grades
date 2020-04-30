import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
django.setup()
from datacenter.models import Mark
from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
import random


def get_schoolkid(schoolkid_name):
    schoolkid = Schoolkid.objects.get(full_name=schoolkid_name)
    if len(schoolkid) > 1:
        raise Schoolkid.MultipleObjectsReturned
    return schoolkid


def fix_marks(grades, required_mark):
    for grade in poor_grades:
        grade.points = required_mark
        grade.save()


def get_poor_grades(schoolkid, poor_limit):
    return Mark.objects.filter(schoolkid=schoolkid, points__lte=poor_limit)


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def get_lessons(year_of_study, group_letter, subject):
    return Lesson.objects.filter(
        year_of_study=year_of_study,
        group_letter=group_letter,
        subject__title=subject,
        )


def create_commendation(schoolkid, text, lesson):
    Commendation.objects.create(
        schoolkid=schoolkid,
        text=text,
        subject=lesson.subject,
        teacher=lesson.teacher,
        created=lesson.date,
        )


if __name__ == "__main__":
    schoolkid_name = "Фролов Иван Григорьевич"
    year_of_study, group_letter = 6, "А"
    poor_limit, good_point = 3, 5
    subject_for_commendations = "Математика"
    lesson_step = 2
    commendation_phrases = [
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
    try:
        schoolkid = get_schoolkid(schoolkid_name)
    except Schoolkid.DoesNotExist:
        exit("Нет ученика с тамим именем - {0}".format(schoolkid_name))
    except Schoolkid.MultipleObjectsReturned:
        exit("Нaйдено больше 1 ученика с таким именем - {0}".format(
            schoolkid_name
            ))
    poor_grades = get_poor_grades(schoolkid, poor_limit)
    fix_marks(poor_grades, good_point)
    remove_chastisements(schoolkid)
    lessons = get_lessons(
        year_of_study,
        group_letter,
        subject_for_commendations,
        )
    for lesson in lessons[::lesson_step]:
        commendation_phrase = random.choice(commendation_phrases)
        create_commendation(schoolkid, commendation_phrase, lesson)
