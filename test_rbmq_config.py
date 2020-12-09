import pytest
import os
import yaml
from importlib import reload

import rbmq_config

@pytest.fixture(params=['default'])
def generate_config_parameters(request):
    expected_default_result = {
        'host': 'localhost',
        'port': 5672,
        'user': 'guest',
        'pw': 'guest',
        'vhost': 'LOCAL',
        'exchange': '',
        'queue': 'hello-MQ',
        'endless': True,
        'payload': '',
        'interval': 0
    }
    expected_file_result = {
        'host': 'localhost',
        'port': 5672,
        'user': 'rbmq_user',
        'pw': 'rbmq_pass',
        'vhost': 'LOCAL',
        'exchange': '',
        'queue': 'testq',
        'endless': True,
        'payload': '',
        'interval': 10
    }
    expected_env_result = {
        'host': 'mytesthost',
        'port': 5671,
        'user': 'test_user',
        'pw': 'test_pw',
        'vhost': '/myvhost',
        'exchange': 'test_exchg',
        'queue': 'test_q',
        'endless': True,
        'payload': 'test_payload',
        'interval': 60
    }    

    return expected_default_result, expected_file_result, expected_env_result

@pytest.fixture
def mock_set_environment(monkeypatch):
    test_environment = {
        'RBMQ_HOST': 'mytesthost',
        'RBMQ_PORT': '5671',
        'RBMQ_USER': 'test_user',
        'RBMQ_PASS': 'test_pw',
        'RBMQ_VHOST': '/myvhost',
        'RBMQ_QUEUE': 'test_q',
        'RBMQ_EXCHANGE': 'test_exchg',
        'RBMQ_PAYLOAD': 'test_payload',
        'RBMQ_INTERVAL': '60'
    }
    for key, value in test_environment.items():
        monkeypatch.setenv(key, value)

@pytest.fixture
def mock_config_file(tmpdir_factory):
    config_file = 'rbmq-tester.yml'
    config = {
        'host': 'localhost',
        'user': 'rbmq_user',
        'pw': 'rbmq_pass',
        'queue': 'testq',
        'interval': 10
    }    
    with open(config_file, 'w') as f:
        yaml.safe_dump(config,f)
    yield
    os.remove(config_file)

#
#####################################################
#
def test_default_config(generate_config_parameters):
    config = rbmq_config.Config().get_config()
    assert config == generate_config_parameters[0]

def test_file_config(mock_config_file, generate_config_parameters):
    reload(rbmq_config)
    config = rbmq_config.Config().get_config()
    assert config == generate_config_parameters[1]


def test_environment_config(mock_set_environment, generate_config_parameters):
    reload(rbmq_config)
    config = rbmq_config.Config().get_config()
    assert config == generate_config_parameters[2]
