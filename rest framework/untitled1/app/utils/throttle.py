# author navigator
import time


class FreqView():
    def allow_request(self,request,view):
        remote_addr = request.META.get('REMOTE_ADDR')
        print(remote_addr)
        return True

    def wait(self):

        return 10