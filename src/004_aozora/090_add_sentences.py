import requests
from bs4 import BeautifulSoup
import re

def getId(index, count):
    return "YG"+str(index).zfill(2)+str(count * 100).zfill(8)

#Requestsを使って、webから取得
r = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/tei/yosano/01.xml")
#要素を抽出
soup = BeautifulSoup(r.content, 'lxml-xml')

index = 1

# print(soup)

main_text = soup.find(rend="main_text")

children = main_text.contents # .findChildren(text=True)

all = ""

sum = ""

count = 1

def aaa(text, all, sum, count, div_flg):
    print("***********", text)
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

for i in range(len(children)):
    # print(i+1, len(children))
    child = children[i]
    # print(child)

    text = str(child)

    # この中でも改行がありうる
    if "div" in str(child):



        sum2 = sum.replace("<lb/>", "").strip()

        if len(sum2) > 0:

            print("*********", sum)

            # ここまでのところを一旦保存
            all += "<s xml:id='"+getId(index, count)+"'>"+sum+"</s>"
            count += 1

        else:

            

            # 追加
            all += sum

        sum = ""

        # all, sum, count = aaa(str(child), all, sum, count, True)

        print("*********", child)

        

        # print(child)
        all += "<s xml:id='"+getId(index, count)+"'>"+str(child)+"</s>"
        count += 1
        



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
                    # sum += texts[i]

                

        else:

            sum += str(text)

# main_text.contents = all
soup.find(rend="main_text").replace_with(BeautifulSoup(all, "html.parser"))

f = open("data/"+str(index).zfill(2)+".xml", "w")
f.write(soup.prettify())
f.close()

index += 1

    