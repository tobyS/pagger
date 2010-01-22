======
pagger
======

Pagger is a command line tool to semi-automatically tag MP3 files with proper
genres.

Assigning proper genre information to MP3 files is not easy. First of, you
don't want to perform such a task by hand on large music collections. This is
cumbersome and most propably will result in very inconsistent mapping. Second
you might not be able to determine proper genre information for every song just
by looking at artist and title. Pagger tries to solve both problems for you, at
least to a certain degree.

Pagger runs on a directory of MP3 files. For each file, it requests the most
popular tags assigned to the song (and propably artist) on `Last.fm`__. In the
pagger config file, you define which genres you'd like to have at all in your
MP3s. In addition you can define a mapping from Last.fm tags to proper genre
names. Pagger will check these settings and see if it can determine proper
genres from this information. If it can, it simply assignes the genre to the
file and saves it. Otherwise it will enter an interactive shell mode, where you
can analyze the tags found (if any), define new tags and mappings, as well as
manually assigne genres to the file.

For help on commands in the shell, simply type "help" or "help <command>" for
further details.

__ http://last.fm

Pagger is my first little project in Python, so please bear with me. Comments,
critics and patches always welcome. :)
