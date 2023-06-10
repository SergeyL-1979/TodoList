from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from bot.tg.client import TgClient
from core.models import User
from tests import factories


@pytest.mark.django_db
class TestTgUser:
    url: str = reverse('bot:verify')

    def test_bot_verify(self, auth_client, user: User):
        tg_user = factories.TuserFactory.create(
            chat_id='124315315',
            user_ud='124315315',
            username='test_user',
            user=user,
            verification_code='correct'
        )
        payload = {'verification_code': 'correct'}  # A A A

        with patch.object(TgClient, "send_message") as mock:
            response = auth_client.patch(self.url, data=payload)

        tg_user.refresh_from_db()
        assert tg_user.user == user
        assert response.status_code == status.HTTP_200_OK
        mock.assert_called_once_with(tg_user.chat_id, '[verification has been completed]')

    def test_incorrect(self, auth_client, client, user: User):
        tg_user = factories.TuserFactory.create(
            chat_id='124315315',
            user_ud='124315315',
            username='test_user',
            user=user,
            verification_code='correct'
        )
        payload = {'verification_code': 'incorrect'}

        with patch.object(TgClient, "send_message") as mock:
            response = auth_client.patch(self.url, data=payload)
            mock.assert_not_called()

        tg_user.refresh_from_db()
        assert tg_user.user == user
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock.assert_not_called()

# ================= ОРИГИНАЛ =====================
# @pytest.mark.django_db
# def test_bot_verify(auth_client, user: TgUser):
#     factories.TuserFactory.create(
#         chat_id='124315315',
#         user_ud='124315315',
#         username='test_user',
#         user=user,
#         verification_code='correct'
#     )
#     url: str = reverse('bot:verify')
#     payload1 = {'verification_code': 'correct'}
#     payload2 = {'verification_code': 'incorrect'}
#
#     with patch.object(TgClient, "send_message") as mock:
#
#         response1 = auth_client.patch(
#             path=url,
#             data=payload1,
#         )
#         mock.assert_called_once_with(124315315, '[verification has been completed]')
#
#     with patch.object(TgClient, "send_message") as mock:
#         response2 = auth_client.patch(
#             path=url,
#             data=payload2,
#         )
#         mock.assert_not_called()
#
#     assert response1.status_code == status.HTTP_200_OK
#     assert response2.status_code == status.HTTP_400_BAD_REQUEST
