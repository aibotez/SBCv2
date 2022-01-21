from django.http import StreamingHttpResponse,FileResponse
from django.utils.encoding import escape_uri_path
import os

class FileDU():
    def __init__(self):
        pass

    def file_iterator(self,file_name, chunk_size=20 * 1024 * 1024):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def Down(self,FileInfo):

        the_file_name = FileInfo['fename']
        the_file_path = FileInfo['fepath']
        # print(the_file_name,the_file_path)
        #response = FileResponse(file_iterator(the_file_name))
        response = StreamingHttpResponse(self.file_iterator(the_file_path))
        response = FileResponse(response)
        response['Content-Type'] = 'application/octet-stream'
        response['content-length'] = os.path.getsize(the_file_path)
        #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(wjname)
        response["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(escape_uri_path(the_file_name))
        return response