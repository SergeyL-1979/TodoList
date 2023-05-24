import random
from django.db import models

from core.models import User

CODE_VOCABULARY = "qwertyuasdfghkzxvbnm123456789"


class TgUser(models.Model):
    """ Минимальные поля в модели:
        - telegram chat_id
        - telegram user_ud
        - внутренний user_id пользователя (nullable поле)
    """
    chat_id = models.BigIntegerField(verbose_name='Чат ID')
    # tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    user_ud = models.BigIntegerField(verbose_name="user ud", unique=True)
    # tg_id = models.BigIntegerField(verbose_name="tg id", unique=True)
    username = models.CharField(max_length=512, verbose_name="tg username", null=True, blank=True, default=None)
    user = models.ForeignKey(User, models.PROTECT, null=True, blank=True, default=None,
                             verbose_name='Связанный пользователь')
    verification_code = models.CharField(max_length=32, verbose_name="Код подтверждения")

    def set_verification_code(self):
        code = "".join([random.choice(CODE_VOCABULARY) for _ in range(12)])
        self.verification_code = code

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = "Телеграм Пользователь"
        verbose_name_plural = "Телеграм Пользователи"
