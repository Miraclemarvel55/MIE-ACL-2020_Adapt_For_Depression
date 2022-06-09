import json
import glob
import os

goal_type = "dev"
home_dir = os.path.expanduser("~")
relative_base = "Tools/brat-1.3_Crunchy_Frog/data/depression_windows/{source}_windows/"
relative_dir = {
    "dev":
        {
            "CMDD": os.path.join(home_dir, relative_base.format(source="CMDD"), "test"),
            "chunyu": os.path.join(home_dir, relative_base.format(source="chunyu"), "dev")
        },
    "test": 1,
    "train": 2
}
source_chunyu_dir = relative_dir[goal_type]["chunyu"]
source_CMDD_dir = relative_dir[goal_type]["CMDD"]


def get_dialogue_dirs(source1_dir, number_max):
    source_dialogue_dirs = []
    for i in range(number_max):
        dialogue_ix = str(i).zfill(4)
        source_dialogue_dirs.append(os.path.join(source1_dir, dialogue_ix))
    return source_dialogue_dirs


source1_dialogue_dirs = get_dialogue_dirs(
    source1_dir=source_chunyu_dir,
    number_max=50)
source2_dialogue_dirs = get_dialogue_dirs(
    source1_dir=source_CMDD_dir,
    number_max=50)
goal_dialogue_dirs = set(source1_dialogue_dirs + source2_dialogue_dirs)

from ontology_generate import example_dict, ontology, example2class, label2info
dialogues = []
for windows_dir in goal_dialogue_dirs:
    dialogue_windows = []
    anns = sorted(glob.glob(os.path.join(windows_dir, "*.ann")))
    txts = sorted(glob.glob(os.path.join(windows_dir, "*.txt")))
    assert len(anns) == len(txts)
    label = []
    for ix, ann in enumerate(anns):
        txt = txts[ix]
        assert txt[-8:-4] == ann[-8:-4]
        with open(txt, 'r')as f:
            content_txt = f.read().splitlines()
            assert content_txt
            utterances = content_txt
        # process labels
        labels = []
        with open(ann, 'r')as f:
            content = f.read().strip()
        if content:
            old_lines = content.splitlines()
            for line in old_lines:
                T_ix, value, mention = line.split("\t")
                label_, start, end = value.split(" ")
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
                status = sep.join(["状态","阳性"])
                label = split.join([sep.join([slot, full_type]), status])
                labels.append(label)
        window_info = {"utterances": utterances, "label": labels}
        dialogue_windows.append(window_info)
    if dialogue_windows:
        dialogues.append(dialogue_windows)
with open(f"{goal_type}.json", 'w')as f:
    json.dump(dialogues, f, ensure_ascii=False)
import time
time.sleep(1)
os.system(f"cp {goal_type}.json test.json")
os.system(f"cp {goal_type}.json train.json")
