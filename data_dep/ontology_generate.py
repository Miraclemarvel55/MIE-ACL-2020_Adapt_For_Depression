import json
import os
saveDir = os.path.dirname(__file__)
ontology = dict()
fullSchemaPathCandis = [
    "/home/zxc/PythonProjects/depression_dialog/docs/标注尝试/FullSchema.json",
    "FullSchema.json",
]
for path in fullSchemaPathCandis:
    try:
        with open(path, "r") as f:
            ontology.update(json.load(f))
            break
    except:
        pass


# 抑郁症症状分类及其examples
# 把超过目标层级的小类当做大类的examples
def recursive_ontology_resolve_for_examples(example_dict=dict(), level=0, end_level=1, level_sep=" ",
                                            ontology="ontology"):
    if isinstance(ontology, str):
        if level < end_level:
            example_dict[ontology] = dict()
        elif level == end_level:
            example_dict[ontology] = list()
        else:
            example_dict.append(ontology)
    elif isinstance(ontology, dict):
        for category, items in ontology.items():
            if level < end_level:
                example_dict[category] = dict()
            elif level == end_level:
                example_dict[category] = list()
            else: example_dict.append(category)
            if level <= end_level:
                next_container = example_dict[category]
            else:
                next_container = example_dict
            for item in items:
                recursive_ontology_resolve_for_examples(
                    example_dict=next_container, level=level + 1, end_level=end_level, level_sep=level_sep,
                    ontology=item)
    else:
        print("something outlier need to process")
    return example_dict


example_dict = recursive_ontology_resolve_for_examples(ontology=ontology)

# example_dict.update({"状态": {"阳性": [], "阴性": []}})
example_dict.update({"状态": {"阳性": [], }})
for category, items in example_dict.items():
    if category != "状态":
        items["其他"] = []

example2class = dict()
for category, items in example_dict.items():
    for class_, examples in items.items():
        for example in examples:
            example2class[example] = class_

with open(os.path.join(saveDir, "example_dict.json"), "w", newline="\n") as f:
    json.dump(example_dict, f, ensure_ascii=False, indent=1)
# ontology
ontology = dict()
for category, items in example_dict.items():
    items_without_example = sorted(items.keys())
    ontology[category] = items_without_example
assert len(ontology) == len(example_dict)
with open(os.path.join(saveDir, "ontology.json"), "w", newline="\n") as f:
    json.dump(ontology, f, ensure_ascii=False, indent=1)

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
