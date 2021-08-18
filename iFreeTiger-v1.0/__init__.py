from flask import Flask, render_template, request
from flask import send_from_directory

import random
import string
import xlrd
import xlwt
import time
import jionlp

from model_res1 import single
from model_res2 import single2
from model_res3 import single3

import ckpe

app = Flask(__name__)


@app.route('/')  # 后台管理，默认只支持GET请求
def index():
    return render_template('index.html')


# 单条新闻分类处理
@app.route('/predict', methods=['GET', 'POST'])
def predict():

    time_start = time.time()

    if request.method == "POST":
        new_content = request.form.get('news')
        new_content = new_content.replace('\n', '')
        text = jionlp.clean_text(new_content)

        if len(new_content) <= 64:
            model_time, run_time, possible_list = single2.main(text)
            title = ''

        elif 64 < len(new_content) <= 200:
            ckpe_obj = ckpe.ckpe()
            key_phrases = ckpe_obj.extract_keyphrase(text)
            title = ','.join(key_phrases)

            model_time, run_time, possible_list = single.main(title)
            model_time, run_time, possible_list2 = single2.main(title)
            model_time, run_time, possible_list3 = single3.main(title)

            if possible_list == possible_list2:
                possible_list = possible_list
            elif possible_list == possible_list3:
                possible_list = possible_list
            elif possible_list2 == possible_list3:
                possible_list = possible_list2
            else:
                possible_list = possible_list2

        else:
            res = jionlp.summary.extract_summary(text)

            ckpe_obj = ckpe.ckpe()
            key_phrases = ckpe_obj.extract_keyphrase(res)
            title = ','.join(key_phrases)

            model_time, run_time, possible_list = single.main(title)
            model_time, run_time, possible_list2 = single2.main(title)
            model_time, run_time, possible_list3 = single3.main(title)

            if possible_list == possible_list2:
                possible_list = possible_list
            elif possible_list == possible_list3:
                possible_list = possible_list
            elif possible_list2 == possible_list3:
                possible_list = possible_list2
            else:
                possible_list = possible_list2


        time_end = time.time()
        time_c = time_end - time_start
        time_total = str(time_c)

        return render_template('index2.html',
                               possible_list=possible_list[0],
                               time_total=time_total[0:7],
                               new_content=new_content,
                               title=title)

    return render_template('index.html')


ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
save_path = ("".join("static/download/" + ran_str + '.xls'))


@app.route('/batch.html')
def batch():
    time_start = time.time()
    new_num = 2000
    dic_item = {
        '财经': 335,
        '房产': 210,
        '科技': 234,
        '军事': 175,
        '体育': 120,
        '教育': 186,
        '汽车': 178,
        '娱乐': 202,
        '游戏': 235,
        '其他': 125
    }
    time_end = time.time()
    time_cc = time_end - time_start
    str1 = str(time_cc)
    return render_template('batch.html',
                           time_cc=str1[0:7],
                           dic_item=dic_item,
                           new_num=new_num,
                           num1=dic_item['财经'],
                           num2=dic_item['房产'],
                           num3=dic_item['教育'],
                           num4=dic_item['科技'],
                           num5=dic_item['军事'],
                           num6=dic_item['汽车'],
                           num7=dic_item['体育'],
                           num8=dic_item['游戏'],
                           num9=dic_item['娱乐'],
                           num10=dic_item['其他'])


