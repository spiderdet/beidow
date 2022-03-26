#学习怎么用xpinyin或pypinyin OK
#把所有成语中出现过的字和对应的注音存到word_dict.txt NO
#重点搞定judge函数，并完成单元测试 OK
#写好game_simulation流程框架 OK
#鱼yu晕yun轮lun的问题   OK
#提示系统
#速查表系统
#UI
#处理一不、33=23等转调风格
#贝使用自定义拼音风格
# ü
from pypinyin import pinyin, Style,lazy_pinyin
import re
import random
import datetime


def game_simulation(seed=0,trys=10):
    word_len = 4
    with open("chengyu2231.txt",'r',encoding='utf-8') as f:
        chengyu_list = f.read().rstrip('\n').splitlines()
    if seed != 0:
        random.seed(seed)
    chosen_word = chengyu_list[random.randrange(len(chengyu_list))]
    # print(chosen_word)
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    with open("answer.txt",'a', encoding='utf-8') as f:
        f.write(now+" ")
        f.write(chosen_word+"\n")
    for i in range(1, trys+1):
        while True:
            trying = input("{0}'th trying:".format(i))
            if valid(trying, word_len):
                break
            else:
                print("invalid chengyu, please try again~")
        hanzi,tone,word_notone,shengmu,yunmu,word_notone2,tone2,shengmu2,yunmu2 = judge(chosen_word, trying)
        print_result(trying,hanzi,tone,word_notone,shengmu,yunmu,word_notone2,tone2,shengmu2,yunmu2)
        if 0 not in hanzi and 1 not in hanzi:
            if i <= 4:
                print("congratulations! you are \033[33;1mso \033[34;1mso \033[32;1mso \033[35;1mSMART!\033[0m loving you~ Try times =", i)
            else:
                print("congratulations! you have won! \033[35;1mloving U,贝\033[0m. Try times =", i)
            return
    print("You have used out your chances, True Answer is {0}\n"
          " please start another game~".format(chosen_word))

def valid(try_word, word_len):
    try_word = try_word.strip()
    if len(try_word) != word_len:
        print("Not right length!")
        return False
    for i in try_word:
        if ord(i)<127:
            print("Only Chinese please!")
            return False
    return True
def get_pinyin(word): # 输出单字、普通成语、特殊成语的注音，特殊成语会自动识别
    # for i in word:
    s = ''
    # heteronym=True开启多音字
    for i in pinyin(word, heteronym=False,style=Style.TONE3): #
        print("i: ",i)
        s = s + ''.join(i) + " "
    print("s: ",s)
    return s
def get_lazy_pinyin(word):
    result = lazy_pinyin(word,style=Style.TONE3,v_to_u=True,tone_sandhi=True,neutral_tone_with_five=True)
    # print(result)
    tone,word_notone,shengmu_list,yunmu_list =[],[],[],[]
    for idx,i in enumerate(result):
        if i[-1].isdigit():
            tone.append(str((int(i[-1])-1)%4+1))
            i_notone = i[:-1]
        else:
            print("\033[31;1mError, word {0} {1} didn't have tone\033[0m".format(word[idx],i))
            i_notone = i
        shengmu = re.match('sh|ch|zh|[bpmfdtnlgkhjqxrzcsyw]',i_notone)
        if shengmu is None:
            shengmu_list.append(shengmu) # shengmu = None
            shengmu = ''
            # print("\033[32;1mMind, word {0} {1} didn't have shengmu\033[0m".format(word[idx],i))
            yunmu = i_notone
            yunmu_list.append(yunmu)
        else:
            shengmu = shengmu.group()
            shengmu_list.append(shengmu)
            yunmu = re.sub('sh|ch|zh|[bpmfdtnlgkhjqxrzcsyw]', '', i_notone, 1)
            if yunmu in ['u','un','ue','uan'] and shengmu in ['j','q','x','y']:
                yunmu = re.sub('u','ü',yunmu)
                # print("\033[33;1mMind, word {0} {1} from u->ü, {2}\033[0m".format(word[idx], i,yunmu))
            yunmu_list.append(yunmu)
        if len(yunmu) == 0:
            print("\033[31;1mError, word {0} {1} didn't have yunmu\033[0m".format(word[idx],i))

        word_notone.append(shengmu+yunmu)
    # print("tone: ",tone)
    # print("word_notone: ",word_notone)
    # print("shengmu: ",shengmu_list)
    # print("yunmu: ",yunmu_list)
    #再加上自定义转调规则
    return tone,word_notone,shengmu_list,yunmu_list
