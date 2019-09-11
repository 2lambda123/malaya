import pickle
import os
import numpy as np
from .texts._distance import JaroWinkler
from scipy.spatial.distance import cdist
from sklearn.neighbors import NearestNeighbors
import tensorflow as tf
from . import home
from ._utils._utils import download_file, _Calculator


def load_wiki():
    """
    Return malaya pretrained wikipedia word2vec size 256.

    Returns
    -------
    dictionary: dictionary of dictionary, reverse dictionary and vectors
    """
    if not os.path.isfile('%s/word2vec-wiki/word2vec.p' % (home)):
        print('downloading word2vec-wiki embedded')
        download_file(
            'v13/word2vec/word2vec-wiki-nce-256.p',
            '%s/word2vec-wiki/word2vec.p' % (home),
        )
    with open('%s/word2vec-wiki/word2vec.p' % (home), 'rb') as fopen:
        return pickle.load(fopen)


def load_news(size = 256):
    """
    Return malaya pretrained news word2vec.

    Parameters
    ----------
    size: int, (default=256)

    Returns
    -------
    dictionary: dictionary of dictionary, reverse dictionary and vectors
    """
    if not isinstance(size, int):
        raise ValueError('input must be an integer')
    if size not in [32, 64, 128, 256, 512]:
        raise ValueError(
            'size word2vec not supported, only supports [32, 64, 128, 256, 512]'
        )
    if not os.path.isfile('%s/word2vec-%d/word2vec.p' % (home, size)):
        print('downloading word2vec-%d embedded' % (size))
        download_file(
            'v7/word2vec/word2vec-%d.p' % (size),
            '%s/word2vec-%d/word2vec.p' % (home, size),
        )
    with open('%s/word2vec-%d/word2vec.p' % (home, size), 'rb') as fopen:
        return pickle.load(fopen)


def load(embed_matrix, dictionary):

    """
    Return malaya.wordvector._wordvector object.

    Parameters
    ----------
    embed_matrix: numpy array
    dictionary: dictionary

    Returns
    -------
    _wordvector: malaya.wordvector._wordvector object
    """

    return _wordvector(embed_matrix = embed_matrix, dictionary = dictionary)


