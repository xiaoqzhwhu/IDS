#coding=utf-8

#节点静态信息：用户ID、用户性别、用户地址、用户描述、用户标签、关注数、粉丝数、互动用户总数；
static_graph = {}
#节点动态信息：互动用户列表，互动类型，互动文本详情<原始文本，comment文本>；
dynamic_graph = {}

import json
import random
round = 5
product = "huohuasiwei"
# product = "abc"
product = "alice"
# product = "yunjing"
# product = "cream"
# product = "brush"
product = "suboer"
relation_f = open("t100/%s_r%s_relation.txt" % (product, str(round)), "w+", encoding="utf-8")
user_f = open("t100/%s_r%s_uid.txt" % (product, str(round+1)), "w+", encoding="utf-8")

def load_seeds(round):
    global product
    seed_set = []
    for i in range(round+1):
        filename = "t100/%s_r%s_uid.txt" % (product, i)
        for line in open(filename, "r", encoding="utf-8"):
            line = line.strip("\n")
            fields = line.split("\t")
            if len(fields) > 0:
                if str(fields[0]) not in seed_set:
                    seed_set.append(str(fields[0]))
    return set(seed_set)


def update_graph(comments, static_graph, dynamic_graph):
    for comment in comments:
        #对每条comment，新增用户静态信息和一级互动信息
        comment_text = comment["text"]
        comment_source = ""
        if "source" in comment:
            comment_source = comment["source"]
        comment_id = str(comment["user"]["id"])
        comment_name = comment["user"]["screen_name"]
        comment_region = ""
        if "region_name" in comment:
            comment_region = comment["region_name"]
        comment_description = ""
        if "description" in comment["user"]:
            comment_description = comment["user"]["description"]
        comment_location = ""
        if "location" in comment["user"]:
            comment_location = comment["user"]["location"]
        comment_gender = ""
        if "gender" in comment["user"]:
            comment_gender = comment["user"]["gender"]
        comment_followers = 0
        if "followers_count" in comment["user"]:
            comment_followers = comment["user"]["followers_count"]
        comment_friends = 0
        if "friends_count" in comment["user"]:
            comment_friends = comment["user"]["friends_count"]
        if comment_id not in static_graph:
            # 更新静态表
            item = {}
            item["user_id"] = comment_id
            item["user_name"] = comment_name
            item["user_tag"] = ""
            item["user_source"] = comment_source
            item["user_region"] = comment_region
            item["user_gender"] = comment_gender
            item["user_location"] = comment_location
            item["user_followers"] = comment_followers
            item["user_friends"] = comment_friends
            item["user_description"] = comment_description
            static_graph.setdefault(comment_id, item)
        # 更新动态表
        interactions = []
        if user_id in dynamic_graph:
            interactions = dynamic_graph[user_id]
        action = {}
        action["text_raw"] = text_raw
        action["text_comment"] = comment_text
        action["interact_type"] = interact_type
        action["interact_id"] = comment_id
        interactions.append(action)
        if user_id in dynamic_graph:
            dynamic_graph[user_id] = interactions
        else:
            dynamic_graph.setdefault(user_id, interactions)
        #存在二次交互时，新增用户静态信息和二级互动信息
        inner_comments = []
        if "comments" in comment:
            inner_comments = comment["comments"]
        # print(inner_comments)
        for inner_comment in inner_comments:
            # 对每条comment，新增用户静态信息和一级互动信息
            inner_comment_text = inner_comment["text"]
            inner_comment_source = ""
            if "source" in inner_comment:
                inner_comment_source = inner_comment["source"]
            inner_comment_id = str(inner_comment["user"]["id"])
            inner_comment_name = inner_comment["user"]["screen_name"]
            inner_comment_region = ""
            if "region_name" in inner_comment:
                inner_comment_region = inner_comment["region_name"]
            inner_comment_description = inner_comment["user"]["description"]
            inner_comment_location = inner_comment["user"]["location"]
            inner_comment_gender = inner_comment["user"]["gender"]
            inner_comment_followers = inner_comment["user"]["followers_count"]
            inner_comment_friends = inner_comment["user"]["friends_count"]
            if inner_comment_id not in static_graph:
                # 更新静态表
                item = {}
                item["user_id"] = inner_comment_id
                item["user_name"] = inner_comment_name
                item["user_tag"] = ""
                item["user_source"] = inner_comment_source
                item["user_region"] = inner_comment_region
                item["user_gender"] = inner_comment_gender
                item["user_location"] = inner_comment_location
                item["user_followers"] = inner_comment_followers
                item["user_friends"] = inner_comment_friends
                item["user_description"] = inner_comment_description
                static_graph.setdefault(inner_comment_id, item)
            else:
                item = static_graph[inner_comment_id]
                item["user_gender"] = inner_comment_gender
                item["user_location"] = inner_comment_location
                item["user_followers"] = inner_comment_followers
                item["user_friends"] = inner_comment_friends
                item["user_description"] = inner_comment_description
                static_graph["inner_comment_id"] = item
            # 更新动态表
            interactions = []
            if comment_id in dynamic_graph:
                interactions = dynamic_graph[comment_id]
            action = {}
            action["text_raw"] = comment_text
            action["text_comment"] = inner_comment_text
            action["interact_type"] = interact_type
            action["interact_id"] = inner_comment_id
            interactions.append(action)
            if comment_id in dynamic_graph:
                dynamic_graph[comment_id] = interactions
            else:
                dynamic_graph.setdefault(comment_id, interactions)
    return static_graph, dynamic_graph

