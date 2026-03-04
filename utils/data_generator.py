import random
import string
import time
from datetime import datetime, timedelta


class DataGenerator:
    """Генератор тестовых данных для пациентов"""

    MALE_NAMES = [
        'Александр', 'Дмитрий', 'Михаил', 'Андрей', 'Сергей',
        'Владимир', 'Алексей', 'Иван', 'Евгений', 'Николай',
        'Роман', 'Павел', 'Константин'
    ]
    FEMALE_NAMES = [
        'Анна', 'Елена', 'Ольга', 'Мария', 'Наталья', 'Ирина',
        'Светлана', 'Татьяна', 'Екатерина', 'Юлия', 'Анастасия',
        'Виктория', 'Дарья'
    ]
    MALE_SURNAMES = [
        'Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов',
        'Попов', 'Васильев', 'Павлов', 'Семенов', 'Голубев',
        'Виноградов', 'Богданов'
    ]
    FEMALE_SURNAMES = [
        'Иванова', 'Петрова', 'Сидорова', 'Смирнова', 'Кузнецова',
        'Попова', 'Васильева', 'Павлова', 'Семенова', 'Голубева',
        'Виноградова', 'Богданова'
    ]
    MALE_MIDDLENAMES = [
        'Александрович', 'Дмитриевич', 'Михайлович', 'Андреевич',
        'Сергеевич', 'Владимирович', 'Алексеевич', 'Иванович',
        'Евгеньевич', 'Николаевич'
    ]
    FEMALE_MIDDLENAMES = [
        'Александровна', 'Дмитриевна', 'Михайловна', 'Андреевна',
        'Сергеевна', 'Владимировна', 'Алексеевна', 'Ивановна',
        'Евгеньевна', 'Николаевна'
    ]

    TRANSLIT = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }

    @classmethod
    def name(cls, gender='male') -> str:
        return random.choice(cls.MALE_NAMES if gender == 'male' else cls.FEMALE_NAMES)

    @classmethod
    def surname(cls, gender='male') -> str:
        return random.choice(cls.MALE_SURNAMES if gender == 'male' else cls.FEMALE_SURNAMES)

    @classmethod
    def middlename(cls, gender='male') -> str:
        return random.choice(cls.MALE_MIDDLENAMES if gender == 'male' else cls.FEMALE_MIDDLENAMES)

    @classmethod
    def phone(cls) -> str:
        """Генерация номера по маске +79XXXXXXXXX"""
        suffix = ''.join(random.choices('0123456789', k=9))
        return f"+79{suffix}"

    @classmethod
    def email(cls, firstname=None, surname=None) -> str:
        domains = ['gmail.com', 'yandex.ru', 'mail.ru', 'outlook.com']
        domain = random.choice(domains)
        if firstname and surname:
            fn = cls._to_latin(firstname.lower())
            sn = cls._to_latin(surname.lower())
            username = f"{fn}.{sn}"
        else:
            username = ''.join(random.choices(string.ascii_lowercase, k=8))
        numbers = ''.join(random.choices('0123456789', k=3))
        return f"{username}{numbers}@{domain}"

    @classmethod
    def unique_email(cls) -> str:
        """Email с timestamp — гарантированно уникальный"""
        return f"patient{int(time.time())}@test.com"

    @classmethod
    def birthday(cls, min_age=18, max_age=70) -> str:
        """Дата рождения в формате ДД.ММ.ГГГГ"""
        now = datetime.now()
        max_birth = now - timedelta(days=min_age * 365)
        min_birth = now - timedelta(days=max_age * 365)
        days_range = (max_birth - min_birth).days
        birth_date = min_birth + timedelta(days=random.randint(0, days_range))
        return birth_date.strftime("%d.%m.%Y")

    @classmethod
    def patient(cls, gender='male') -> dict:
        """Полный набор данных пациента одним вызовом"""
        fn = cls.name(gender)
        sn = cls.surname(gender)
        mn = cls.middlename(gender)
        return {
            'firstname': fn,
            'surname': sn,
            'middlename': mn,
            'birthday': cls.birthday(),
            'gender': gender,
            'phone': cls.phone(),
            'email': cls.email(fn, sn)
        }

    @classmethod
    def _to_latin(cls, text: str) -> str:
        return ''.join(cls.TRANSLIT.get(ch, ch) for ch in text)
