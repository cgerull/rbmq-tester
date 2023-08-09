"""
Unit test for configuration module
"""

from importlib import reload
import pytest
import yaml
import os

import rbmq_config

TEST_CONFIG_FILE = 'rbmq-unittest.yml'

@pytest.fixture(params=['default'])
def generate_config_parameters(request):
    """ Reference set for default, file and envirnment parameters. """
    expected_default_result = {
        'host': 'localhost',
        'port': 5672,
        'ssl_port': 5671,
        'user': 'guest',
        'pw': 'guest',
        'vhost': 'local',
        'exchange': 'myExchg',
        'queue': 'myMQ',
        'routing_key': '',
        'endless': True,
        'payload': '',
        'interval': 0,
        'ssl_enabled': True,
        'mode': 'consume'
    }
    expected_file_result = {
        'host': 'localhost',
        'port': 5672,
        'ssl_port': 5671,
        'user': 'rbmq_user',
        'pw': 'rbmq_pass',
        'vhost': 'local',
        'exchange': 'myExchg',
        'queue': 'testq',
        'routing_key': '',
        'endless': True,
        'payload': '',
        'interval': 10,
        'ssl_enabled': True,
        'mode': 'consume'
    }
    expected_env_result = {
        'host': 'mytesthost',
        'port': 5671,
        'ssl_port': 5671,
        'user': 'test_user',
        'pw': 'test_pw',
        'vhost': '/myvhost',
        'exchange': 'test_exchg',
        'queue': 'test_q',
        'routing_key': 'rkey',
        'endless': True,
        'payload': 'test_payload',
        'interval': 60,
        'ssl_enabled': False,
        'mode': 'produce'
    }

    return expected_default_result, expected_file_result, expected_env_result


@pytest.fixture
def mock_set_environment(monkeypatch):
    """ Mock environment parameters. """
    test_environment = {
        'RBMQ_HOST': 'mytesthost',
        'RBMQ_PORT': '5671',
        'RBMQ_USER': 'test_user',
        'RBMQ_PASS': 'test_pw',
        'RBMQ_VHOST': '/myvhost',
        'RBMQ_QUEUE': 'test_q',
        'RBMQ_ROUTING_KEY': 'rkey',
        'RBMQ_EXCHANGE': 'test_exchg',
        'RBMQ_PAYLOAD': 'test_payload',
        'RBMQ_INTERVAL': '60',
        'RBMQ_SSL_ENABLED': 'False',
        'MODE': 'produce'
    }
    for key, value in test_environment.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def mock_config_file(tmpdir_factory):
    """ Write mock config file."""
    # 'rbmq-unittest.yml'config_file =
    config = {
        'host': 'localhost',
        'user': 'rbmq_user',
        'pw': 'rbmq_pass',
        'queue': 'testq',
        'interval': 10
    }
    with open(TEST_CONFIG_FILE , 'w', encoding="utf-8") as file:
        yaml.safe_dump(config, file)
    yield
    os.remove(TEST_CONFIG_FILE)


#
#####################################################
#
def test_default_config(generate_config_parameters):
    """ Test build-in default parameter set. """
    config = rbmq_config.Config('no-file.ymll')
    parameters = config.get_config()
    assert parameters == generate_config_parameters[0]


def test_file_config(mock_config_file, generate_config_parameters):
    """ Test parameters from mock config file. """
    reload(rbmq_config)
    # mock_config_file = 'rbmq-unittest.yml'
    config = rbmq_config.Config(TEST_CONFIG_FILE )
    parameters = config.get_config()
    assert parameters == generate_config_parameters[1]


def test_environment_config(mock_set_environment, generate_config_parameters):
    """ Test parameter override from environment variables. """
    reload(rbmq_config)
    config = rbmq_config.Config().get_config()
    assert config == generate_config_parameters[2]
