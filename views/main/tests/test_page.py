import pytest


@pytest.mark.asyncio
async def test_main_page(user_san_sanych):
    response = await user_san_sanych.get('/')
    assert response.status_code == 200
    assert 'html' in response.text.lower()
