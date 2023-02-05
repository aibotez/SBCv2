from SBC import GetUserPath
import os

class FileSycManager():
    def __init__(self):
        self.getuserpath = GetUserPath.GetUserPath()

    def checkFile(self,fileinfo):
        feMd5 = fileinfo['LoMD5']
        RoFilePath = fileinfo['RoFilePath']
        RoFileFaPath = fileinfo['RoFileFaPath']
        FileName = fileinfo['FileName']
        useremail = fileinfo['useremail']
        dst = self.getuserpath.getuserserpath(useremail,RoFileFaPath)
        if os.path.exists(dst+'/'+FileName):
            FileCheck = {
            'exist': 0,
            # 'FileStart': FileStart
            }

    def UpFile(self,fileinfo):
        feMd5 = fileinfo['LoMD5']
        RoFilePath = fileinfo['RoFilePath']
        RoFileFaPath = fileinfo['RoFileFaPath']
        FileName = fileinfo['FileName']


        # feMd5 = redit['LoMD5']
        # userpath = redit['CurPath']
        # with open(self.FilesStock + feMd5, "ab") as f:
        #     # f.seek(0,2)
        #     for chunk in file_obj.chunks(chunk_size=2 * 1024 * 1024):
        #         f.write(chunk)
        # if os.path.getsize(self.FilesStock + feMd5) == redit['FileSize']:
        #     if feMd5 == self.GetFileMd5(self.FilesStock + feMd5):
        #         if os.path.exists(self.FilesStock + redit['FileName']):
        #             os.remove(self.FilesStock + redit['FileName'])
        #         os.rename(self.FilesStock + feMd5, self.FilesStock + redit['FileName'])
        #         dst = self.getuserpath.getuserserpath(useremail, userpath)
        #         if not os.path.isdir(dst):
        #             os.makedirs(dst)
        #         dstfename = redit['FileName']
        #         srcfename = redit['FileName']
        #         lk = MakeLink()
        #         lk.mklk(dst, srcfename, dstfename)
        #         models.FilesStock.objects.create(FileMd5=feMd5, FileName=srcfename,
        #                                          FilePath=self.FilesStock + srcfename)
        #         usermange = UserManage.usermange()
        #         usermange.AddUsedCap(useremail, os.path.getsize(self.FilesStock + redit['FileName']))
        #
        #         dstuserpath = userpath + redit['FileName']
        #         userfilerecordmanage = UserFileRecordManage.userfilerecordmanage()
        #         userfilerecordmanage.AddNewRecord(useremail, dstuserpath, feMd5)