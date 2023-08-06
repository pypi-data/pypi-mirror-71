import os

from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from .utils import flatten
from . import markdown as md


class AddNumberPlugin(BasePlugin):
    config_scheme = (
        ('strict_mode', config_options.Type(bool, default=False)),
        ('increment_pages', config_options.Type(bool, default=False)),
        ('increment_topnav', config_options.Type(bool, default=False)),
        ('excludes', config_options.Type(list, default=[])),
        ('includes', config_options.Type(list, default=[])),
        ('order', config_options.Type(int, default=1))
    )

    def _check_config_params(self):
        set_parameters = self.config.keys()
        allowed_parameters = dict(self.config_scheme).keys()
        if set_parameters != allowed_parameters:
            unknown_parameters = [x for x in set_parameters if
                                  x not in allowed_parameters]
            raise AssertionError(
                "Unknown parameter(s) set: %s" % ", ".join(unknown_parameters))

    def on_nav(self, nav, config, files):
        """
        The nav event is called after the site navigation is created and
        can be used to alter the site navigation.

        See:
        https://www.mkdocs.org/user-guide/plugins/#on_nav

        :param nav:     global navigation object
        :param config:  global configuration object
        :param files:   global files collection
        :return:        global navigation object
        """
        self._title2index = dict()
        is_increment_topnav = self.config.get("increment_topnav", False)
        is_increment_pages = self.config.get("increment_pages", False)

        index = 0
        while index < len(nav.items):
            if is_increment_topnav:
                nav.items[index].title = str(index + 1) + '. ' + \
                                         nav.items[index].title
            # Section(title='Linux')
            #       Page(title=[blank], url='/linux/epel%E6%BA%90/')
            if type(nav.items[index]) == Section:
                pages = nav.items[index].children
                j = 0
                while j < len(pages):
                    if is_increment_topnav and is_increment_pages:
                        self._title2index[pages[j].url] = \
                            str(index + 1) + '.' + str(j + 1) + ' '
                    elif is_increment_pages:
                        self._title2index[pages[j].url] = str(j + 1) + '. '
                    j += 1
            index += 1
        return nav

    def on_files(self, files, config):
        """
        The files event is called after the files collection is populated from the docs_dir. 
        Use this event to add, remove, or alter files in the collection.
        
        See https://www.mkdocs.org/user-guide/plugins/#on_files
        
        Args:
            files (list): files: global files collection
            config (dict): global configuration object
            
        Returns:
            files (list): global files collection
        """
        self._check_config_params()

        # Use navigation if set, 
        # (see https://www.mkdocs.org/user-guide/configuration/#nav)
        # only these files will be displayed.
        nav = config.get('nav', None)
        if nav:
            files_str = flatten(nav)
        # Otherwise, take all source markdown pages
        else:
            files_str = [
                file.src_path for file in files if file.is_documentation_page()
                ]

        # Record excluded files from selection by user
        self._excludes = self.config['excludes']
        self._exclude_files = [os.path.normpath(file1) for file1 in
                               self._excludes if not file1.endswith('\\')
                               and not file1.endswith('/')]
        self._exclude_dirs = [os.path.normpath(dir1) for dir1 in self._excludes
                              if dir1.endswith('\\')
                              or dir1.endswith('/')]

        self._includes = self.config['includes']
        self._include_files = [os.path.normpath(file1) for file1 in
                               self._includes if not file1.endswith('\\')
                               and not file1.endswith('/')]
        self._include_dirs = [os.path.normpath(dir1) for dir1 in self._includes
                              if dir1.endswith('\\')
                              or dir1.endswith('/')]

        self._order = self.config['order'] - 1

        # Remove files excluded from selection by user
        files_to_remove = [file for file in files_str if
                           self._is_exclude(file) and not self._is_include(
                               file)]
        self.files_str = [file for file in files_str if
                          file not in files_to_remove]

        return files

    def on_page_markdown(self, markdown, page, config, files):
        """
        The page_markdown event is called after the page's markdown is loaded 
        from file and can be used to alter the Markdown source text. 
        The meta- data has been stripped off and is available as page.meta 
        at this point.
        
        See:
        https://www.mkdocs.org/user-guide/plugins/#on_page_markdown
        
        Args:
            markdown (str): Markdown source text of page as string
            page (Page): mkdocs.nav.Page instance
            config (dict): global configuration object
            files (list): global files collection
        
        Returns:
            markdown (str): Markdown source text of page as string
        """
        if self.config.get('increment_pages', False):
            index_str = self._title2index.get(page.url, None)
            if index_str:
                page.title = index_str + page.title

        if page.file.src_path not in self.files_str:
            return markdown

        lines = markdown.split('\n')
        heading_lines = md.headings(lines)

        if len(heading_lines) <= self._order:
            return markdown

        tmp_lines_values = list(heading_lines.values())

        if self.config['strict_mode']:
            tmp_lines_values, _ = self._searchN(tmp_lines_values, 1,
                                                self._order, 1, [])
        else:
            tmp_lines_values = self._ascent(tmp_lines_values, [0], 0, [], 1,
                                            self._order)

        # replace the links of current page after numbering the titles
        def _format_link_line(line):
            line = line.replace(".", "")
            new_line = ''
            for s in line:
                if s.isdigit() or s in (" ", "_") \
                        or (u'\u0041' <= s <= u'\u005a') \
                        or (u'\u0061' <= s <= u'\u007a'):
                    new_line += s.lower()
            return '#' + '-'.join(new_line.split())

        link_lines = [_format_link_line(v) for v in tmp_lines_values]
        link_lines = {'#' + i.split("-", 1)[1]: i for i in link_lines
                      if i.count('-') > 0}
        n = 0
        while n < len(lines):
            for k in link_lines.keys():
                line_content = lines[n]
                if line_content.count('[') >= 1 \
                        and line_content.count('(') >= 1:
                    lines[n] = line_content.replace(k, link_lines[k])
            n += 1

        # replace these new titles
        n = 0
        for key in heading_lines.keys():
            lines[key] = tmp_lines_values[n]
            n += 1

        return '\n'.join(lines)

    def _ascent(self, tmp_lines, parent_nums_head, level, args, num, startrow):
        """
        Add number to every line.

        e.g.
        if number from h2, then the level is:
        ## level=1
        ### level=2
        #### level=3
        ### level=2

         args
        |...|
        v   v
        ######
             ^
             |
            num

        :param tmp_lines: line
        :param parent_nums_head: storage depth of header before this line.
        :param level: level of header
        :param args: all of numbers to combine the number
        :param num: the last number
        :param startrow: start row to deal
        :return: lines which has been numbered
        """
        if startrow == len(tmp_lines):
            return tmp_lines

        nums_head = md.heading_depth(tmp_lines[startrow])
        parent_nums = parent_nums_head[len(parent_nums_head) - 1]
        chang_num = nums_head - parent_nums

        # drop one level
        if chang_num < 0:
            if level != 1:
                # for _ in range(-chang_num):
                num = args.pop()
            level -= 1
            parent_nums_head.pop()
            return self._ascent(tmp_lines, parent_nums_head, level, args, num,
                                startrow)

        # sibling
        if chang_num == 0:
            num += 1
            tmp_lines[startrow] = self._replace_line(tmp_lines[startrow],
                                                     '#' * nums_head + ' ',
                                                     '%d.' * len(args) % tuple(
                                                         args), num)
            return self._ascent(tmp_lines, parent_nums_head, level, args, num,
                                startrow + 1)

        # rise one level
        level += 1
        if level != 1:
            # for _ in range(chang_num):
            args.append(num)
        parent_nums_head.append(nums_head)
        num = 1
        tmp_lines[startrow] = self._replace_line(tmp_lines[startrow],
                                                 '#' * nums_head + ' ',
                                                 '%d.' * len(args) % tuple(
                                                     args), num)
        return self._ascent(tmp_lines, parent_nums_head, level, args, num,
                            startrow + 1)

    def _replace_line(self, tmp_line, substr, prenum_str, nextnum):
        re_str = (substr + "%d. " % nextnum) if (prenum_str == '') else (
        substr + "%s%d " % (prenum_str, nextnum))
        tmp_line = tmp_line.replace(substr, re_str)
        return tmp_line

    def _searchN(self, tmp_lines, num, start_row, level, args):
        while True:
            tmp_lines, start_row, re = self._replace(tmp_lines,
                                                     '#' * level + ' ',
                                                     '.'.join(('%d.' * (
                                                     level - 1)).split()) % tuple(
                                                         args),
                                                     num, start_row)
            if not re:
                break

            next_num = 1
            if level != 6:
                args.append(num)
                re_lines, start_row = self._searchN(tmp_lines, next_num,
                                                    start_row, level + 1, args)
                args.pop()

            num += 1

        return tmp_lines, start_row

    def _replace(self, tmp_lines, substr, prenum_str, nextnum, start_row):
        if start_row == len(tmp_lines) or not tmp_lines[start_row].startswith(
                substr):
            return tmp_lines, start_row, False

        re_str = (substr + "%d. " % nextnum) if (prenum_str == '') else (
        substr + "%s%d " % (prenum_str, nextnum))
        tmp_lines[start_row] = tmp_lines[start_row].replace(substr, re_str)
        return tmp_lines, start_row + 1, True

    def _is_exclude(self, file):
        if len(self._excludes) == 0:
            return False

        url = os.path.normpath(file)

        if url in self._exclude_files or '*' in self._exclude_files:
            return True

        for dir1 in self._exclude_dirs:
            if url.find(dir1) != -1:
                return True

        return False

    def _is_include(self, file):
        if len(self._includes) == 0:
            return False

        url = os.path.normpath(file)

        if url in self._include_files:
            return True

        for dir1 in self._include_dirs:
            if url.find(dir1) != -1:
                return True

        return False
