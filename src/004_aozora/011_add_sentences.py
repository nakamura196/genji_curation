import requests
from bs4 import BeautifulSoup
import re
import glob

def getId(index, count):
    return "YG"+str(index).zfill(2)+str(count * 100).zfill(8)

def getReplacedSum(sum):
    return sum.replace("<lb></lb>", "").replace("<lb/>", "").strip()

def aaa(text, all, sum, count, div_flg):
    # print("***********", text)
    if "。" in text or div_flg:
        texts = text.split("。")

        for i in range(len(texts)):

            # 最後だけ
            if i == len(texts) - 1: # and not div_flg:
                sum += texts[i]

                '''
                if div_flg:

                    all += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
                    count += 1

                    sum = ""
                '''

            else:

                sum += texts[i] + "。"
                all += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
                count += 1

                sum = ""

    else:

        sum += str(text)

    return all, sum, count

def exec2element(parent, all, count):

    sum = ""

    # 子要素の取得
    children = parent.contents

    all2 = ""

    for i in range(len(children)):
        # print(i+1, len(children))
        child = children[i]
        # print(child)

        text = str(child)

        # この中でも改行がありうる
        if "div" in str(child):

            if getReplacedSum(sum) != "":
                # ここまでのところを一旦保存
                all2 += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
                count += 1

            else:
                # 追加
                all2 += sum

            sum = ""

            '''
            print(child)
            all2 += "<s xml:id='"+getId(index, count)+"'>"+str(child)+"</s>"
            count += 1
            '''

        else:
            if "。" in text:
                texts = text.split("。")

                for i in range(len(texts)):

                    # 最後だけ
                    if i == len(texts) - 1:
                        sum += texts[i]
                    else:

                        sum += texts[i] + "。"
                        all2 += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
                        count += 1

                        sum = ""
                        # sum += texts[i]
            else:
                sum += str(text)

    # ここまでのところを一旦保存
    sum2 = sum.replace("<lb/>", "").strip()

    if len(sum2) > 0:
        all2 += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
        count += 1

    new_element = BeautifulSoup(all2, "html.parser")

    parent.string = ""
    parent.append(new_element)

    return parent, count

files = glob.glob("data/xml/*.xml")

files = sorted(files)

for n in range(len(files)):

    index = n + 1

    print(index, len(files))

    file = files[n]

    ###############

    count = 1

    all = ""

    sum = ""

    soup = BeautifulSoup(open(file,'r'), "lxml-xml")

    main_text = soup.find(rend="main_text")

    children = main_text.contents # .findChildren(text=True)

    for i in range(len(children)):
        # print(i+1, len(children))
        child = children[i]
        # print(child)

        text = str(child)

        # この中でも改行がありうる
        if "div" in str(child):

            # 前の合計テキストが存在する場合は<s>付きでallに追加
            if getReplacedSum(sum) != "":
                # ここまでのところを一旦保存
                all += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
                count += 1
            # 前の合計テキストが存在するが、<lb/>のみの場合などは<s>なしでallに追加
            else:
                # 追加
                all += sum

            # 上記のいずれの場合でも一旦合計テキストは初期化
            sum = ""

            
            
            new_element, count = exec2element(child, all, count)
            all += str(new_element)


        else:

            if "。" in text:
                texts = text.split("。")

                for i in range(len(texts)):

                    # 最後だけ
                    if i == len(texts) - 1:
                        sum += texts[i]
                    else:

                        sum += texts[i] + "。"
                        all += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
                        count += 1

                        sum = ""
            else:

                sum += str(text)

    soup.find(rend="main_text").replace_with(BeautifulSoup(all, "html.parser"))

    f = open(file.replace("/xml/", "/xml_s/"), "w")
    f.write(soup.prettify())
    f.close()

    