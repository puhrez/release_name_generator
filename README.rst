Release Name Generator
======================

How To Use:
-----------

::

    $ python

    #  Initialize your Generator
    >>> from release_name_gen import NameGenerator
    >>> name_gen = NameGenerator

    #  Load your prefixes and names
    >>> name_gen.extend_subset_with_txt('prefixes', 'prefixes.txt')
    >>> name_gen.extend_subset_with_txt('name', 'names.txt')

    #  Generate!
    >>> name_gen.pprint_names


