import tensorflow as tf
from os.path import join
import getopt
import sys

import constants as c
from LSTMModel import LSTMModel
from data_reader import DataReader


class LyricGenRunner:
    def __init__(self, model_load_path, artist_name, test, prime_text):

        self.sess = tf.Session()
        self.artist_name = artist_name

        print 'Process data...'
        self.data_reader = DataReader(self.artist_name)
        self.vocab = self.data_reader.get_vocab()

        print 'Init model...'
        self.model = LSTMModel(self.sess,
                               self.vocab,
                               c.BATCH_SIZE,
                               c.SEQ_LEN,
                               c.CELL_SIZE,
                               c.NUM_LAYERS,
                               test=test)

        print 'Init variables...'
        self.saver = tf.train.Saver(max_to_keep=None)
        self.sess.run(tf.initialize_all_variables())

        if model_load_path is not None:
            self.saver.restore(self.sess, model_load_path)
            print 'Model restored from ' + model_load_path

        if test:
            self.test(prime_text)
        else:
            self.train()

    def train(self):
        while True:
            inputs, targets = self.data_reader.get_train_batch(
                c.BATCH_SIZE, c.SEQ_LEN)
            print 'Training model...'

            feed_dict = {self.model.inputs: inputs,
                         self.model.targets: targets}
            global_step, loss, _ = self.sess.run([self.model.global_step,
                                                  self.model.loss,
                                                  self.model.train_op],
                                                 feed_dict=feed_dict)

            print 'Step: %d | loss: %f' % (global_step, loss)
            if global_step % c.MODEL_SAVE_FREQ == 0:
                print 'Saving model...'
                self.saver.save(self.sess, join(
                    c.MODEL_SAVE_DIR, self.artist_name + '.ckpt'),
                    global_step=global_step)

    def test(self, prime_text):
        sample = self.model.generate(prime=prime_text)

        print sample


def main():
    load_path = None
    artist_name = 'kanye_west'
    test = False
    prime_text = None

    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'l:m:a:p:s:t', [
                                'load_path=', 'model_name=', 'artist_name=',
                                'prime=', 'seq_len', 'test', 'save_freq='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-l', '--load_path'):
            load_path = arg
        if opt in ('-m', '--model_name'):
            c.set_save_name(arg)
        if opt in ('-a', '--artist_name'):
            artist_name = arg
        if opt in ('-p', '--prime'):
            prime_text = arg
        if opt in ('-s', '--seq_len'):
            c.SEQ_LEN = arg
        if opt in ('-t', '--test'):
            test = True
        if opt == '--save_freq':
            c.MODEL_SAVE_FREQ = int(arg)

    LyricGenRunner(load_path, artist_name, test, prime_text)


if __name__ == '__main__':
    main()