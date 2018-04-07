from datetime import datetime


class Task():
    def __init__(self, dictionary):
        self.id = dictionary['id']
        self.model_id = dictionary['model_id']
        self.session_id = dictionary['session_id']

        # Execution definition
        self.command = dictionary['command']

        # Pre-Execution
        self.before_snapshot_id = dictionary.get('before_snapshot_id', "")
        self.ports = dictionary.get('ports', [])
        self.gpu = dictionary.get('gpu', False)
        self.interactive = dictionary.get('interactive', False)
        self.task_dirpath = dictionary.get('task_dirpath', "")
        self.log_filepath = dictionary.get('log_filepath', "")

        # Post-Execution
        self.after_snapshot_id = dictionary.get('after_snapshot_id', "")
        self.hardware_info = dictionary.get('hardware_info', "")
        self.container_id = dictionary.get('container_id', "")
        self.logs = dictionary.get('logs', "")
        self.status = dictionary.get('status', "")

        self.created_at = dictionary.get('created_at', datetime.utcnow())
        self.updated_at = dictionary.get('updated_at', self.created_at)

    def __eq__(self, other):
        return self.id == other.id if other else False

    def toDictionary(self):
        attr_dict = self.__dict__
        pruned_attr_dict = { attr: val
                    for attr, val in attr_dict.items() if not callable(getattr(self, attr)) and not attr.startswith("__")
        }
        return pruned_attr_dict