def get_initial_final(word):
    for i in pinyin(word, style=Style.INITIALS):
        print("initials :",i)
    for i in pinyin(word, style=Style.FINALS):
        print("finals: ",i)
def get_initial_final_Notstrict(word):
    for i in pinyin(word, strict=False,style=Style.INITIALS):
        print("initials :",i)
    for i in pinyin(word, strict=False,style=Style.FINALS):
        print("finals: ",i)
def get_initial_final_practical(word):
    for i in pinyin(word, strict=False,style=Style.INITIALS):
        print("initials :",i)
    for i in pinyin(word, strict=True,v_to_u=True,style=Style.FINALS):
        print("finals: ",i)
def judge(ans_word,try_word): #输出整体注音、声母、韵母、音调、汉字所有的正确性
    hanzi = judge_unit(ans_word,try_word)
    tone1,word_notone1, shengmu1, yunmu1 = get_lazy_pinyin(ans_word)
    tone2,word_notone2, shengmu2, yunmu2 = get_lazy_pinyin(try_word)
    tone = judge_unit(tone1,tone2)
    word_notone = judge_unit(word_notone1,word_notone2)
    shengmu = judge_unit(shengmu1,shengmu2)
    yunmu = judge_unit(yunmu1, yunmu2)
    # print(hanzi,tone,word_notone,shengmu,yunmu)
    return hanzi,tone,word_notone,shengmu,yunmu,word_notone2,tone2,shengmu2,yunmu2

def judge_unit(ans_array, try_array):
    #用dict记录，字母位置都正确之后，去掉dict中的次数，再匹配只有字母正确的
    ans_dict = {}
    for letter in ans_array:
        if letter is None:
            continue
        elif letter in ans_dict.keys():
            ans_dict[letter]+=1
        else:
            ans_dict[letter]=1
    # print(ans_dict)
    result = []
    length = len(ans_array)
    for idx in range(length):
        if try_array[idx] is None:# when both are None
            result.append(0)
        elif ans_array[idx] == try_array[idx]:
            result.append(2)
            ans_dict[ans_array[idx]]-=1
        else:
            result.append(0)
    for idx in range(length):
        if result[idx]==2:
            continue
        elif try_array[idx] in ans_dict.keys() and ans_dict[try_array[idx]]>0:
            result[idx] = 1
            ans_dict[try_array[idx]]-=1
    # print("the comparison of {0} and {1} is {2}".format(ans_array,try_array,result))
    return result

def print_result(trying,hanzi,tone,word_notone,shengmu,yunmu,word_notone2,tone2,shengmu2,yunmu2):#两行，第一行注音，第二行文字
    num = len(trying)
    all_hanzi_string,all_pinyin_string = "",""
    for idx in range(num):
        #如果整体完全对，就整体绿
        #如果整体对了但位置不对，就整体蓝，除非其中有绿色的声母或韵母，换句话说绿+蓝或者蓝+绿，所以和声母是否为None无关
        #如果整体不对，就按普通的声母+韵母。
        pinyin_string = ""
        if shengmu2[idx] is None:
            shengmu2[idx] = ''
        if word_notone[idx] == 2:
            pinyin_string = pinyin_string+"\033[32;1m{0}\033[0m".format(word_notone2[idx])
        elif word_notone[idx] == 1:
            if shengmu[idx] == 2:
                pinyin_string = pinyin_string + "\033[32;1m{0}\033[34;1m{1}\033[0m".format(shengmu2[idx],yunmu2[idx])
            elif yunmu[idx] == 2:
                pinyin_string = pinyin_string + "\033[34;1m{0}\033[32;1m{1}\033[0m".format(shengmu2[idx],yunmu2[idx])
            else:
                pinyin_string = pinyin_string + "\033[34;1m{0}\033[0m".format(word_notone2[idx])
        else:
            if shengmu[idx] == 2:
                pinyin_string = pinyin_string + "\033[32;1m{0}\033[0m".format(shengmu2[idx])
            elif shengmu[idx] == 1:
                pinyin_string = pinyin_string + "\033[33;1m{0}\033[0m".format(shengmu2[idx])
            else:
                pinyin_string = pinyin_string + "{0}".format(shengmu2[idx])
            if yunmu[idx] == 2:
                pinyin_string = pinyin_string + "\033[32;1m{0}\033[0m".format(yunmu2[idx])
            elif yunmu[idx] == 1:
                pinyin_string = pinyin_string + "\033[33;1m{0}\033[0m".format(yunmu2[idx])
            else:
                pinyin_string = pinyin_string + "{0}".format(yunmu2[idx])

        if tone[idx] == 2:
            pinyin_string = pinyin_string+"\033[32;1m{0}\033[0m".format(tone2[idx])
        elif hanzi[idx] == 1:
            pinyin_string=pinyin_string+"\033[33;1m{0}\033[0m".format(tone2[idx])
        else:
            pinyin_string=pinyin_string+"{0}".format(tone2[idx])
        pinyin_string = my_align(pinyin_string,8)
        # print(pinyin_string)
        all_pinyin_string += pinyin_string
    print(all_pinyin_string)
    for idx in range(num):
        hanzi_string = ""
        if hanzi[idx] == 2:
            hanzi_string = hanzi_string+"\033[30;42;1m{0}\033[0m".format(trying[idx])
        elif hanzi[idx] == 1:
            hanzi_string=hanzi_string+"\033[30;43;1m{0}\033[0m".format(trying[idx])
        else:
            hanzi_string=hanzi_string+"\033[37;40;1m{0}\033[0m".format(trying[idx])
        hanzi_string = my_align(hanzi_string,8)
        # print(hanzi_string)
        all_hanzi_string +=hanzi_string
    print(all_hanzi_string)

