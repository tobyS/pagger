# coding=utf-8
import cmd
import readline
import shlex

class Shell (cmd.Cmd):

    _handler = None

    _config = None

    def __init__(self, handler, config):
        cmd.Cmd.__init__(self)
        self._handler = handler
        self._config = config

    def postcmd(self, stop, line):
        return stop

    # 'map' command

    def do_map(self, s):
        params = shlex.split(s)
        
        if len(params) != 2:
            return self._error(u'Expected exactly 2 parameters.')

        from_tag = params[0]
        to_tag = params[1]
        
        if to_tag not in self._config.tags:
            return self._error(u'Tag "' + to_tag + u'" not recognized.')
        
        print u'Established new mapping "' + from_tag + u'" → "' + to_tag + u'"'

    def help_map(self):
        print 'Adds a new tag mapping'

    # 'avail' command

    def do_avail(self, s):
        print u'Available tags'
        print u'--------------'
        for tag in self._config.tags:
            print tag

    def help_avail(self):
        print u'Lists all defined tags'

    # 'tags' command

    def do_tags(self, s):
        print u'Assigned tags'
        print u'-------------'
        for tag in self._handler.get_tags():
            print tag

    def help_tags(self):
        print u'Displays the tags found for the track'

    # 'q' command

    def do_quit(self, s):
        return True

    def help_quit(self):
        print 'Quits the shell. Note that you need to save if changes should not be lost.'

    do_q = do_quit
    help_q = help_quit

    do_EOF = do_quit

    # 'help' command

    def help_help(self):
        print 'Prints available commands. Use "help <command>" to get command help.'

    # misc

    def _error(self, message):
        print u'Error: ' + message
