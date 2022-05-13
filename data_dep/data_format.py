import json
import glob
import os

home_dir = os.path.expanduser("~")
relative_base = "Tools/brat-1.3_Crunchy_Frog/data/depression_windows/{source}_windows/"
relative_dir = {
    "dev":
        {
            "CMDD": os.path.join(home_dir, relative_base.format(source="CMDD"), "validate"),
            "chunyu": os.path.join(home_dir, relative_base.format(source="chunyu"), "dev")
        },
    "test":
        {
            "CMDD": os.path.join(home_dir, relative_base.format(source="CMDD"), "test"),
            "chunyu": os.path.join(home_dir, relative_base.format(source="chunyu"), "test")
        },
    "train":
        {
            "CMDD": os.path.join(home_dir, relative_base.format(source="CMDD"), "train"),
            "chunyu": os.path.join(home_dir, relative_base.format(source="chunyu"), "train")
        }
}


def get_dialogue_dirs(source1_dir, number_max):
    source_dialogue_dirs = []
    for i in range(number_max):
        dialogue_ix = str(i).zfill(4)
        source_dialogue_dirs.append(os.path.join(source1_dir, dialogue_ix))
    return source_dialogue_dirs


def get_dialogue_dirs_2(source1_dir, sub_layers="*/*"):
    source_dialogue_dirs = sorted(glob.glob(os.path.join(source1_dir, sub_layers)))
    return source_dialogue_dirs


goal_types = ["dev", "test", "train"]


def detailLabel2formattedLabel(label_):
    """
    将标注时的不定层级的标签转为目标层级的标签
    :param label_:
    :return:
    """
    sep = ":"
    split = "-"
    if label_ not in label2info:
        if label_ in example2class:
            label_ = example2class[label_]
    try:
        slot, full_type, predecessors = label2info[label_]
    except:
        if label_ in ontology.keys():
            slot, full_type, predecessors = label_, "其他", []
        else:
            raise
    status = sep.join(["状态", "阳性"])
    label = split.join([sep.join([slot, full_type]), status])
    return label


def ann2labels(ann):
    labels = []
    with open(ann, 'r') as f:
        content = f.read().strip()
    if content:
        old_lines = content.splitlines()
        for line in old_lines:
            T_ix, value, mention = line.split("\t")
            label_, start, end = value.split(" ")
            label = detailLabel2formattedLabel(label_)
            if label not in labels:
                labels.append(label)
    return labels

for goal_type in goal_types:
    source_chunyu_dir = relative_dir[goal_type]["chunyu"]
    source_CMDD_dir = relative_dir[goal_type]["CMDD"]

    source1_dialogue_dirs = get_dialogue_dirs_2(
        source1_dir=source_chunyu_dir,
        sub_layers="*/*")
    source2_dialogue_dirs = get_dialogue_dirs_2(
        source1_dir=source_CMDD_dir,
        sub_layers="*/*")
    source2_dialogue_dirs = list()
    goal_dialogue_dirs = sorted(set(source1_dialogue_dirs + source2_dialogue_dirs))

    from ontology_generate import example_dict, ontology, example2class, label2info

    abnormal_windows = []
    dialogues = []
    # windows_dir == dialogue_dir
    for windows_dir in goal_dialogue_dirs:
        dialogue_windows = []
        anns = sorted(glob.glob(os.path.join(windows_dir, "*.ann")))
        txts = sorted(glob.glob(os.path.join(windows_dir, "*.txt")))
        assert len(anns) == len(txts)
        label = []
        for ix, ann in enumerate(anns):
            txt = txts[ix]
            assert txt[-8:-4] == ann[-8:-4]
            with open(txt, 'r') as f:
                content_txt = f.read().splitlines()
                content_txt = [line for line in content_txt if len(line.strip()) > 2]
                assert content_txt
                if len(content_txt) != 5:
                    abnormal_windows.append(txt)
                    continue
                utterances = content_txt
            # process labels
            labels = ann2labels(ann)
            window_info = {"utterances": utterances, "label": labels}
            dialogue_windows.append(window_info)
        if dialogue_windows:
            dialogues.append(dialogue_windows)
    with open(f"{goal_type}.json", 'w', newline="\n") as f:
        json.dump(dialogues, f, ensure_ascii=False, indent=1)
