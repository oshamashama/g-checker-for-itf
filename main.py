import sys
import csv
import re
from tokenize import String
from xmlrpc.client import boolean
import json
import argparse

MAX = 10000


class Color:
	BLACK          = '\033[30m'#(文字)黒
	RED            = '\033[31m'#(文字)赤
	GREEN          = '\033[32m'#(文字)緑
	YELLOW         = '\033[33m'#(文字)黄
	BLUE           = '\033[34m'#(文字)青
	MAGENTA        = '\033[35m'#(文字)マゼンタ
	CYAN           = '\033[36m'#(文字)シアン
	WHITE          = '\033[37m'#(文字)白
	COLOR_DEFAULT  = '\033[39m'#文字色をデフォルトに戻す
	BOLD           = '\033[1m'#太字
	UNDERLINE      = '\033[4m'#下線
	INVISIBLE      = '\033[08m'#不可視
	REVERCE        = '\033[07m'#文字色と背景色を反転
	BG_BLACK       = '\033[40m'#(背景)黒
	BG_RED         = '\033[41m'#(背景)赤
	BG_GREEN       = '\033[42m'#(背景)緑
	BG_YELLOW      = '\033[43m'#(背景)黄
	BG_BLUE        = '\033[44m'#(背景)青
	BG_MAGENTA     = '\033[45m'#(背景)マゼンタ
	BG_CYAN        = '\033[46m'#(背景)シアン
	BG_WHITE       = '\033[47m'#(背景)白
	BG_DEFAULT     = '\033[49m'#背景色をデフォルトに戻す
	RESET          = '\033[0m'#全てリセット

OK_COLOR_STR = f'{Color.RESET}{Color.GREEN}{Color.BOLD}'
FEATURE_COLOR_STR = f'{Color.RESET}{Color.CYAN}'
FAIL_COLOR_STR = f'{Color.RESET}{Color.RED}{Color.BOLD}'
RESET_COLOR_STR = f'{Color.RESET}'




class Dir():
    name:String
    max_certificated_credit_num:int
    now_certificated_credit_num:int
    feature_certificated_credit_num:int
    min_certificated_credit_num:int
    is_frame:bool   # if is_frame, filter_mode else dir_mode
    course_filter:dict
    dir_depth:int
    now_certificated_credit_name:list

    def __init__(self, name:String, max:int, min:int, is_frame:boolean, parent_depth:int):
        self.name = name
        self.max_certificated_credit_num = max
        self.now_certificated_credit_num = 0
        self.feature_certificated_credit_num = 0
        self.min_certificated_credit_num = min
        self.is_frame = is_frame
        self.course_filter = {}
        self.dir_depth = parent_depth
        self.now_certificated_credit_name = []
        
    def get_indent(self):
        return (self.dir_depth - 1)*1

    def print_son(self):
        if(self.now_certificated_credit_num >= self.min_certificated_credit_num):
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{}".format(OK_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, OK_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR))
        else:
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{}".format(FAIL_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, FAIL_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR))
        for item in self.course_filter.values():
            if item.is_frame:
                item.print_son()
            else:
                item.print_ls()

    def namelist(self):
        return ' '.join(self.now_certificated_credit_name)

    def print_ls(self):
        if(self.now_certificated_credit_num >= self.min_certificated_credit_num):
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{} {}".format(OK_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, OK_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR, self.namelist()))
        else:
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{} {}".format(FAIL_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, FAIL_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR, self.namelist()))

    def check(self, ls) -> int:
        self.now_certificated_credit_num = 0
        if self.is_frame: # 下を見に行く
            for item in self.course_filter.values():
                res = item.check(ls)
                self.now_certificated_credit_num += res[0]
                self.feature_certificated_credit_num += res[1]
        else: # RecoFil について
            for item in self.course_filter.values():
                res = item.checkCourse(ls)
                self.now_certificated_credit_num += res[0]
                if not res[1] == "":
                    self.now_certificated_credit_name += res[1]
                    self.feature_certificated_credit_num += res[2]
        return self.now_certificated_credit_num, self.feature_certificated_credit_num

    def add(self, item):
        self.course_filter[item.name] = item

class RecognizedFilter():
    name:str
    regexp_number:str
    regexp_name:str
    def __init__(self, name, num, regname) -> None:
        self.name = name
        self.regexp_number = num
        self.regexp_name = regname
    
    def checkCourse(self, ls):
        res_credit = 0
        feature_credit = 0
        res_course_name = []
        for kamoku in ls:
            flag = False
            if not self.regexp_number == r"" and re.compile(self.regexp_number).match(kamoku.course_number):
                flag = True
            if not self.regexp_name == r"" and re.compile(self.regexp_name).match(kamoku.course_name):
                flag = True
            if flag:
                if not kamoku.used:
                    if kamoku.can_use:
                        kamoku.used = True
                        res_credit += kamoku.credit
                        res_course_name.append("{}{}{}".format(Color.GREEN, kamoku.course_name, Color.RESET))
                    elif kamoku.grade == "履修中":
                        kamoku.used = True
                        feature_credit += kamoku.credit
                        res_course_name.append("{}{}{}".format(FEATURE_COLOR_STR, kamoku.course_name, Color.RESET))
                    else:
                        res_course_name.append("{}{}{}".format(Color.RED, kamoku.course_name, Color.RESET))
        return res_credit, res_course_name, feature_credit
    
    def print_son(self, depth):
        print("{}{}".format("   "*(depth - 1),self.name))


