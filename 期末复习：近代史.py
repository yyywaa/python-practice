import os
os.system('pip install pandas')
os.system('pip install xlrd')
import pandas as pd
path_raw=r'C:\Users\86188\Desktop\大一期末\大一上\大一上\近代史\长沙理工大学近代史题库.xls长沙理工大学近代史题库(1) (1) (1).xls'
Path=os.path.join(path_raw)
df=pd.read_excel(Path,header = 0)
#只有question_index为题号！
mistake_index=[]
def get_q(question_index):
    index=question_index - 1
    question=df['题目'].tolist()[index]
    return question
def get_options(question_index):
    index=question_index - 1
    a=df['选项\nA'].tolist()[index]
    b=df['选项\nB'].tolist()[index]
    c=df['选项\nC'].tolist()[index]
    d=df['选项\nD'].tolist()[index]
    options=f'A.{a}\nB.{b}\nC.{c}\nD.{d}'
    return options
def get_answers(question_index):
    index=question_index - 1
    answer=df['答案 '].tolist()[index]
    return answer
def mistake_record(question_index,check_value):
    index=question_index - 1
    if check_value:
        mistake_index.append(index)

def run_learning():
    start_index = int(input('请输入上次结束的题号：')) + 1
    task_quantity=int(input('本次计划题量为：'))
    print('正在为您调用题库：')
    for index in range(start_index, start_index + task_quantity):
        print(f'本题为第{index}题！')
        print(get_q(index))
        print(get_options(index))
        user_answer=input('请输入答案：(若想进入错题模式，请以‘答案 m’形式输入)')
        check=user_answer==get_answers(index)
        if not check:
            if 'm' in user_answer:
                print(f'本题答案为{get_q(index)}')
                mistake_record(index,check)
                break


            else:
                print(f'答案错误，正确答案为{get_answers(index)}')
                mistake_record(index,check)
                print('已将本题加入错题本！')
        else:
            print('答案正确！')
    print('恭喜，您已完成任务！')
    print('即将为您开启错题模式！')
    run_mistaking()
def run_mistaking():
    print('已开启错题模式！')
    for index in mistake_index:
        print(f'本题为第{index}题！')
        print(get_q(index))
        print(get_options(index))
        user_answer = input('请输入答案：')
        check = user_answer == get_answers(index)
        if check:
            print('回答正确')
            continue
        else:
            print(f'答案错误，正确答案为{get_answers(index)}')
            print('本程序不记录该错题，请记下运行记录中的题号')

    print('恭喜，您已完成所有错题')

mode=input('请选择模式：学习模式【learning】 or 错题模式【mistaking】')
if mode=='learning':
    run_learning()
if mode=='mistaking':
    run_mistaking()

print('感谢使用本程序，祝您期末顺利！')
print('制作者：yyy/Cloudra')


