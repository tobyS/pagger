# coding=utf-8
import cmd
import readline
import shlex

class Shell (cmd.Cmd):

    _config = None

    _mp3 = None

    _tag = None

    _list_commands = [
        u'available',
        u'ignored',
        u'mapping',

        u'assigned',
        u'raw',
        u'mapped',
        u'unmappedu'
    ]

    def __init__(self, config, mp3, tag):
        cmd.Cmd.__init__(self)
        self._config = config
        self._mp3 = mp3
        self._tag = tag

    def precmd(self, line):
        print ''
        return cmd.Cmd.precmd(self, line)

    def postcmd(self, stop, line):
        print ''
        return cmd.Cmd.postcmd(self, stop, line)

    # 'map' command

    def do_map(self, s):
        params = shlex.split(s)
        
        if len(params) != 2:
            return self._error(u'Expected exactly 2 parameters: <from tag> <to tag>.')

        from_tag = params[0]
        to_tag = params[1]
        
        if to_tag not in self._config.tags:
            return self._error(u'Tag "' + to_tag + u'" not recognized. Maybe add it first?')

        self._config.add_mapping(from_tag, to_tag)
        
        print u'Established new mapping "' + from_tag + u'" → "' + to_tag + u'"'

    def help_map(self):
        print 'Adds a new tag mapping'

    # 'add' command

    def do_add(self, s):
        params = shlex.split(s)

        if len(params) != 1:
            return self._error(u'Expected exactly 1 parameter: <genre>.')

        tag = params[0]

        if tag in self._config.tags:
            return self._error(u'Genre "' + tag + u'" already in config.')
        
        self._config.add_tag(tag)

        print u'Added genre "' + tag + u'" to config.'

    def help_add(self):
        print u'Adds a new genre to the configuration.'

    # 'assign' command

    def do_assign(self, s):
        params = shlex.split(s)

        if len(params) != 1:
            return self._error(u'Expected exactly 1 parameter: <tag>.')
        
        tag = params[0]

        if tag not in self._config.tags:
            return self._error(u'Tag "' + tag + u'" not available. Add it first?')

        self._tag.add_tag(tag)

        print u'Tag "' + tag + u'" successfully added.'

    def help_assign(self, s):
        print u'Assign a tag to the song.'

    # 'list' command

    def do_list(self, s):
        params = shlex.split(s)

        if len(params) < 1:
            params.append('assigned')

        command = params[0]

        if command not in self._list_commands:
            return self._error(u'Unknown command "' + command + u'". Available are: ' + u', '.join(self._list_commands))

        getattr(self, u'_print_' + command)()

    def help_list(self):
        print u'List tags/genres. Available sub-commands are: ' + u', '.join(self._list_commands) + u'.'

    def complete_list(self, text, line, begindex, endindex):
        return [i for i in self._list_commands if i.startswith(text)]

    def _print_available(self):
        self._print_heading(u'Available genres')
        for tag in self._config.tags:
            print tag

    def _print_ignored(self):
        self._print_heading(u'Ignored tag matchings')
        for tag in self._config.ignore:
            print tag

    def _print_mapping(self):
        self._print_heading(u'Overall tag mapping')
        for key, val in self._config.tagmap.items():
            print u'{0!s: <10} → {1!s}'.format(key, val)

    def _print_assigned(self):
        self._print_heading(u'Assigned genres')
        for tag in self._tag.get_tags():
            print tag

    def _print_raw(self):
        self._print_heading(u'Assigned tags')
        for tag in self._tag.get_raw_tags():
            print tag

    def _print_mapped(self):
        self._print_heading(u'Currently mapped')
        for key, val in self._tag.get_tag_mapping().items():
            print u'{0!s: <10} → {1!s}'.format(key, val)

    def _print_unmapped(self):
        self._print_heading(u'Not mapped tags')
        for tag in self._tag.get_unmapped_tags():
            print tag

    def _print_heading(self, heading):
        print heading
        print u'-' * len(heading)

    # 'ignore' command

    def do_ignore(self, s):
        params = shlex.split(s)

        if len(params) != 1:
            return self._error(u'Expected exactly 1 parameter: <tag>.')

        tag = params[0]

        self._config.ignore.add(tag)

        print u'Added tag "' + tag + u'" to ignore list.'

    def help_ignore(self):
        print u'Add a tag to the ignore list.'

    # 'q' command

    def do_quit(self, s):
        return True

    def help_quit(self):
        print u'Quits the shell. Note that you need to save if changes should not be lost.'

    do_q = do_quit
    help_q = help_quit

    do_EOF = do_quit

    # 'help' command

    def help_help(self):
        print u'Prints available commands. Use "help <command>" to get command help.'

    # misc

    def _error(self, message):
        print u'Error: ' + message
