# coding: utf-8

import gensim
import numpy as np
import pymorphy2




def w2v_transformation(data, labels, word2vec_model):
    """
    transform the data - it can be pandas format or just array
    labels for indexing because not all rows can be transformed
    :param data: data - pandas, numpy, list
    :param labels: pandas, numpy, list
    :param word2vec_model
    :return: transformed_data and appropriate labels
    """

    mapping = {
        'ADJF': '_A',
        'NOUN': '_S',
        'INFN': '_V',
    }
    morph = pymorphy2.MorphAnalyzer()

    train_vectors = []
    train_labels = []
    # save indexes of labels
    for i, s in enumerate(data):
        words = s.split(' ')

        words_vector = None
        words_count = 0

        for w in words:
            w = morph.parse(w)[0]
            if w.tag.POS in mapping:
                new_w = '{}{}'.decode('utf-8').format(w.normal_form,
                                                      mapping[w.tag.POS])
                v = vector(new_w, word2vec_model)
                if isinstance(v, np.ndarray):
                    words_count += 1

                    if isinstance(words_vector, np.ndarray):
                        words_vector = words_vector + v
                    else:
                        words_vector = v

        if isinstance(words_vector, np.ndarray) and words_count > 0:
            words_vector = words_vector / words_count
        else:
            words_vector = None

        if isinstance(words_vector, np.ndarray):
            train_labels.append(labels[i])
            train_vectors.append(words_vector)

    train_vectors = np.array(train_vectors)
    return train_vectors, np.array(train_labels)


def vector(q, word2vec_model):
    """
    transform a single word to word2vec model - 500 digits
    :param q: just a word from w2v vocabulary
    :param word2vec_model: word2vec model
    :return: vector from 500 digits, numpy
    """
    qf = q

    if q not in word2vec_model:
        candidates_set = set()

        candidates_set.add(q.upper())
        candidates_set.add(q.lower())
        candidates_set.add(q.capitalize())

        no_results = True
        for candidate in candidates_set:
            if candidate in word2vec_model:
                qf = candidate
                no_results = False
                break

        if no_results:
            # obvious that not all elements
            # in corpus will from our vocabulary
            return None

    raw_vector = word2vec_model[qf]
    return raw_vector


def get_word2vec_model(binary_filename, **kwargs):
    """
    get word2vec model from source file
    it is impossible to learn it here

    :param binary_filename: filename (binary format)
    :param kwargs: it is really binary (binary=True)
    :return: word2vec model
    """
    model = gensim.models.Word2Vec.load_word2vec_format(
        binary_filename,
        binary=kwargs.get('binary')
    )

    model.init_sims(replace=True)
    return model
