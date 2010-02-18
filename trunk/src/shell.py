# coding=utf-8
import cmd
import readline
import shlex

class Shell (cmd.Cmd):

    _config = None

    _mp3 = None

    _tag = None

    def __init__(self, config, mp3, tag):
        cmd.Cmd.__init__(self)
        self._config = config
        self._mp3 = mp3
        self._tag = tag
        self._list_command = ListCommand(self)

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
        self._list_command.do_list(s)

    def help_list(self):
        self._list_command.help_list()

    def complete_list(self, text, line, begindex, endindex):
        self._list_command.complete_list(text, line, begindex, endindex)

    # def _generate_tables(self, heading, content):
    #     max_len = reduce(max, map(len, content))

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
        print u'Prints available commands. Use "help <command>" to get command help.\n'

    # misc

    def _error(self, message):
        print u'Error: ' + message

class ListCommand:

    _shell = None

    def __init__(self, shell):
        self._shell = shell

    _list_commands = {
        u'available': lambda self: self._generate_table(
            u'Available genres',
            self._shell._config.tags
        ),
        u'ignored': lambda self: self._generate_table(
            u'Ignored tag matchings',
            self._shell._config.ignore
        ),
        u'mapping': lambda self: self._generate_mapping_table(
            u'Overall tag mapping',
            dict(filter(self._filter_mapping, self._shell._config.tagmap.items()))
        ),
        u'assigned': lambda self: self._generate_table(
            u'Assigned genres',
            self._shell._tag.get_tags()
        ),
        u'raw': lambda self: self._generate_table(
            u'Assigned tags',
            self._shell._tag.get_raw_tags()
        ),
        u'mapped': lambda self: self._generate_mapping_table(
            u'Currently mapped',
            self._shell._tag.get_tag_mapping()
        ),
        u'unmapped': lambda self: self._generate_table(
            u'Not mapped tags',
            self._shell._tag.get_unmapped_tags()
        )
    }

    def do_list(self, s):
        params = shlex.split(s)

        if len(params) < 1:
            params.append('assigned')

        command = params[0]

        if not self._list_commands.has_key(command):
            raise CommandNotFound(
                u'Unknown command "' + command + u'". Available are: ' + self._available_commands()
            )

        print self._list_commands[command](self)

    def help_list(self):
        print u'List tags/genres. Available sub-commands are: ' + self._available_commands() + u'.'

    def complete_list(self, text, line, begindex, endindex):
        return [i for i in self._list_commands.keys() if i.startswith(text)]

    def _filter_mapping(self, tup):
        return tup[0].lower() != tup[1].lower()

    def _available_commands(self):
        return u', '.join(self._list_commands.keys())

    def _generate_heading(self, heading):
        return heading + u"\n" + u'-' * len(heading) + u"\n"

    def _generate_table(self, heading, content):
        res = self._generate_heading(heading) + "\n"
        for val in content:
            res += val + "\n"
        return res

    def _generate_mapping_table(self, heading, mapping):
        max_len = reduce(
            max,
            map(
                len,
                mapping.keys()
            )
        )

        return self._generate_table(
            heading,
            map(
                lambda x: u'{0!s: <{1}} → {2!s}'.format(x[0], max_len, x[1]),
                mapping.items()
            )
        )

class CommandNotFound (Exception):
    pass