seed_set = load_seeds(round)
print(seed_set)

for line in open("t100/%s_r%s.json" % (product, str(round)), "r", encoding="utf-8"):
    line = line.strip("\n")
    try:
        details = json.loads(line)
    except:
        continue
    #新增用户静态信息
    user_id = str(details["user"]["id"])
    # if user_id not in seed_set:
    #     continue
    user_name = details["user"]["screen_name"]
    user_tag = ""
    if "tag_struct" in details:
        user_tag = details["tag_struct"][0]["tag_name"]
    text_raw = details["text_raw"]
    user_source = details["source"]
    user_region = ""
    if "region_name" in details:
        user_region = details["region_name"]
    # 根据评论详情补全
    user_gender = ""
    user_location = ""
    user_followers = 0
    user_friends = 0
    user_description = ""
    if user_id not in static_graph:
        item = {}
        item["user_id"] = user_id
        item["user_name"] = user_name
        item["user_tag"] = ""
        item["user_source"] = user_source
        item["user_region"] = user_region
        item["user_gender"] = user_gender
        item["user_location"] = user_location
        item["user_followers"] = user_followers
        item["user_friends"] = user_friends
        item["user_description"] = user_description
        static_graph.setdefault(user_id, item)
    comments = []
    reposts = []
    interact_type = ""
    if "comments" in details:
        interact_type = "comment"
        comments = details["comments"]
    print(comments)
    static_graph, dynamic_graph = update_graph(comments, static_graph, dynamic_graph)
    if "reposts" in details:
        interact_type = "reposts"
        reposts = details["reposts"]
    #print(reposts)
    static_graph, dynamic_graph = update_graph(reposts, static_graph, dynamic_graph)

print("static_graph")
static_f = open("t100/%s_r%s.static.graph" % (product, round), "w+", encoding="utf-8")
static_f.write(json.dumps(static_graph, ensure_ascii=False, indent=2))
static_f.close()
print("dynamic_graph")
dynamic_f = open("t100/%s_r%s.dynamic.graph" % (product, round), "w+", encoding="utf-8")
dynamic_f.write(json.dumps(dynamic_graph, ensure_ascii=False, indent=2))
dynamic_f.close()
print("用户总数：%s" % len(static_graph))
dynamic_len = 0
for user_id in dynamic_graph:
    dynamic_len += len(dynamic_graph[user_id])
print("互动总数：%s" % dynamic_len)
interact_count_stat = {}
interact_section_stat = {}
seed_overlap_count = 0

