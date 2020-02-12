import uuid
from datetime import timedelta

from django.utils import timezone

import pytest

from apps.core.tests.base_test_utils import mock_email_service_function
from apps.users.constants.messages import EXPIRED_LINK_MESSAGE

from .constants import USER_ACCOUNT_DATA_URL

pytestmark = pytest.mark.django_db


def test_create_user_info_link_anon_user(client):
    response = client.post(USER_ACCOUNT_DATA_URL)
    assert response.status_code == 400


def test_create_user_info_link_auth_user(logged_in_client, user, mocker):
    mocked_email_func = mock_email_service_function(mocker, "_send_message")

    assert user.account_info_link is None
    assert user.last_account_info_created is None

    response = logged_in_client.post(USER_ACCOUNT_DATA_URL)
    assert response.status_code == 200

    user.refresh_from_db()
    assert user.account_info_link is not None
    assert user.last_account_info_created is not None
    assert mocked_email_func.call_count == 2


def test_get_user_info_link_anon_user(client):
    response = client.post(USER_ACCOUNT_DATA_URL, args=["some_hash"])
    assert response.status_code == 400


def test_get_user_info_link_auth_user(logged_in_client, user):
    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now()
    user.save()

    user.refresh_from_db()

    response = logged_in_client.post(
        USER_ACCOUNT_DATA_URL, args=[str(user.account_info_link)]
    )
    assert response.status_code == 200
    assert response.data == []


def test_get_user_info_link_auth_user_expired_link(logged_in_client, user, settings):
    settings.ACCOUNT_INFO_LINK_AVAILABILITY_IN_DAYS = 5

    user.account_info_link = uuid.uuid4()
    user.last_account_info_created = timezone.now() - timedelta(days=6)
    user.save()

    user.refresh_from_db()

    response = logged_in_client.post(
        USER_ACCOUNT_DATA_URL, args=[str(user.account_info_link)]
    )
    assert response.status_code == 400
    assert response.data["messages"][0] == f"non_field_errors: {EXPIRED_LINK_MESSAGE}"


def test_get_user_info_link_other_user(logged_in_client, user_factory):
    other_user = user_factory(
        account_info_link=uuid.uuid4(), last_account_info_created=timezone.now()
    )

    response = logged_in_client.post(
        USER_ACCOUNT_DATA_URL, args=[str(other_user.account_info_link)]
    )
    assert response.status_code == 400
    assert response.data["messages"][0] == f"non_field_errors: {EXPIRED_LINK_MESSAGE}"