# 文件上传的处理
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    time_start = time.time()
    if request.method == 'POST':
        file = request.files['file']
        # print(file.filename)  # 打印文件名

        f = file.read()  # 文件内容
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        list0 = table.col_values(0)
        list2 = table.col_values(2)
        list3 = table.col_values(3)

        list1 = []

        new_num = table.nrows - 1

        for i in range(1, table.nrows):
            list3[i] = list3[i].replace('\n', '')
            text = jionlp.clean_text(list3[i])

            res = jionlp.summary.extract_summary(text)

            ckpe_obj = ckpe.ckpe()
            key_phrases = ckpe_obj.extract_keyphrase(res)
            title = ','.join(key_phrases)

            model_time, run_time, possible_list = single.main(title)
            model_time, run_time, possible_list2 = single2.main(title)
            model_time, run_time, possible_list3 = single3.main(title)

            if possible_list == possible_list2:
                possible_list = possible_list
            elif possible_list == possible_list3:
                possible_list = possible_list
            elif possible_list2 == possible_list3:
                possible_list = possible_list2
            else:
                possible_list = possible_list2
            list1.append(possible_list[0])

        dic_item = {}

        for i in list1:
            if i not in dic_item:
                dic_item[i] = 1
            else:
                dic_item[i] += 1

        dic = {
            '财经': 0,
            '房产': 0,
            '教育': 0,
            '科技': 0,
            '军事': 0,
            '汽车': 0,
            '体育': 0,
            '游戏': 0,
            '娱乐': 0,
            '其他': 0}

        for i in list1:
            if i not in dic_item:
                dic[i] = 1
            else:
                dic[i] += 1

        book = xlwt.Workbook(encoding="utf-8", style_compression=0)
        sheet = book.add_sheet('pre_result', cell_overwrite_ok=True)

        row0 = ["编号", "new_category", "title", "content"]
        for i in range(0, len(row0)):
            sheet.write(0, i, row0[i])

        for i in range(1, table.nrows):

            sheet.write(i, 0, list0[i])
            sheet.write(i, 1, list1[i - 1])
            sheet.write(i, 2, list2[i])
            sheet.write(i, 3, list3[i])

        book.save(save_path)

        news_list1 = []
        news_list2 = []
        news_list3 = []
        news_list4 = []
        news_list5 = []
        news_list6 = []
        news_list7 = []
        news_list8 = []
        news_list9 = []
        news_list10 = []

        for i in range(0, table.nrows - 1):
            if list1[i] == '财经':
                list2[i + 1] = list2[i + 1].replace('\n','')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list1.append(list2[i + 1])
            if list1[i] == '房产':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list2.append(list2[i + 1])
            if list1[i] == '科技':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list3.append(list2[i + 1])
            if list1[i] == '军事':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list4.append(list2[i + 1])
            if list1[i] == '体育':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list5.append(list2[i + 1])
            if list1[i] == '教育':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list6.append(list2[i + 1])
            if list1[i] == '汽车':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list7.append(list2[i + 1])
            if list1[i] == '娱乐':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list8.append(list2[i + 1])
            if list1[i] == '游戏':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list9.append(list2[i + 1])
            if list1[i] == '其他':
                list2[i + 1] = list2[i + 1].replace('\n', '')
                list2[i + 1] = list2[i + 1].replace('\r', '')
                news_list10.append(list2[i + 1])


        time_end = time.time()
        time_cc = time_end - time_start
        str2 = str(time_cc)

        return render_template('batch.html',
                               time_cc=str2[0:7],
                               dic_item=dic_item,
                               new_num=new_num,
                               num1=dic['财经'],
                               num2=dic['房产'],
                               num3=dic['教育'],
                               num4=dic['科技'],
                               num5=dic['军事'],
                               num6=dic['汽车'],
                               num7=dic['体育'],
                               num8=dic['游戏'],
                               num9=dic['娱乐'],
                               num10=dic['其他'],
                               news_list1=news_list1[0:12],
                               news_list2=news_list2[0:12],
                               news_list3=news_list3[0:12],
                               news_list4=news_list4[0:12],
                               news_list5=news_list5[0:12],
                               news_list6=news_list6[0:12],
                               news_list7=news_list7[0:12],
                               news_list8=news_list8[0:12],
                               news_list9=news_list9[0:12],
                               news_list10=news_list10[0:12])

    return render_template('batch.html')


@app.route('/download')
def download():
    return send_from_directory(
        "static/download",
        "".join(
            ran_str + '.xls'),
        as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