class _wordvector:
    def __init__(self, embed_matrix, dictionary):
        self._embed_matrix = embed_matrix
        self._dictionary = dictionary
        self._reverse_dictionary = {v: k for k, v in dictionary.items()}
        self.words = list(dictionary.keys())
        self._jarowinkler = JaroWinkler()
        _graph = tf.Graph()
        with _graph.as_default():
            self._embedding = tf.placeholder(
                tf.float32, self._embed_matrix.shape
            )
            self._x = tf.placeholder(
                tf.float32, [None, self._embed_matrix.shape[1]]
            )
            normed_embedding = tf.nn.l2_normalize(self._embedding, axis = 1)
            normed_array = tf.nn.l2_normalize(self._x, axis = 1)
            self._cosine_similarity = tf.matmul(
                normed_array, tf.transpose(normed_embedding, [1, 0])
            )
            self._sess = tf.InteractiveSession()

    def get_vector_by_name(self, word):
        """
        get vector based on string.

        Parameters
        ----------
        word: str

        Returns
        -------
        vector: numpy
        """
        if not isinstance(word, str):
            raise ValueError('input must be a string')
        if word not in self._dictionary:
            arr = np.array(
                [self._jarowinkler.similarity(word, k) for k in self.words]
            )
            idx = (-arr).argsort()[:5]
            strings = ', '.join([self.words[i] for i in idx])
            raise Exception(
                'input not found in dictionary, here top-5 nearest words [%s]'
                % (strings)
            )
        return self._embed_matrix[self._dictionary[word]]

    def tree_plot(self, labels, figsize = (7, 7), annotate = True):
        """
        plot a tree plot based on output from calculator / n_closest / analogy.

        Parameters
        ----------
        labels : list
            output from calculator / n_closest / analogy.
        visualize : bool
            if True, it will render plt.show, else return data.
        figsize : tuple, (default=(7, 7))
            figure size for plot.

        Returns
        -------
        results: [embed, labelled]
        """

        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            sns.set()
        except:
            raise Exception(
                'matplotlib and seaborn not installed. Please install it and try again.'
            )

        if not isinstance(labels, list):
            raise ValueError('input must be a list')
        if not isinstance(figsize, tuple):
            raise ValueError('figsize must be a tuple')
        if not isinstance(annotate, bool):
            raise ValueError('annotate must be a boolean')

        idx = [
            self.words.index(e[0] if isinstance(e, list) else e) for e in labels
        ]
        embed = self._embed_matrix[idx]
        embed = embed.dot(embed.T)
        embed = (embed - embed.min()) / (embed.max() - embed.min())
        labelled = []
        for label in labels:
            label = (
                '%s, %.3f' % (label[0], label[1])
                if isinstance(label, list)
                else label
            )
            labelled.append(label)

        plt.figure(figsize = figsize)
        g = sns.clustermap(
            embed,
            cmap = 'Blues',
            xticklabels = labelled,
            yticklabels = labelled,
            annot = annotate,
        )
        plt.show()
        return embed, labelled

    def scatter_plot(
        self,
        labels,
        centre = None,
        figsize = (7, 7),
        plus_minus = 25,
        handoff = 5e-5,
    ):
        """
        plot a scatter plot based on output from calculator / n_closest / analogy.

        Parameters
        ----------
        labels : list
            output from calculator / n_closest / analogy
        centre : str, (default=None)
            centre label, if a str, it will annotate in a red color.
        figsize : tuple, (default=(7, 7))
            figure size for plot.

        Returns
        -------
        list_dictionaries: list of results
        """

        try:
            from sklearn.manifold import TSNE
            import matplotlib.pyplot as plt
            import seaborn as sns

            sns.set()
        except:
            raise Exception(
                'matplotlib and seaborn not installed. Please install it and try again.'
            )

        if not isinstance(labels, list):
            raise ValueError('input must be a list')
        if not isinstance(figsize, tuple):
            raise ValueError('figsize must be a tuple')
        if not isinstance(plus_minus, int):
            raise ValueError('plus_minus must be an integer')

        idx = [
            self.words.index(e[0] if isinstance(e, list) else e) for e in labels
        ]
        if centre:
            if not isinstance(centre, str):
                raise ValueError('centre must be a string')
            idx.append(self.words.index(centre))
        cp_idx = idx[:]
        for i in idx:
            cp_idx.extend(np.arange(i - plus_minus, i).tolist())
            cp_idx.extend(np.arange(i, i + plus_minus).tolist())
        tsne = TSNE(n_components = 2, random_state = 0).fit_transform(
            self._embed_matrix[cp_idx]
        )

        plt.figure(figsize = figsize)
        plt.scatter(tsne[:, 0], tsne[:, 1])
        for label, x, y in zip(
            labels, tsne[: len(labels), 0], tsne[: len(labels), 1]
        ):
            label = (
                '%s, %.3f' % (label[0], label[1])
                if isinstance(label, list)
                else label
            )
            plt.annotate(
                label,
                xy = (x, y),
                xytext = (0, 0),
                textcoords = 'offset points',
            )
        if centre:
            plt.annotate(
                centre,
                xy = (tsne[len(labels), 0], tsne[len(labels), 1]),
                xytext = (0, 0),
                textcoords = 'offset points',
                color = 'red',
            )
        plt.xlim(
            tsne[: len(idx), 0].min() + handoff,
            tsne[: len(idx), 0].max() + handoff,
        )
        plt.ylim(
            tsne[: len(idx), 1].min() + handoff,
            tsne[: len(idx), 1].max() + handoff,
        )
        plt.xticks([])
        plt.yticks([])
        plt.show()
        return tsne

    def _calculate(self, equation):
        tokens, temp = [], ''
        for char in equation:
            if char == ' ':
                continue
            if char not in '()*+-':
                temp += char
            else:
                if len(temp):
                    row = self._dictionary[
                        self.words[
                            np.argmax(
                                [
                                    self._jarowinkler.similarity(temp, k)
                                    for k in self.words
                                ]
                            )
                        ]
                    ]
                    tokens.append(
                        ','.join(
                            self._embed_matrix[row, :].astype('str').tolist()
                        )
                    )
                    temp = ''
                tokens.append(char)
        if len(temp):
            row = self._dictionary[
                self.words[
                    np.argmax(
                        [
                            self._jarowinkler.similarity(temp, k)
                            for k in self.words
                        ]
                    )
                ]
            ]
            tokens.append(
                ','.join(self._embed_matrix[row, :].astype('str').tolist())
            )
        return _Calculator(tokens).exp()

    def _batch_process(self, batch, num_closest = 5, return_similarity = True):
        top_k = tf.nn.top_k(self._cosine_similarity, k = num_closest)
        results = self._sess.run(
            top_k,
            feed_dict = {self._x: batch, self._embedding: self._embed_matrix},
        )
        indices = results.indices
        values = results.values
        words = []
        if not return_similarity:
            for result in indices:
                words.append([self._reverse_dictionary[i] for i in result])
        else:
            for no in range(len(results)):
                words.append(
                    [
                        (
                            self._reverse_dictionary[indices[no, i]],
                            values[no, i],
                        )
                        for i in range(len(indices[no]))
                    ]
                )
        return words

    def batch_calculator(
        self, equations, num_closest = 5, return_similarity = False
    ):
        """
        batch calculator parser for word2vec using tensorflow.

        Parameters
        ----------
        equations: list of str
            Eg, '[(mahathir + najib) - rosmah]'
        num_closest: int, (default=5)
            number of words closest to the result.

        Returns
        -------
        word_list: list of nearest words
        """
        if not isinstance(equations, list):
            raise ValueError('equations must be a list of string')
        if not isinstance(num_closest, int):
            raise ValueError('num_closest must be an integer')
        if not isinstance(return_similarity, bool):
            raise ValueError('return_similarity must be a boolean')
        batches = np.array([self._calculate(eq) for eq in equations])
        return self._batch_process(
            batches,
            num_closest = num_closest,
            return_similarity = return_similarity,
        )

    def calculator(
        self,
        equation,
        num_closest = 5,
        metric = 'cosine',
        return_similarity = True,
    ):
        """
        calculator parser for word2vec.

        Parameters
        ----------
        equation: str
            Eg, '(mahathir + najib) - rosmah'
        num_closest: int, (default=5)
            number of words closest to the result.
        metric: str, (default='cosine')
            vector distance algorithm.
        return_similarity: bool, (default=True)
            if True, will return between 0-1 represents the distance.

        Returns
        -------
        word_list: list of nearest words
        """
        if not isinstance(equation, str):
            raise ValueError('input must be a string')
        if not isinstance(num_closest, int):
            raise ValueError('num_closest must be an integer')
        if not isinstance(metric, str):
            raise ValueError('metric must be a string')
        if not isinstance(return_similarity, bool):
            raise ValueError('num_closest must be a boolean')
        calculated = self._calculate(equation)
        if return_similarity:
            nn = NearestNeighbors(num_closest + 1, metric = metric).fit(
                self._embed_matrix
            )
            distances, idx = nn.kneighbors(calculated.reshape((1, -1)))
            word_list = []
            for i in range(1, idx.shape[1]):
                word_list.append(
                    [self._reverse_dictionary[idx[0, i]], 1 - distances[0, i]]
                )
            return word_list
        else:
            closest_indices = self.closest_row_indices(
                calculated, num_closest + 1, metric
            )
            word_list = []
            for i in closest_indices:
                word_list.append(self._reverse_dictionary[i])
            return word_list

    def batch_n_closest(
        self, words, num_closest = 5, return_similarity = False, soft = True
    ):
        """
        find nearest words based on a batch of words using Tensorflow.

        Parameters
        ----------
        words: list
            Eg, ['najib','anwar']
        num_closest: int, (default=5)
            number of words closest to the result.
        return_similarity: bool, (default=True)
            if True, will return between 0-1 represents the distance.
        soft: bool, (default=True)
            if True, a word not in the dictionary will be replaced with nearest fuzzywuzzy ratio.
            if False, it will throw an exception if a word not in the dictionary.

        Returns
        -------
        word_list: list of nearest words
        """
        if not isinstance(words, list):
            raise ValueError('input must be list of strings')
        if not isinstance(num_closest, int):
            raise ValueError('num_closest must be an integer')
        if not isinstance(return_similarity, bool):
            raise ValueError('return_similarity must be a boolean')
        if not isinstance(soft, bool):
            raise ValueError('soft must be a boolean')
        if soft:
            for i in range(len(words)):
                if words[i] not in self.words:
                    words[i] = self.words[
                        np.argmax(
                            [
                                self._jarowinkler.similarity(words[i], k)
                                for k in self.words
                            ]
                        )
                    ]
        else:
            for i in range(len(words)):
                if words[i] not in self.words:
                    raise Exception(
                        '%s not in dictionary, please use another word or set `soft` = True'
                        % (words[i])
                    )
        batches = np.array([self.get_vector_by_name(w) for w in words])
        return self._batch_process(
            batches,
            num_closest = num_closest,
            return_similarity = return_similarity,
        )

    def n_closest(
        self, word, num_closest = 5, metric = 'cosine', return_similarity = True
    ):
        """
        find nearest words based on a word.

        Parameters
        ----------
        word: str
            Eg, 'najib'
        num_closest: int, (default=5)
            number of words closest to the result.
        metric: str, (default='cosine')
            vector distance algorithm.
        return_similarity: bool, (default=True)
            if True, will return between 0-1 represents the distance.

        Returns
        -------
        word_list: list of nearest words
        """
        if not isinstance(word, str):
            raise ValueError('input must be a string')
        if not isinstance(num_closest, int):
            raise ValueError('num_closest must be an integer')
        if not isinstance(metric, str):
            raise ValueError('metric must be a string')
        if not isinstance(return_similarity, bool):
            raise ValueError('num_closest must be a boolean')
        if return_similarity:
            nn = NearestNeighbors(num_closest + 1, metric = metric).fit(
                self._embed_matrix
            )
            distances, idx = nn.kneighbors(
                self.get_vector_by_name(word).reshape((1, -1))
            )
            word_list = []
            for i in range(1, idx.shape[1]):
                word_list.append(
                    [self._reverse_dictionary[idx[0, i]], 1 - distances[0, i]]
                )
            return word_list
        else:
            wv = self.get_vector_by_name(word)
            closest_indices = self.closest_row_indices(
                wv, num_closest + 1, metric
            )
            word_list = []
            for i in closest_indices:
                word_list.append(self._reverse_dictionary[i])
            if word in word_list:
                word_list.remove(word)
            return word_list

    def closest_row_indices(self, wv, num, metric):
        dist_array = np.ravel(
            cdist(self._embed_matrix, wv.reshape((1, -1)), metric = metric)
        )
        sorted_indices = np.argsort(dist_array)
        return sorted_indices[:num]

    def analogy(self, a, b, c, num = 1, metric = 'cosine'):
        """
        analogy calculation, vb - va + vc.

        Parameters
        ----------
        a: str
        b: str
        c: str
        num: int, (default=1)
        metric: str, (default='cosine')
            vector distance algorithm.

        Returns
        -------
        word_list: list of nearest words
        """
        if not isinstance(a, str):
            raise ValueError('a must be a string')
        if not isinstance(b, str):
            raise ValueError('b must be a string')
        if not isinstance(c, str):
            raise ValueError('c must be a string')
        if a not in self._dictionary:
            raise Exception('a not in dictinary')
        if b not in self._dictionary:
            raise Exception('b not in dictinary')
        if c not in self._dictionary:
            raise Exception('c not in dictinary')
        va = self.get_vector_by_name(a)
        vb = self.get_vector_by_name(b)
        vc = self.get_vector_by_name(c)
        vd = vb - va + vc
        closest_indices = self.closest_row_indices(vd, num, metric)
        d_word_list = []
        for i in closest_indices:
            d_word_list.append(self._reverse_dictionary[i])
        return d_word_list

    def project_2d(self, start, end):
        """
        project word2vec into 2d dimension.

        Parameters
        ----------
        start: int
        end: int

        Returns
        -------
        tsne decomposition: numpy
        """
        if not isinstance(start, int):
            raise ValueError('start must be an integer')
        if not isinstance(end, int):
            raise ValueError('end must be an integer')
        tsne = TSNE(n_components = 2)
        embed_2d = tsne.fit_transform(self._embed_matrix[start:end, :])
        word_list = []
        for i in range(start, end):
            word_list.append(self._reverse_dictionary[i])
        return embed_2d, word_list

    def network(
        self,
        word,
        num_closest = 8,
        depth = 4,
        min_distance = 0.5,
        iteration = 300,
        figsize = (15, 15),
        node_color = '#72bbd0',
        node_factor = 50,
    ):

        """
        plot a social network based on word given

        Parameters
        ----------
        word : str
            centre of social network.
        num_closest: int, (default=8)
            number of words closest to the node.
        depth: int, (default=4)
            depth of social network. More deeper more expensive to calculate, big^O(num_closest ** depth).
        min_distance: float, (default=0.5)
            minimum distance among nodes. Increase the value to increase the distance among nodes.
        iteration: int, (default=300)
            number of loops to train the social network to fit min_distace.
        figsize: tuple, (default=(15, 15))
            figure size for plot.
        node_color: str, (default='#72bbd0')
            color for nodes.
        node_factor: int, (default=10)
            size factor for depth nodes. Increase this value will increase nodes sizes based on depth.

        Returns
        -------
        g: networkx graph object
        """

        try:
            import pandas as pd
            import networkx as nx
            import matplotlib.pyplot as plt
        except:
            raise Exception(
                'matplotlib, networkx and pandas not installed. Please install it and try again.'
            )

        if not isinstance(word, str):
            raise ValueError('input must be a string')
        if not isinstance(num_closest, int):
            raise ValueError('num_closest must be an integer')
        if not isinstance(depth, int):
            raise ValueError('depth must be an integer')
        if not isinstance(min_distance, float):
            raise ValueError('min_distance must be a float')
        if not isinstance(iteration, int):
            raise ValueError('iteration must be an integer')
        if not isinstance(figsize, tuple):
            raise ValueError('figsize must be a tuple')
        n_closest = self.n_closest

        def get_follower(
            centre,
            top,
            max_depth = depth,
            current_depth = 0,
            accepted_list = [],
            data = [],
        ):
            if current_depth == max_depth:
                return data, accepted_list
            if centre in accepted_list:
                return data, accepted_list
            else:
                accepted_list.append(centre)

            closest = n_closest(
                centre, num_closest = num_closest, return_similarity = False
            )

            d = {
                'name': centre,
                'followers_ids': closest,
                'centre': top,
                'power': max_depth - current_depth,
            }

            data.append(d)

            cd = current_depth

            if cd + 1 < max_depth:
                for fid in closest:
                    data, accepted_list = get_follower(
                        fid,
                        fid,
                        max_depth = max_depth,
                        current_depth = cd + 1,
                        accepted_list = accepted_list,
                        data = data,
                    )

            return data, accepted_list

        data, accepted_list = get_follower(word, word)
        df = pd.DataFrame(data)
        id_unique = np.unique(df['centre']).tolist()

        followers = []
        for i in range(df.shape[0]):
            followers += df.followers_ids.iloc[i]
        followers = list(set(followers))

        followers = [i for i in followers if i in id_unique]
        true_followers = []
        for i in range(df.shape[0]):
            follows = df.followers_ids.iloc[i]
            follows = [k for k in follows if k in followers]
            true_followers.append(follows)

        df['true_followers'] = true_followers

        G = nx.Graph()

        for i in range(df.shape[0]):
            size = df.power.iloc[i] * node_factor
            G.add_node(df.centre.iloc[i], name = df.centre.iloc[i], size = size)

        for i in range(df.shape[0]):
            for k in df.true_followers.iloc[i]:
                G.add_edge(df.centre.iloc[i], k)

        sizes = [G.node[node]['size'] for node in G]
        names = [G.node[node]['name'] for node in G]

        labeldict = dict(zip(G.nodes(), names))
        plt.figure(figsize = figsize)
        plt.axis('equal')
        nx.draw(
            G,
            node_color = node_color,
            labels = labeldict,
            with_labels = 1,
            node_size = sizes,
            pos = nx.spring_layout(G, k = min_distance, iterations = iteration),
        )
        plt.show()
        return G