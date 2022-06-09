from data_format import ann2labels
import glob
from tqdm import tqdm

A_dir = "/home/zxc/Tools/brat-1.3_Crunchy_Frog/consistency/depression_windows/"
B_dir = "/home/zxc/Tools/brat-1.3_Crunchy_Frog/data/depression_windows/"

A_anns = list(sorted(glob.glob(A_dir + "*/*/*/*/*.ann")))
B_anns = [ann.replace(A_dir, B_dir) for ann in A_anns]

A_result = []
B_result = []

candi_labels = set()
for ix, a_ann in tqdm(enumerate(A_anns)):
    b_ann = B_anns[ix]
    window_a_labels = ann2labels(ann=a_ann)
    window_b_labels = ann2labels(ann=b_ann)
    candi_labels.update(window_a_labels)
    candi_labels.update(window_b_labels)
label2id = {label: ix for ix, label in enumerate(candi_labels)}


def window_result2one_hot_result(window_labels, label2id=label2id):
    window_result = [0] * len(label2id)
    for label in window_labels:
        window_result[label2id[label]] = 1
    return window_result


for ix, a_ann in tqdm(enumerate(A_anns)):
    b_ann = B_anns[ix]
    window_a_labels = ann2labels(ann=a_ann)
    window_b_labels = ann2labels(ann=b_ann)
    window_a_result = window_result2one_hot_result(window_labels=window_a_labels)
    window_b_result = window_result2one_hot_result(window_labels=window_b_labels)
    keep_goal_only = False
    goal = 1
    if keep_goal_only:
        tuples_ab = zip(window_a_result, window_b_result)
        try:
            window_a_result_final, window_b_result_final = zip(*filter(lambda x: goal in x, tuples_ab))
        except:
            assert goal not in window_a_result and goal not in window_b_result
            window_a_result_final, window_b_result_final = [], []
    else:
        window_a_result_final, window_b_result_final = window_a_result, window_b_result
    assert len(window_a_result_final) == len(window_b_result_final)
    A_result.extend(window_a_result_final)
    B_result.extend(window_b_result_final)

from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

sample_weight = [0.1 if a == b == 0 else 1 for (a, b) in zip(A_result, B_result)]
sample_weight = None

kappa = cohen_kappa_score(y1=A_result, y2=B_result, sample_weight=sample_weight)
f1 = f1_score(A_result, B_result, pos_label=1)
cf_matrix = confusion_matrix(A_result, B_result)
print(f"coherence:{kappa}")
print(f"f1:{f1}")
print("confusion matrix:")
print(cf_matrix)
observation_rate = (cf_matrix[0, 0] + cf_matrix[1, 1]) / sum(cf_matrix).sum()
A_p1 = sum(A_result) / len(A_result)
A_p0 = 1 - A_p1
A_0_B0 = (len(B_result) - sum(B_result)) * A_p0
A_1_B1 = sum(B_result) * A_p1
opptunity_rate = (A_0_B0 + A_1_B1) / len(A_result)
kappa_ = (observation_rate - opptunity_rate) / (1 - opptunity_rate)
print(f"观察符合率:{observation_rate}")
print(f"A的先验概率：0:{A_p0},1:{A_p1}")
print(f"B标为0在完全偶然情况下A也标为0的个数:{A_0_B0}")
print(f"B标为1在完全偶然情况下A也标为1的个数:{A_1_B1}")
print(f"机遇符合率：{opptunity_rate}")
print(f"kappa_:(observation_rate-opptunity_rate)/(1-opptunity_rate):\n{kappa_}")
