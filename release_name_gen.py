# -*- coding: utf-8 -*-
"""
    release_name_gen
    ~~~~~~~~~~~~~~~~

    Use to generate names from set of prefixes and names.
"""

import cPickle as pickle
import sys
import pprint
import os
import random

DEFAULT_FILE_NAME = 'tokens_dict.pickle'


class NameGenerator(object):
    SUBSETS = {'prefixes', 'names'}
    EXTENSIONS = {'.pickle'}

    def __init__(self, prefixes=None, names=None,
                 pickle_path=None):
        """
        :param prefixes: list of prefixes
        :param names: list of names
        :param pickle_path: path to pickle to load tokens from
        """
        self.tokens = {}
        self.tokens['prefixes'] = set(prefixes) if prefixes else set()
        self.tokens['names'] = set(names) if names else set()
        self.used = set()
        self.tokens_pickle = pickle_path

        if self.tokens_pickle:
            self.load_tokens_from_file(pickle_path)

    @property
    def prefixes(self):
        return list(self.tokens['prefixes'])

    @property
    def names(self):
        return list(self.tokens['names'])

    def _validate_support(self, s, supported_subset):
        if s not in supported_subset:
            raise NotImplementedError(
                '%s not supported. Currently only support for %s'
                % (s, str(supported_subset))
            )
        return s

    def extend_subset_with_txt(self, subset, text_f):
        with open(text_f) as f:
            self._validate_support(subset, self.SUBSETS)
            self.tokens[subset] += f.readlines()

    def load_tokens_from_file(self, pickle_path, subset=None):
        """
            :param pickle_path: file path to tokens pickle
        """
        self.tokens_pickle = pickle_path
        with open(self.tokens_pickle) as f:
            self._validate_support(
                os.path.splitext(self.tokens_pickle)[1],
                self.EXTENSIONS
            )
            loaded_tokens = pickle.load(f)
            self.tokens.update(
                prefixes=loaded_tokens['prefixes'],
                names=loaded_tokens['names'])
            self.used = loaded_tokens['used']

    def save(self, pickle_path=None):
        self.tokens_pickle = pickle_path or self.tokens_pickle
        with open(self.tokens_pickle, 'w') as f:
            pickle.dump(self.as_dict(), f)

    def generate_name(self):
        """
            :param prefixes: list(strings)
            :param names: list(strings)
            :param used: list(strings of used combination)
        """
        prefix_name = random.choice(self.prefixes).split(' ') + \
            random.choice(self.names).split(' ')
        # import pdb; pdb.set_trace()
        pull_request_name = ' '.join(prefix_name)
        branch_name = '-'.join(prefix_name).lower()

        if branch_name in self.used:
            self.generate_name()
        else:
            self.used.add(branch_name)
            return (
                pull_request_name,
                branch_name,
            )

    def as_dict(self):
        return {
            'prefixes': self.tokens['prefixes'],
            'used': self.used,
            'names': self.tokens['names']
        }

    def clean_tokens(self, save=True, **save_kwargs):
        self.used = set()
        if save:
            self.save(*save_kwargs)

    def pprint_names(self, debug=None):
        """pprints the name generated by generate_name"""
        pr_name, branch_name = self.generate_name()
        print 'PR Name:', pr_name
        print 'Branch Name:', branch_name
        if debug:
            print '\nDEBUG\n'
            pprint.pprint(self.as_dict())


if __name__ == '__main__':
    if '-l' in sys.argv or '--load' in sys.argv:
        try:
            file_name_index = sys.argv.index('-l')
        except:
            file_name_index = sys.argv.index('--load')
        name_gen = NameGenerator(pickle_path=sys.argv[file_name_index + 1])
    else:
        name_gen = NameGenerator(pickle_path=DEFAULT_FILE_NAME)

    if '--clean' in sys.argv or '-c' in sys.argv:
        name_gen.clean_tokens()

    name_gen.pprint_names(
        debug=True if '-d' in sys.argv or'--debug' in sys.argv
        else None
    )

    name_gen.save()