print("已抓取用户总数：")
print(len(seed_set))
# seed_set = {"1674427277", "3213060995", "1748332981", "1929045072", "2525724021", "2756008445", "2137896993", "6563221434", "2155183437", "5024091107"}
interact_section_stat[">=100"] = 0
interact_section_stat["50-100"] = 0
interact_section_stat["40-50"] = 0
interact_section_stat["30-40"] = 0
interact_section_stat["20-30"] = 0
interact_section_stat["10-20"] = 0
interact_section_stat["2-10"] = 0
interact_section_stat["==1"] = 0
for user_id in dynamic_graph:
    interact_set = set([str(item["interact_id"]) for item in dynamic_graph[user_id]])
    # print(interact_set)
    overlap_set = interact_set & seed_set
    if len(overlap_set) >= 2:
        print(user_id)
        print(overlap_set)
        seed_overlap_count += 1
    interact_count = len(dynamic_graph[user_id])
    if str(interact_count) in interact_count_stat:
        interact_count_stat[str(interact_count)] += 1
    else:
        interact_count_stat.setdefault(str(interact_count), 1)
    if interact_count >= 100:
        interact_section_stat[">=100"] += 1
    elif interact_count >= 50 and interact_count < 100:
        interact_section_stat["50-100"] += 1
    elif interact_count >= 40 and interact_count < 50:
        interact_section_stat["40-50"] += 1
    elif interact_count >= 30 and interact_count < 40:
        interact_section_stat["30-40"] += 1
    elif interact_count >= 20 and interact_count < 30:
        interact_section_stat["20-30"] += 1
    elif interact_count >= 10 and interact_count < 20:
        interact_section_stat["10-20"] += 1
    elif interact_count >= 2 and interact_count < 10:
        interact_section_stat["2-10"] += 1
    else:
        interact_section_stat["==1"] += 1
print("用户交互统计：")
print(json.dumps(interact_count_stat, indent=2))
print("用户交互分段统计：")
print(json.dumps(interact_section_stat, indent=2))
print("和种子用户存在overlap用户数统计：%s" % seed_overlap_count)
#输出留存用户
relation_dict = {}
for user_id in dynamic_graph:
    # if len(dynamic_graph[user_id]) > 50 and str(user_id) not in seed_set and static_graph[user_id]['user_followers'] > 0:
    if (len(dynamic_graph[user_id]) >= 100 and static_graph[user_id]['user_followers'] > 0) or \
            (static_graph[user_id]['user_followers'] > 100000 and len(dynamic_graph[user_id]) >= 10):
        if str(user_id) not in seed_set:
            # user_f.write("%s\n" % user_id)
            user_f.write("%s\t%s:%s:%s:%s\n" % (user_id, static_graph[user_id]['user_name'], static_graph[user_id]['user_followers'], static_graph[user_id]['user_friends'], len(dynamic_graph[user_id])))
        # 输出节点和边
        out_flag = 1
        for item in dynamic_graph[user_id]:
            # if len(dynamic_graph[user_id]) < 200:
            #     continue
            edge_type = "REPOSTS"
            if item["interact_type"] == "comment":
                edge_type = "COMMENT"
            relation_key = static_graph[item["interact_id"]]["user_name"] + edge_type + static_graph[user_id]["user_name"]
            if item["interact_id"] not in dynamic_graph and out_flag == 1:
            #     print("filter user")
            #     print(len(dynamic_graph[user_id])/10)
            #     if random.randint(0, max(10, int(len(dynamic_graph[user_id])/10))) > 0:
            #         out_flag = 0
            # if out_flag == 1:
                out_flag = 0
                if relation_key not in relation_dict:
                    relation_dict.setdefault(relation_key, 1)
                    relation_f.write("%s\t%s\t%s\n" % (static_graph[item["interact_id"]]["user_name"], edge_type, static_graph[user_id]["user_name"]))
            if item["interact_id"] in dynamic_graph and len(dynamic_graph[item["interact_id"]]) > 0 and relation_key not in relation_dict:
                relation_dict.setdefault(relation_key, 1)
                relation_f.write("%s\t%s\t%s\n" % (static_graph[item["interact_id"]]["user_name"], edge_type, static_graph[user_id]["user_name"]))
relation_f.close()
user_f.close()


