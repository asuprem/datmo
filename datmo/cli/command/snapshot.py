from __future__ import print_function

import prettytable

from datmo.util.i18n import get as _
from datmo.cli.command.project import ProjectCommand
from datmo.controller.snapshot import SnapshotController
from datmo.util.exceptions import ProjectNotInitializedException


class SnapshotCommand(ProjectCommand):
    def __init__(self, home, cli_helper):
        super(SnapshotCommand, self).__init__(home, cli_helper)
        # dest="subcommand" argument will populate a "subcommand" property with the subparsers name
        # example  "subcommand"="create"  or "subcommand"="ls"
        snapshot_parser = self.subparsers.add_parser("snapshot", help="Snapshot module")
        subcommand_parsers = snapshot_parser.add_subparsers(title="subcommands", dest="subcommand")

        create = subcommand_parsers.add_parser("create", help="Create snapshot")
        create.add_argument("--message", "-m", dest="message", default="", help="Message to describe snapshot")
        create.add_argument("--label", "-l", dest="label", default="",
                            help="Label snapshots with a category (e.g. best)")
        create.add_argument("--session-id", dest="session_id", default="", help="User given session id")

        create.add_argument("--task-id", dest="task_id", default="",
                            help="Specify task id to pull information from")

        create.add_argument("--code-id", dest="code_id", default="",
                            help="User provided code id (e.g. git revision for git)")

        create.add_argument("--environment-def-path", dest="environment_def_path", default="",
                            help="Absolute filepath to environment definition file (e.g. /path/to/Dockerfile)")

        create.add_argument("--config-filename", dest="config_filename", default="",
                            help="Filename to use to search for configuration JSON")
        create.add_argument("--config-filepath", dest="config_filepath", default="",
                            help="Absolute filepath to use to search for configuration JSON")

        create.add_argument("--stats-filename", dest="stats_filename", default="",
                            help="Filename to use to search for metrics JSON")
        create.add_argument("--stats-filepath", dest="stats_filepath", default="",
                            help="Absolute filepath to use to search for metrics JSON")

        create.add_argument("--filepaths", dest="filepaths", default=[], nargs="*",
                            help="Absolute paths to files or folders to include within the files of the snapshot")

        create.add_argument("--not-visible", dest="visible", action="store_false",
                         help="Boolean if you want snapshot to not be visible")

        delete = subcommand_parsers.add_parser("delete", help="Delete a snapshot by id")
        delete.add_argument("--id", dest="id", help="snapshot id to delete")

        ls = subcommand_parsers.add_parser("ls", help="List snapshots")
        ls.add_argument("--session-id", dest="session_id", default=None, help="Session ID to filter")
        ls.add_argument("--session-name", dest="session_name", default=None, help="Session name to filter")
        ls.add_argument("-a", dest="details", default=True, help="Show detailed SnapshotCommand information")

        checkout = subcommand_parsers.add_parser("checkout", help="Checkout a snapshot by id")
        checkout.add_argument("--id", dest="id", default=None, help="SnapshotCommand ID")

        self.snapshot_controller = SnapshotController(home=home,
                                                      dal_driver=self.project_controller.dal_driver)
        if not self.project_controller.is_initialized:
            raise ProjectNotInitializedException(_("error",
                                                   "cli.project",
                                                   self.home))

    def create(self, **kwargs):
        self.cli_helper.echo(_("info", "cli.snapshot.create"))

        def mutually_exclusive(dictionary, mutually_exclusive_args):
            for arg in mutually_exclusive_args:
                if arg in kwargs and kwargs[arg]:
                    snapshot_dict[arg] = kwargs[arg]
                    break
            return dictionary

        snapshot_dict = {}

        # Code
        mutually_exclusive_args = ["code_id", "commit_id"]
        snapshot_dict = mutually_exclusive(snapshot_dict, mutually_exclusive_args)

        # Environment
        mutually_exclusive_args = ["environment_id", "environment_definition_filepath"]
        snapshot_dict = mutually_exclusive(snapshot_dict, mutually_exclusive_args)

        # File
        mutually_exclusive_args = ["file_collection_id", "file_collection"]
        snapshot_dict = mutually_exclusive(snapshot_dict, mutually_exclusive_args)

        optional_args = ["config_filepath", "config_filepath", "config_filename", "config_filename", "session_id",
                         "task_id", "message", "label", "visible"]

        for arg in optional_args:
            if arg in kwargs and kwargs[arg]:
                snapshot_dict[arg] = kwargs[arg]

        snapshot_obj = self.snapshot_controller.create(snapshot_dict)

        return snapshot_obj.id

    def delete(self, **kwargs):
        self.cli_helper.echo(_("info", "cli.snapshot.delete"))
        id = kwargs.get("id", None)
        return self.snapshot_controller.delete(id)

    def ls(self, **kwargs):
        session_id = kwargs.get('session_id',
                                self.snapshot_controller.current_session.id)
        # Get all snapshot meta information
        header_list = ["id", "config", "stats", "message", "label", "created at"]
        t = prettytable.PrettyTable(header_list)
        snapshot_objs = self.snapshot_controller.list(session_id)
        for snapshot_obj in snapshot_objs:
            t.add_row([snapshot_obj.id, snapshot_obj.config, snapshot_obj.stats,
                       snapshot_obj.message, snapshot_obj.label,
                       snapshot_obj.created_at.strftime("%Y-%m-%d %H:%M:%S")])
        self.cli_helper.echo(t)
        return True

    def checkout(self, **kwargs):
        id = kwargs.get("id", None)
        return self.snapshot_controller.checkout(id)







