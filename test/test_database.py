#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import contextlib
import pytest

from unity.model import users

def test_users_crud():
    try:
        users.refreshdb()
    except:
        pass
    assert len(users.get())==0
    users.add(id=149812944,description='Суперюзер',role='admin')
    users.add(id=162333088,description='Юзер')
    with pytest.raises(TypeError):
        users.add()
    assert users.get()[0]['id']==149812944
    assert users.get()[1]['description']=='Юзер'
    assert users.get(id=149812944)['description']=='Суперюзер'
    assert users.get(162333088)['role']=='user'
    users.set(id=149812944,description='Сверхпользователь')
    assert users.get(id=149812944)['description']=='Сверхпользователь'
    users.set(id=162333088,role='admin')
    assert users.get(id=162333088)['role']=='admin'
    assert users.get(12345) == False
    assert len(users.get())==2
    users.remove(id=149812944)
    assert users.get(id=149812944) == False
    assert len(users.get())==1
    users.remove(id=162333088)
    assert len(users.get())==0
    with pytest.raises(ValueError):
        users.remove(id=12345)
    with pytest.raises(TypeError):
        users.remove()


if __name__ == '__main__':
    pytest.main('test_database.py')