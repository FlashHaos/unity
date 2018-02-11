#!/usr/bin/python
# -*- coding: utf-8 -*-

from unity.modules.configmodule import config
import win32com.client as win32
import os, logging
from PIL import ImageGrab


class Excel:

    def __init__(self,bookfilename=False,sheetname=False,visible=False):
        logging.debug('Создаётся объект Excel')
        try:
            self.application = win32.gencache.EnsureDispatch('Excel.Application')
            logging.debug('Закрываются текущие процессы Excel.Application')
            self.application.Quit()
            self.application.Visible = visible
            self.worksheet = None
            self.workbook = None
            self.worsheets_list = None
            logging.debug('Процессы Excel.Application завершены, переменные обнулены')
            logging.debug('Объект Excel создан')
        except Exception as e:
            logging.critical(e)
            logging.critical('Не удаётся открыть Excel.')
            raise OSError("Cannot open Excel application!")
        if bookfilename:
            self.OpenBook(bookfilename)
        if sheetname:
            self.OpenSheet(sheetname)

    def OpenBook(self,bookfilename):
        logging.debug('Открывается книга "{}"'.format(bookfilename))
        if self.worksheet:
            self.worksheet = None
        if self.workbook:
            self.workbook.Close(False)
            self.workbook = None
        if not os.path.isfile(bookfilename) :
            logging.critical('Книга "{}" не найдена.'.format(bookfilename))
            raise FileExistsError('Cannot find workbook file "{}"!'.format(bookfilename))
        self.workbook = self.application.Workbooks.Open(bookfilename)
        logging.debug('Книга "{}" открыта'.format(bookfilename))
        #получаем список имен листов
        logging.debug('Получение списка листов в книге "{}"'.format(bookfilename))
        self.worsheets_list=[]
        for i in range(1,65536):
            try:
                self.worsheets_list.append(self.workbook.Sheets(i).Name)
                logging.debug('Лист {}: "{}"'.format(i,self.workbook.Sheets(i).Name))
            except:
                break

    def OpenSheet(self, sheetname):
        logging.debug('Открывается лист "{}"'.format(sheetname))
        if not self.workbook:
            logging.critical('Невозможно совершать операции с книгой, если она не открыта.')
            raise OSError("Cannot do anything with workbook that is not opened!")
        if sheetname not in self.worsheets_list:
            logging.critical('Лист "{}" не найден в книге.'.format(sheetname))
            raise OSError('Worksheet "{}" does not exists!'.format(sheetname))
        if self.worksheet:
            self.worksheet = None
        self.worksheet = self.workbook.Worksheets(sheetname)
        logging.debug('Лист "{}" открыт'.format(sheetname))

    def RefreshPivots(self):
        logging.debug('Обновляются сводные таблицы на активном листе')
        # обновить сводные на этом листе
        if not self.workbook:
            logging.critical('Невозможно совершать операции с листом или книгой, если они не открыты.')
            raise OSError("Cannot do anything with workbook or worksheet that are not opened!")
        self.worksheet.Unprotect()  # IF protected
        pivots_count = self.worksheet.PivotTables().Count
        logging.debug('Найдено сводных таблиц: {}'.format(pivots_count))
        for j in range(1, pivots_count + 1):
            logging.debug('Обновление сводной таблицы "{}"'.format(self.worksheet.PivotTables(j).Name))
            try:
                self.worksheet.PivotTables(j).PivotCache().Refresh()
            except Exception as e:
                logging.error(e)
                if 'Сбой инициализации источника данных' in str(e):
                    logging.error('Внешняя БД недоступна. Невозможно обновить сводную таблицу "{}"'.format(self.worksheet.PivotTables(j).Name))
        self.workbook.Save()

    def SaveAsPicture(self,range,filename):
        if not self.workbook:
            logging.critical('Невозможно совершать операции с листом или книгой, если они не открыты.')
            raise OSError("Cannot do anything with workbook or worksheet that are not opened!")
        logging.debug('Копируется диапазон "{}" с активного листа "{}"'.format(range,self.worksheet.Name))
        self.worksheet.Range(range).CopyPicture()
        logging.debug('Скопированный элемент сохраняется с использованием временной книги')
        self.tempworkbook = self.application.Workbooks.Add()
        self.tempworksheet = self.tempworkbook.ActiveSheet
        self.tempworksheet.Paste()
        self.tempworksheet.Shapes('Picture 1').Copy()
        img = ImageGrab.grabclipboard()
        imgFile = os.path.join(filename)
        logging.debug('Запись в файл "{}"'.format(filename))
        img.save(imgFile)
        self.tempworkbook.Close(False)
        self.tempworksheet = None
        self.tempworkbook = None


    def close(self):
        logging.debug('Завершение работы с файлом "{}"'.format(self.workbook.Name))
        logging.debug('Закрываются документы, обнуляются переменные')
        if self.worksheet:
            self.worksheet = None
        if self.workbook:
            self.workbook.Close(False)
            self.workbook = None
        logging.debug('Завершаются процессы Excel.Application')
        if self.application:
            self.application.Quit()
            self.application = None

if __name__=="__main__":
    pass