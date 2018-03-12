import os
import stat
from mako.lookup import TemplateLookup
import zc.buildout


class Recipe:
    """ Buildout recipe for making files out of Mako templates.

    All part options are directly available to the template. In addition, all options from all
    parts listed in the buildout section pluss the options from the buildout
    section itself are available to the templates through parts.<part>.<key>.
    If an eggs option is defined, the egg references are transformed into a
    pkg_resources.WorkingSet object before given to the template.
    """

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.options = options
        self.files = _parse_files_option(options.get('files'))
        directories = _parse_directories_option(
            options.get('directories', buildout["buildout"]["directory"]))
        self.lookup = TemplateLookup(directories=directories)

    def install(self):
        kwargs = dict(self.options)
        kwargs.setdefault('parts', dict(self.buildout))
        for template, target, is_executable in self.files:
            self.options.created(target)
            with open(target, "w") as f:
                f.write(self.lookup.get_template(template).render(**kwargs))
            if is_executable:
                os.chmod(target, os.stat(target).st_mode | stat.S_IEXEC)
        return self.options.created()

    update = install


def _parse_list_values(value):
    items = (i.strip() for i in value.strip().split('\n'))
    items = (i for i in items if i)
    return items


def _parse_directories_option(value):
    directories = (os.path.abspath(i) for i in _parse_list_values(value))
    return list(directories)


def _parse_files_option(value):
    """
    Goals:
        * split input
        * resolve 'target' it to abspath
        * isExecutable?
        * acknowledge overwrites or same template reuse (marker ":overwrite"")

    return [('template', 'target', 'isExecutable'), ]
    """
    sources = set()
    targets = set()
    files = []

    for line in _parse_list_values(value):
        options = tuple(i.strip() for i in line.split(':'))

        if not (1 < len(options) < 5):
            raise zc.buildout.UserError(
                "Malformed file option '{}'\nallowed format is "
                "'source:target[:is_executable(true or false)[:collision_allowed]]'"
                "".format(line)
            )

        source = options[0]
        target = os.path.abspath(options[1])
        is_executable = len(options) > 2 and _to_bool(options[2])
        collision_allowed = len(options) > 3 and options[3] == 'collision_allowed'

        if not collision_allowed and source in sources:
            raise zc.buildout.UserError(
                "Template collision is detected at '{}'".format(line))

        if not collision_allowed and target in targets:
            raise zc.buildout.UserError(
                "Target collision is detected at '{}'".format(line))

        sources.add(source)
        targets.add(target)
        files.append((source, target, is_executable))

    return files


def _to_bool(value):
    return value.lower() in ("yes", "true", "1", "on")
