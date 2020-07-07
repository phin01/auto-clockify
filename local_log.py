import os
import datetime
import configs


class LocalLog():
    """
        LocalLog will log all changes to a local text file, according to set interval
        No tags will be used, only program name, time and window title
    """

    def __init__(self):
        cfg = configs.AutoClockifyConfig()
        local_log_path = cfg.get_local_log_path()
        if local_log_path:
            self.log_path = local_log_path + "log.txt"
        else:
            self.log_path = os.path.join(os.path.dirname(__file__), "log.txt")


    def create_log_entry(self, win_title: str, program_name: str):
        input_string = "{}|{}|{}\n"
        log_file = open(self.log_path, "a+")
        log_file.write(input_string.format(win_title, program_name, self.get_time()))


    def get_time(self) -> str:
        """ return datetime.now() formatted as a string """
        return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") # time string formatted according to Clockify API requirements






# if __name__ == '__main__':
    # log = LocalLog()
    # log.create_log_entry("eita\dfdffz\fdsfs", "aaaa")