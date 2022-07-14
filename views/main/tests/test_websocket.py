import asyncio
import pytest


@pytest.mark.asyncio
async def test_after_connect(user_gamaz, user_bydlo):
    data = await user_gamaz.receive_json()
    assert data == {'code': 100, 'data': []}

    data = await user_bydlo.receive_json()
    assert data == {'code': 100, 'data': []}


@pytest.mark.asyncio
async def test_start_timer(user_gamaz, user_bydlo):
    await user_gamaz.send_json({'action': 'toggle', 'value': 1})

    data = await user_bydlo.receive_json()
    assert data.get('code') == 101
    assert data.get('data').get('event') == 'started'

    data = await user_gamaz.receive_json()
    assert data.get('code') == 101
    assert data.get('data').get('event') == 'started'


@pytest.mark.asyncio
async def test_wait_timer_tick(user_gamaz, user_bydlo):
    await asyncio.sleep(0.5)

    data = await user_bydlo.receive_json()
    assert data.get('code') == 102
    assert data.get('data').get('event') == 'started'

    data = await user_gamaz.receive_json()
    assert data.get('code') == 102
    assert data.get('data').get('event') == 'started'


@pytest.mark.asyncio
async def test_stop_timer(user_gamaz, user_bydlo):
    await user_bydlo.send_json({'action': 'toggle', 'value': 0})

    data = await user_bydlo.receive_json()
    assert data.get('code') == 102
    assert data.get('data').get('event') == 'stopped'

    data = await user_gamaz.receive_json()
    assert data.get('code') == 102
    assert data.get('data').get('event') == 'stopped'
