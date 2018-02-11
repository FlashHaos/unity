#!/usr/bin/python
# -*- coding: utf-8 -*-

import contextlib
import pytest

from unity.modules import xlsx


def test_example():
    bookfilename=r'C:\Temp\Хранимые объемы NBU v1.xlsx'
    sheetname='Хранимые по политике'
    picrange="A34:I52"
    picfilename=r'C:\Temp\test.png'
    with contextlib.closing(xlsx.Excel(bookfilename=bookfilename, sheetname=sheetname, visible=False)) as excel:
        excel.RefreshPivots()
        excel.SaveAsPicture(range=picrange,filename=picfilename)

if __name__ == '__main__':
    pytest.main('test_xlsx.py')