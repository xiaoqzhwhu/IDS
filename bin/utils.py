import json
import re

# 加载大V
def load_seeds_from_uid(round, static_data, product):
    seed_set = []
    for i in range(round+1):
        filename = "./t100/%s_r%s_uid.txt" % (product, i)
        for line in open(filename, "r", encoding="utf-8"):
            line = line.strip("\n")
            fields = line.split("\t")
            if len(fields) > 0:
                if str(fields[0]) not in seed_set and static_data[fields[0]]["user_followers"] > 100000:
                    seed_set.append(str(fields[0]))
        # print(len(seed_set))
    return set(seed_set)

# 加载静态信息：用户ID，静态profile
def load_static_profile(static_file):
    with open(static_file, 'r', encoding='utf-8') as file:
        static_data = json.load(file)
    return static_data

# 加载动态信息：用户ID，历史评论等
def load_dynamic_profile(dynamic_file):
    with open(dynamic_file, 'r', encoding='utf-8') as file:
        dynamic_data = json.load(file)
    return dynamic_data

def remove_angle_brackets(input_string):
    # 使用正则表达式匹配尖括号内的内容
    pattern = re.compile(r'<.*?>')
    # 使用 sub 方法将匹配到的内容替换为空字符串
    result = re.sub(pattern, '', input_string)
    # if len(result.strip()) == 0:
    #     result = input_string
    return result


def remove_mentions(text):
    # 构建正则表达式模式，匹配提及格式，例如@某人
    mention_pattern = re.compile(r'回复@(\w+):')
    # 对文本进行替换
    modified_text = mention_pattern.sub('', text)
    mention_pattern = re.compile(r'回复@(\w+)：')
    # 对文本进行替换
    modified_text = mention_pattern.sub('', modified_text)
    # 如果需要同时去除多个不同的人，可以将所有人的用户名用|分隔在正则表达式中
    # 例如: mention_pattern = re.compile(r'@(user1|user2|user3)')
    return modified_text
