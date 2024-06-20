import os
import pytest
import requests
from requests.models import Response
from bin_alert import BinApp
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('PushoverApiToken', 'dummy_api_token')
    monkeypatch.setenv('UserToken', 'dummy_user_token')
    monkeypatch.setenv('ApiUrl', 'https://dummyapi.com')
    monkeypatch.setenv('BinUrl', 'https://dummybinurl.com')
    
def test_bin_env(mock_env_vars):
    app = BinApp()
    assert app.api_token == 'dummy_api_token'
    assert app.user_token == 'dummy_user_token'
    assert app.api_url == 'https://dummyapi.com'
    assert app.bin_url == 'https://dummybinurl.com'
    
def test_bin_logging():
    app = BinApp()
    assert os.path.exists('./app.log')
    
@patch('bin_alert.requests.get')
def test_bin_site_call(mock_get, mock_env_vars):
    mock_html_content = '''
    <html>
        <fieldset>
            <p>Your next Blue Bin day is Tomorrow.</p>
        </fieldset>
        <span id="Application_AddressForUPRN">123 Main St</span>
    </html>
    '''
    response = MagicMock(spec=Response)
    response.content = mock_html_content
    mock_get.return_value = response

    app = BinApp()
    app.bin_site_call()

    assert app.formatted_message == '<b>123 Main St</b>\n<a href="https://dummybinurl.com">Bin Calendar</a>\n<font color=#0000FF>Tomorrow: Blue Bin</font>'
    assert app.send == True
    
@patch('bin_alert.requests.post')
def test_send_message(mock_post, mock_env_vars):
    app = BinApp()
    app.send = True
    app.message_dict = {
        'token': 'dummy_api_token',
        'user': 'dummy_user_token',
        'title': 'Bin Reminder',
        'message': '<b>123 Main St</b>\n<a href="https://dummybinurl.com">Bin Calendar</a>\n<font color=#0000FF>Tomorrow: Blue Bin</font>',
        'html': 1
    }
    
    response = MagicMock(spec=Response)
    response.raise_for_status = MagicMock()
    mock_post.return_value = response

    app.send_message()
    mock_post.assert_called_once_with('https://dummyapi.com', json=app.message_dict)
