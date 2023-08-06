import xlrd
import os
import sys

class 条件表SheetData:
    def __init__(self, idColumnIndex):
        self.idColumnIndex = idColumnIndex
        self.dict = self.条件表Collect(self.idColumnIndex)

    def 条件表Collect(self, idColumnIndex):
        data = xlrd.open_workbook("E:\TestTools\getSheetData\conf\excel\condition.xlsx")
        table = data.sheet_by_name("条件表")
        rowNum = table.nrows
        colNum = table.ncols
        sourceHeadList = table.row_values(0)
        sourceIDList = []
        headList = []
        for i in sourceHeadList:
            if i != "":
                headList.append(i)
        for i in range(rowNum):
            sourceIDList.append(table.row_values(i)[idColumnIndex])
        firstDict = {}
        secondDict = {}
        for i in range(rowNum):
            for j in range(colNum):
                secondDict[sourceHeadList[j]] = table.cell(i, j)
            firstDict[sourceIDList[i]] = secondDict
            secondDict = {}  # reset secondDict
        return (firstDict)

    def getValueByID(self, key, columnname):
        return self.dict[key][columnname]