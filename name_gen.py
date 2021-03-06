# -*- coding: utf-8 -*-
"""
    release_name_gen
    ~~~~~~~~~~~~~~~~

    Use to generate names from set of prefixes and names.
    TODO:
        extend to accept arbitrary subsetsi
"""

import cPickle as pickle
import sys
import pprint
import os
import random


class UnloadedError(Exception):
    pass


class NameGenerator(object):
    SUBSETS = {'prefixes', 'names'}
    EXTENSIONS = {'.pickle'}
    DEFAULT_FILE_NAME = 'tokens_dict.pickle'

    def __init__(self, prefixes=None, names=None,
                 pickle_path=DEFAULT_FILE_NAME):
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

        self.load_tokens_from_file(pickle_path)

    @property
    def prefixes(self):
        return list(self.tokens['prefixes'])

    @property
    def names(self):
        return list(self.tokens['names'])

    def _validate_support(self, el, supported_subset):
        if el not in supported_subset:
            raise NotImplementedError(
                '%s not supported. Currently only support for %s'
                % (el, str(supported_subset))
            )
        return el

    def _extend_subset_with_txt(self, subset, text_f):
        with open(text_f) as f:
            self._validate_support(subset, self.SUBSETS)
            self.tokens[subset] |= set(line.strip() for line in f.readlines())

    def load_prefixes(self, text_f):
        self._extend_subset_with_txt('prefixes', text_f)

    def load_names(self, text_f):
        self._extend_subset_with_txt('names', text_f)

    def load_tokens_from_file(self, pickle_path, subset=None):
        """
            :param pickle_path: file path to tokens pickle
        """
        self.tokens_pickle = pickle_path
        try:
            with open(self.tokens_pickle) as f:
                self._validate_support(
                    os.path.splitext(self.tokens_pickle)[1],
                    self.EXTENSIONS
                )
                loaded_tokens = pickle.load(f)
                self.tokens['prefixes'] |= loaded_tokens.get('prefixes', set())
                self.tokens['names'] |= loaded_tokens.get('names', set())
                self.used = loaded_tokens.get('used', set())
        except (IOError, EOFError):
            self.save()

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
        if not self.prefixes or not self.names:
            raise UnloadedError(
                'You gotta load your prefixes and names silly...'
            )

        prefix_name = random.choice(self.prefixes).split(' ') + \
            random.choice(self.names).split(' ')
        # import pdb; pdb.set_trace()
        pull_request_name = ' '.join(prefix_name)
        branch_name = '-'.join(prefix_name).lower()

        if branch_name in self.used:
            self.generate_name()
        else:
            self.used.add(branch_name)
            self.save()
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

    def reset_tokens(self, save=True, **save_kwargs):
        choice = raw_input(
            "You're about to reset (decimate) your tokens, dat cool? (y/n) "
        ).lower()
        yes_alternatives = {'y', 'yes'}
        if not any(y for y in yes_alternatives if y in choice):
            print "not cool"
            return
        print "cool"
        self.used = set()
        self.tokens.update(
            prefixes=set(),
            names=set()
        )
        if save:
            self.save(*save_kwargs)

    def pprint_names(self, debug=None):
        """pprints the name generated by generate_name"""
        pr_name, branch_name = self.generate_name()
        print
        print 'PR Name:', pr_name
        print 'Branch Name:', branch_name
        print
        if debug:
            print '\nDEBUG\n'
            pprint.pprint(self.as_dict())
        return


def get_arg_param(arg):
    """
        given that the parameter to a cli argument follows the argument,
        this func returns it or None if it doesn't exist
        :param arg: string representing argument
    """
    try:
        file_name_index = sys.argv.index(arg)
        return sys.argv[file_name_index + 1]
    except ValueError:
        return None

if __name__ == '__main__':
    settings = {
        'load_tokens': get_arg_param('-l') or get_arg_param('--load'),
        'load_prefixes': get_arg_param('-p') or get_arg_param('--prefixes'),
        'load_names': get_arg_param('-n') or get_arg_param('--names'),
        'reset_tokens': '-r' in sys.argv or '--reset' in sys.argv,
        'debug': '-d' in sys.argv or'--debug' in sys.argv
    }
    if settings['load_tokens']:
        name_gen = NameGenerator(
            pickle_path=settings['load_tokens'])
    else:
        name_gen = NameGenerator()

    if settings['reset_tokens']:
        name_gen.reset_tokens()

    if settings['load_prefixes']:
        name_gen.load_prefixes(settings['load_prefixes'])

    if settings['load_names']:
        name_gen.load_names(settings['load_names'])

    if name_gen.names and name_gen.prefixes:
        name_gen.pprint_names(
            debug=settings['debug']
        )
    elif not settings['reset_tokens']:
        print 'Waiting to get fed'

    name_gen.save()
