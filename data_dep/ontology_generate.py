import json

# 抑郁症症状分类
example_dict = {
    "认知症状":
        {
            "专注困难": ["注意力不集中"],
            "记忆力减退": [],
            "脑子不清醒": ["表达能力差", "想问题费劲", "思维迟缓反应慢"]
        },
    "自我评价低":
        {
            "厌恶自己": [],
            "感到不被需要": [],
            "感到自卑": ["觉得没自信", "觉得没能力", "觉得没用", "觉得没价值"]
        },
    "抑郁情况":
        {
            "兴趣减退或丢失": [],
            "情绪低落": ["快乐减退或丢失", "心情不好或郁闷抑郁", "不顺心或心很累", "心情时好时坏", "没有感觉或冷漠无所谓"],
            "哭泣": [],
            "孤独少话": ["抗拒交流"],
            "自残自杀轻生": ["想不开", "不想活了", "觉得生活无意义"],
            "疲乏无力": ["身体很累", "没活力", "动作迟缓"],
            "自责自罪自我惩罚": [],
            "当下没动力": ["不想做事"],
            "对未来悲观泄气": ["感到无希望", "感到绝望", "迷茫无助"]
        },
    "焦虑或强迫":
        {
            "压力大": ["学业压力大", "工作事业压力大"],
            "紧张": ["心慌", "心跳过快", "心悸"],
            "烦躁或燥动": ["坐立不安", "心神不宁"],
            "反复清洁或检查": []
        },
    "人际关系敏感或敌对":
        {
            "压抑": ["像被囚禁"],
            "易怒": ["摔东西"],
            "觉得别人议论自己": [],
            "觉得周围不友善": ["觉得别人要害自己"],
            "觉得不被信任": [],
            "觉得没有安全感": [],
        },
        "恐惧或恐怖": {
            "害怕某种情境": [],
            "害怕某人或某物": []
        },
        "偏执和精神病性症状": {
            "臆想或妄想": ["幻想"],
            "疑症": [],
            "幻觉": ["幻视", "幻听"]
        },
        "躯体化症状": {
            "气短": [],
            "胸闷胸痛": [],
            "恶心呕吐": [],
            "腹痛": [],
            "头沉头痛头晕": [],
            "肠胃问题": [],
            "睡眠问题": ["睡不醒", "失眠难以入眠", "睡眠时间短", "睡眠浅或易醒", "多梦", "早醒"],
            "性欲变化": ["性欲增强", "性欲减弱"],
            "体重变化": ["体重变轻", "体重变重"]
        },
    "其他情况":
        {
            "饮食变化": ["饮食不规律.暴饮暴食", "食量增大", "食量减少", "吃不下"],
            "饮酒变化": ["饮酒增多", "饮酒减少", "一直不饮酒"],
            "童年受过创伤": [],
            "确诊过抑郁症或家族史阳性": [],
            "处在特殊时期": ["怀孕或产后", "青春期", "更年期"],
            "性生活不协调": [],
            "重大生活事件": ["嫁到外地", "丧偶", "退休"]
        }
}
example_dict.update({"状态": {"阳性": [], "阴性": []}})
for category, items in example_dict.items():
    if category != "状态":
        items["其他"] = []


example2class = dict()
for category, items in example_dict.items():
    for class_, examples in items.items():
        for example in examples:
            example2class[example] = class_

with open("example_dict.json", "w")as f:
    json.dump(example_dict, f, ensure_ascii=False)
# ontology
ontology = dict()
for category, items in example_dict.items():
    items_without_example = sorted(items.keys())
    ontology[category] = items_without_example
assert len(ontology) == len(example_dict)
with open("ontology.json", "w")as f:
    json.dump(ontology, f, ensure_ascii=False)

label2info = dict()
for category, items in ontology.items():
    if category == "状态":
        continue
    items_set = set(items)
    for full_name in items:
        predecessors = []
        nodes = full_name.split(".")
        full_name_maybe = ""
        for node in nodes:
            full_name_maybe += node
            if full_name_maybe in items_set and full_name_maybe != full_name:
                predecessors.append(full_name_maybe)
        label_name = nodes[-1]
        label2info[label_name] = (category, full_name, predecessors)
        assert len(predecessors) == 0
