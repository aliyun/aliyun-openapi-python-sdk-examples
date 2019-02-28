#encoding=utf-8
import json
import time

class CheckStatus:
    @staticmethod
    def check_status(time_default_out, default_time, func, check_status, id):
        for i in range(time_default_out):
            time.sleep(default_time)
            status = func(id)
            if (status == check_status):
                return True
        return False

