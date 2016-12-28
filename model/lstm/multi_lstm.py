import tensorflow as tf
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import seq2seq

import numpy as np

class Multi_lstm():
    def __init__(self, args, infer=False):
        self.args = args
        if infer:
            args.batch_size = 1
            args.seq_length = 1

        cell_fn = rnn_cell.BasicLSTMCell
        cell = cell_fn(args.rnn_size, state_is_tuple=True)
        self.cell = cell = rnn_cell.MultiRNNCell([cell] * args.num_layers, state_is_tuple=True)

        self.input_data = tf.placeholder(tf.float32, [args.batch_size, args.seq_length])
        self.target = tf.placeholder(tf.float32, [args.batch_size,args.seq_length])
        self.initial_state = cell.zero_state(args.batch_size, tf.float32)

