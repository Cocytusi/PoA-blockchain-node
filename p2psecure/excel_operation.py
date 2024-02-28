import xlrd
import xlwt
from xlutils.copy import copy


class ExcelOperation:
    def __init__(self, book_name, sheet_name):
        self.book_name = book_name
        self.sheet_name = sheet_name
        self.workbook = xlwt.Workbook()  # 新建一个工作簿
        self.sheet = self.workbook.add_sheet(self.sheet_name)  # 在工作簿中新建一个表格

    def write_excel_xls(self, value):
        index = len(value)  # 获取需要写入数据的行数
        for i in range(0, index):
            for j in range(0, len(value[i])):
                self.sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
        self.workbook.save(self.book_name)  # 保存工作簿

    def write_excel_xls_append(self, value):
        index = len(value)  # 获取需要写入数据的行数
        workbook = xlrd.open_workbook(self.book_name)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
        new_workbook.save(self.book_name)  # 保存工作簿

    def read_excel_xls(self):
        workbook = xlrd.open_workbook(self.book_name)  # 打开read工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        for i in range(0, worksheet.nrows):
            for j in range(0, worksheet.ncols):
                print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据


if __name__ == "__main__":
    book_name_xls = 'exp_data.xls'

    sheet_name_xls = 'data'

    value_title = [["Seal number", "block transmission time"]]

    value1 = [[0.2, 0.5]]

    value2 = [["Tom", "男"],
              ["Jones", "女"],
              ["Cat", "女"]]

    eo = ExcelOperation(book_name_xls, sheet_name_xls)

    eo.write_excel_xls(value_title)
    eo.write_excel_xls_append(value1)
    eo.write_excel_xls_append(value2)
    eo.read_excel_xls()
