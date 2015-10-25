Release Name Generator
======================

Ever want to release your masterpiece to the world of version control but no clue how to
refer to it internally?

**worry no more**

Release Name Generator has got you covered!~~~

Just feed it with a set of prefixes and names and kablam! You got a release name
for your Pull Request and your Branch!

How To Use:
-----------

::

    # First run it with the prefixes and names you want to use
    $ python name_gen.py -n sample_txts/names.txt -p sample_txts/prefixes.txt

    PR Name: Civil Snark
    Branch Name: civil-snark

    # Then you can just run it sans args and get a new name!
    $ python name_gen.py

    PR Name: Pit Worker
    Branch Name: pit-worker

    # To reset your tokens pass in '-r' or '--reset'
    $ python name_gen.py -r
    You're about to reset (decimate) your tokens, dat cool? (y/n) y
    cool

    # just be sure to reload it before you try and generate a name!
    $ python name_gen.py
    Waiting to get fed


Todo:
-----
* use (or make :)) ) POS tagger 
    * this would enable the user to feed text, instead of 'subsets', more advance use could let them  set probabilities of POS distribution in the output.