class Level5(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, False, 5)

class Level4(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 4)

class Level3(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 3)

class Level2(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 2)

class Level1(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 1)

def parseJSON(CSVFILENAME) -> Level1:
    with open(CSVFILENAME, 'r') as f:
        data = json.load(f)
    MAX_STR = "max_certificated_credit_num"
    MIN_STR = "min_certificated_credit_num"
    for k1, v1 in data.items():
        all = Level1(k1, v1[MAX_STR], v1[MIN_STR])
        for k2, v2 in v1["leaf"].items():
            all.add(Level2(k2, v2[MAX_STR], v2[MIN_STR]))
            for k3, v3 in v2["leaf"].items():
                all.course_filter[k2].add(Level3(k3, v3[MAX_STR], v3[MIN_STR]))
                for k4, v4 in v3["leaf"].items():
                    all.course_filter[k2].course_filter[k3].add(Level4(k4, v4[MAX_STR], v4[MIN_STR]))
                    for k5, v5 in v4["leaf"].items():
                        all.course_filter[k2].course_filter[k3].course_filter[k4].add(Level5(k5, v5[MAX_STR], v5[MIN_STR]))
                        all.course_filter[k2].course_filter[k3].course_filter[k4].course_filter[k5].add(RecognizedFilter(k5,v5["leaf"]["regexp_number"],v5["leaf"]["regexp_name"]))
    
    return all


class kamokuClass():
    course_number = ""
    course_name = ""
    credit = 0.0
    grade = ""
    used = False
    can_use = False
    isCount = False

    def __init__(self, all) -> None:
        self.course_number = all[2]
        self.course_name = all[3]
        self.credit = float(all[4])
        self.grade = all[7]
        self.can_use = self.grade == "P" or self.grade == "A+" or self.grade == "A" or self.grade == "B" or self.grade == "C" or self.grade == "認"
        self.used = False
        self.isCount = "C0" != all[8]


    def print(self):
        if self.can_use:
            if self.used:
                print('{}{}:{}{}'.format(Color.BLUE,self.course_number,self.course_name,Color.RESET))
            else:
                print('{}{}:{}{}'.format(Color.GREEN,self.course_number,self.course_name,Color.RESET))
        else:
            print('{}{}:{}{}'.format(Color.RED,self.course_number,self.course_name,Color.RESET))

def gp(ls:[]):
    gps = 0.0
    credit_sum = 0.0
    for kam in ls:
        if kam.can_use and kam.isCount:
            if kam.grade == "A+":
                gps += 4.3*kam.credit
                credit_sum += kam.credit
            if kam.grade == "A":
                gps += 4*kam.credit
                credit_sum += kam.credit
            if kam.grade == "B":
                gps += 3*kam.credit
                credit_sum += kam.credit
            if kam.grade == "C":
                gps += 2*kam.credit
                credit_sum += kam.credit
            if kam.grade == "D":
                credit_sum += kam.credit
    
    print("GPA = GPS/CreditSum : {:1.5} = {}/{}".format(gps/credit_sum, gps, credit_sum))



def readCSV(CSVFILENAME):
    
    memo = []
    with open(CSVFILENAME) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i!=0:
                memo.append(kamokuClass(row))


    for t in memo:
        if t.course_name == "オートマトンと形式言語" and t.course_number == "GB21601":
            t.course_number = "GB20401"
        if t.course_name == "プログラム理論" and t.course_number == "GB21111":
            t.course_number = "GB20501"
        if t.course_name == "プログラミングチャレンジ" and t.course_number == "GB21802":
            t.course_number = "GB20602"
        if t.course_name == "プログラム言語処理" and t.course_number == "GB31301":
            t.course_number = "GB30504"
        if t.course_name == "ソフトウェア工学" and t.course_number == "GB31501":
            t.course_number = "GB30601"
        if t.course_name == "情報理論" and t.course_number == "GB12501":
            t.course_number = "GB40601"
    
    return memo


def readNameFromCSV(CSVFILENAME):
    
    memo = []
    with open(CSVFILENAME) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i!=0:
                return row[1]
        # return reader[1][1]

def main():
    parser = argparse.ArgumentParser(description='This program is check that your credit can meet the graduation requirements.')
    parser.add_argument('-i', '--input', help="target file from twins (UTF-8, CSV)", default="sample.csv")
    parser.add_argument('-r', '--requirements', help="requirements file", default="coins20.json")
    args = parser.parse_args()
    
    CSVFILENAME = args.input
    JSONFILENAME = args.requirements

    coins20 = parseJSON(JSONFILENAME)
    print("-"*100,"\n",CSVFILENAME, readNameFromCSV(CSVFILENAME))
    kamoku = readCSV(CSVFILENAME)
    coins20.check(kamoku)
    coins20.print_son()
    gp(kamoku)
    

if __name__ == '__main__':
    main()