def test_print_result(chosen_word, trying):
    hanzi, tone, word_notone, shengmu, yunmu, word_notone2, tone2,shengmu2,yunmu2 = judge(chosen_word, trying)
    print_result(trying, hanzi, tone, word_notone, shengmu, yunmu, word_notone2, tone2,shengmu2,yunmu2)

def my_align(string, length=0, align_type='-'):
    """
    be careful that len("\tA\n") will get 3 ; and len("\033[31;1mA\033[0m")
    will get 12
    By the way, the length of output "中国人" is smaller than "AABBCC",which means
    a chinese character counted as 2 letters is not really True. After my trial,
    roughly 1:1.67
    :param string: 中英文混排时待列对齐的原字符串
    :param length: 待预留列宽,折合的半角字符总数,默认0
    :param align_type: 对齐类型,默认左对齐.左对齐<,右对齐>,居中对齐-
    :return: 补充空格后的字符串
    """
    #用re找到所有彩色输出的地方，并用raw_str保存去除彩色输出命令的string部分，用来计算补充空格数，然后相同
    # print(len(string))
    # print(string)
    raw_str = re.sub('\\033\[.+?m','',string)
    # raw_str = re.sub(r'\033\[.+?m','',string) #这样和上面等价
    # print(len(raw_str))
    # print(raw_str)
    len_raw = len(raw_str)
    if length <= len_raw:
        return string
    len_ch = (len(raw_str.encode('gbk')) - len(raw_str)) * 2  # 中文折合的半角字符总数
    len_en = len(raw_str) * 2 - len(raw_str.encode('gbk'))    # 英文折合的半角字符总数
    len_sp = length - len_ch - len_en                       # 补充空格总数
    if align_type == '>':    # 右对齐
        return ' ' * len_sp + string
    elif align_type == '-':  # 居中对齐
        return ' ' * int(len_sp / 2) + string + ' ' * (len_sp - int(len_sp / 2))
    return string + ' ' * len_sp  # 左对齐

def test_unit():
    # with open("test.txt",'r',encoding="utf-8") as f:
        # words = f.read().rstrip('\n').splitlines()
    # words2=[""] #"和平乱和" "腰威局女鱼晕轮牛归"
    # print("test.txt has words: ",words2)
    # for word in words2:
        # get_pinyin(word)
        # get_initial_final(word)
        # get_initial_final_Notstrict(word)
        # get_initial_final_practical(word)
    # get_lazy_pinyin("晕轮女路鱼")
    # judge("无哎","爱爱")
    # test_print_result("无长碍","深称爱")
    # valid("哎阿斯顿发",5)
    # game_simulation(326)
    # my_align("\033[31;1ms\033[0mh\033[32;1men\033[33;1mg\033[0m1",8)
    pass
if __name__ == '__main__':
    # test_unit()
    game_simulation()