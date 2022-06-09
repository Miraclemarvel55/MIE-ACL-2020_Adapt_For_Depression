import argparse
import os
os.environ['CUDA_VISIBLE_DEVICES'] = "5"
import tensorflow as tf

from src import Dictionary, Ontology, Data, MIE, evaluate

parser = argparse.ArgumentParser(description='MIE')
parser.add_argument('--add-global', type=bool, default=False, help='Add global module or not.')
parser.add_argument('--hidden-size', type=int, default=400, help='Hidden size.')
parser.add_argument('--mlp-layer-num', type=int, default=4, help='Number of layers of mlp.')
parser.add_argument('--keep-p', type=float, default=0.8, help='1 - dropout rate.')

parser.add_argument('--start-lr', type=float, default=1e-3, help='Start learning rate.')
parser.add_argument('--end-lr', type=float, default=1e-4, help='End learning rate.')
parser.add_argument('-e', '--epoch-num', type=int, default=100, help='Epoch num.')
parser.add_argument('-b', '--batch-size', type=int, default=64, help='Batch size.')
parser.add_argument('-t', '--tbatch-size', type=int, default=15, help='Test batch size.')
parser.add_argument('-g', '--gpu-id', type=str, default='5', help='Gpu id.')
parser.add_argument('-l', '--location', type=str, default='model_files/MIE', help='Location to save.')
args = parser.parse_args()


data_dir = "data_dep"
dictionary = Dictionary()
dictionary.load(f'./data/dictionary.txt')

ontology = Ontology(dictionary)
ontology.add_raw(f'./{data_dir}/ontology.json', '状态')
ontology.add_examples(f'./{data_dir}/example_dict.json')
ontology.onto2ids()
data = Data(100, dictionary, ontology)
data.add_raw('train', f'./{data_dir}/train.json', 'window')
data.add_raw('test', f'./{data_dir}/test.json', 'window')
data.add_raw('dev', f'./{data_dir}/dev.json', 'window')

# params of the model.
params = {
    "add_global": args.add_global,
    "num_units": args.hidden_size,
    "num_layers": args.mlp_layer_num,
    "keep_p": args.keep_p
}

# Initialize the model.
model = MIE(data, ontology, params=params)
# model = MIE(data, ontology, params=params, location=args.location)

# Train the model.
model.train(
    epoch_num=args.epoch_num,
    batch_size=args.batch_size,
    tbatch_size=args.tbatch_size,
    start_lr=args.start_lr,
    end_lr=args.end_lr,
    location=args.location)

# Test the model.
infos = evaluate(model, 'test', 100)
from pprint import pprint
pprint(infos)
