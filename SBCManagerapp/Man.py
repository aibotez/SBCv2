import os

from SBCManagerapp import models as SBCManagemodels
from Usersapp.models import User
from UserFileRecordapp.models import UserFileRecord
from FileDownUpapp.models import FilesStock
from pack import CommMode
import json,psutil,time
from SBC import GetUserPath
from django.db.models import Q
from SBC import UserManage
from pySMART import Device

# from win32com.client import GetObject,Dispatch
#
#
#
# wmi = GetObject('winmgmts:/root/cimv2')
# # 创建 SWbemRefresher 刷新器对象
# objRefresher = Dispatch('WbemScripting.SWbemRefresher')
# # 使用从 Win32_PerfFormattedData派生的预计算数据类 Win32_PerfFormattedData_Tcpip_Networkinterface
# # 要注意的是调用了AddEnum之后需要再调用objRefresher.Refresh()来获取初始性能数据，下方因为在循环开头已经做了这步了所以跳过。
# NetInterfaces = objRefresher.AddEnum(wmi,"Win32_PerfFormattedData_Tcpip_Networkinterface")
class Manage():
    def __init__(self):
        self.ComTol = CommMode.ComTol()

    def disksinfoall(self):
        values = []
        disk_partitions = psutil.disk_partitions(all=False)
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                device = {'device': partition.device,
                          'mountpoint': partition.mountpoint,
                          'fstype': partition.fstype,
                          'opts': partition.opts,
                          'total': usage.total,
                          'used': usage.used,
                          'free': usage.free,
                          'percent': usage.percent
                          }
                values.append(device)
            except:
                continue
        values = sorted(values, key=lambda device: device['device'])
        return values
    def GetDiskSMART(self,devicePar):
        # sda = Device(devicePar)
        # atrs0 = sda.attributes
        # atrs = [i for i in atrs0 if i]
        SMARTattrs = []
        SMARToverallhealth = ''
        DeviceModel = ''
        SerialNumber = ''
        RotationRate = ''
        SATAVersion = ''
        Titles = ''
        Power_On_Hours = ''
        Power_Cycle_Count = ''
        DeviceId = ''
        DiskState = '欠佳'
        FirmwareVersion = ''
        r = os.popen('smartctl -a {}'.format(devicePar))
        content = r.read()
        for line in content.split('\n'):
            Vaule = line.split(' ')[-1].replace('\n','')
            if 'Device Model:' in line:
                DeviceModel = Vaule
            elif 'Serial Number:' in line:
                SerialNumber = Vaule
            elif 'Rotation Rate:' in line:
                RotationRate = line.split(' ')[-2]+' '+Vaule
            elif 'Firmware Version:' in line:
                FirmwareVersion = Vaule
            elif 'Device Id:' in line:
                DeviceId = Vaule
            elif 'SATA Version is:' in line:
                SATAVersion = line.split('SATA Version is:  ')[-1].replace('\n','')
            elif 'SMART overall-health self-assessment test result:' in line:
                SMARToverallhealth = Vaule
                if 'pass' in Vaule.lower():
                    SMARToverallhealth = 'PASS'
                    DiskState = '良好'
            elif 'ATTRIBUTE_NAME' in line:
                Titles = line.split(' ')
            elif 'Pre-fail' in line or 'Old_age' in line:
                SMARTattrs.append(line.split(' '))
                if 'Power_On_Hours' in line:
                    Power_On_Hours = Vaule
                elif 'Power_Cycle_Count' in line:
                    Power_Cycle_Count = Vaule
        SMARTInfo = {'SMARToverallhealth':SMARToverallhealth,'DeviceModel':DeviceModel,'SerialNumber':SerialNumber,
                     'RotationRate':RotationRate,'SATAVersion':SATAVersion,'Titles':Titles,'SMARTattrs':SMARTattrs,
                     'Power_Cycle_Count':Power_Cycle_Count,'Power_On_Hours':Power_On_Hours,'DeviceId':DeviceId,
                     'DiskState':DiskState,'FirmwareVersion':FirmwareVersion}
        sda = Device(devicePar)
        Temp = sda.temperature
        SMARTInfo['Temp'] = Temp

        ATTRIBUTE = content.split('Vendor Specific SMART Attributes with Thresholds:')[-1].split('SMART Error Log Version')[0]
        ATTRIBUTE.replace('ATTRIBUTE_NAME','属性名称').replace('VALUE','当前值').replace('WORST','历史最差值').replace('THRESH','临界值').replace('WHEN_FAILED RAW_VALUE','原始数据')
        attr = ATTRIBUTE.split('\n')
        attrs = [i for i in attr if i]
        attrlist = []
        for i in attrs:
            lt = i.split(' ')
            lst = [j for j in lt if j]
            attrlist.append(lst)
        del attrlist[0]
        SMARTInfo['ATTRIBUTE'] = attrlist
        return SMARTInfo

    def ModSBCstock(self,stock):
        stock = stock+'/'
        Info = SBCManagemodels.SBCManager.objects.all()
        if Info:
            info = Info[0]
            info.FileStock = stock.replace('//','/')
            info.save()
            self.InitSerPath()
            return {}
        else:
            SBCManagemodels.SBCManager.objects.creat(FileStock = stock,UserStock = '',SBCStockSize=0,SBCUser0 = 'SBC',
                                                     SBCUserPass0='12',SBCManageEmail = '',par1='',par2='',par3='')
        self.InitSerPath()
        return 1

    # {'device': 'E:\\', 'mountpoint': 'E:\\', 'fstype': 'NTFS', 'opts': 'rw,fixed', 'total': 285616369664,
    #  'used': 245613334528, 'free': 40003035136, 'percent': 86.0}

    def GetDiskParinfo(self):
        disksinfoall = self.disksinfoall()
        DiskInfos = []
        for i in disksinfoall:
            devicePar = i['device'].replace('\\', '/')
            DiskSize = {'total': self.ComTol.size_format(i['total']), 'used': self.ComTol.size_format(i['used']),
                        'percent': i['percent']}
            DiskInfos.append({'Device': devicePar, 'DiskSize': DiskSize})
        return DiskInfos
    def GetDiskInfo(self,idx = None):
        disksinfoall = self.disksinfoall()
        if idx:
            diskinfo = self.GetSerInfo()
            SBCstockpath = diskinfo['FileStock']
            for i in disksinfoall:
                if SBCstockpath in i['mountpoint'].replace('\\','/')+'/':
                    devicePar = i['device'].replace('\\','/')
                    DiskSMARTInfo = self.GetDiskSMART(devicePar)
                    DiskSize = {'total':self.ComTol.size_format(i['total']),'used':self.ComTol.size_format(i['used']),'percent':i['percent']}
                    return {'DiskSMARTInfo':DiskSMARTInfo,'DiskSize':DiskSize}
        else:
            DiskInfos = []
            for i in disksinfoall:
                devicePar = i['device'].replace('\\', '/')
                DiskSMARTInfo = self.GetDiskSMART(devicePar)
                DiskSize = {'total': self.ComTol.size_format(i['total']), 'used': self.ComTol.size_format(i['used']),
                            'percent': i['percent']}
                DiskInfos.append({'DiskSMARTInfo': DiskSMARTInfo, 'DiskSize': DiskSize})

            return DiskInfos



    def get_net_speed(self,interval):
        '''
        输入间隔数，得到间隔数内网卡的流量
        :param interval: 间隔数
        :return:时间戳 间隔数内的发送字节 间隔数内的接收字节
        '''
        net_msg = psutil.net_io_counters()
        bytes_sent, bytes_recv = net_msg.bytes_sent, net_msg.bytes_recv
        time.sleep(interval)
        time1 = int(time.time())
        net_msg = psutil.net_io_counters()
        bytes_sent2, bytes_recv2 = net_msg.bytes_sent, net_msg.bytes_recv
        bytes_sent3 = bytes_sent2 - bytes_sent
        bytes_recv3 = bytes_recv2 - bytes_recv
        return [bytes_recv3,bytes_sent3]
    # def GetSpeed(self):
    #     UpSpeed = 0
    #     DownSpeed = 0
    #     objRefresher.Refresh()
    #     # 循环访问刷新器集合对象
    #     for NetInterface in NetInterfaces.ObjectSet:
    #         UpSpeed += int(NetInterface.BytesSentPersec)
    #         DownSpeed += int(NetInterface.BytesReceivedPersec)
        #
        # units = ['B/s','KB/s','MB/s','GB/s']
        # j = 0
        # while True:
        #     UpSpeed /= 1024
        #     DownSpeed /= 1024
        #     if UpSpeed <1 and DownSpeed <1:
        #         UpSpeed *= 1024
        #         DownSpeed *= 1024
        #         unit = units[j]
        #         break
        #     j += 1
        # return [DownSpeed,UpSpeed]
    def GetSerInfos(self,disk = None):
        mem = psutil.virtual_memory()
        MemTotal = mem.total
        MemUsed = mem.used
        MemPercent = mem.percent
        cpu_percent = psutil.cpu_percent()
        cpu_counts_logi = psutil.cpu_count()
        cpu_counts_phs = psutil.cpu_count(logical=False)
        # psutil.disk_usage('/')
        diskpars = []
        for i in psutil.disk_partitions():
            mount = psutil.disk_usage(i.mountpoint)
            par = i.mountpoint.replace('\\','/')+'/'
            if disk:
                diskinfo = self.GetSerInfo()
                disk = diskinfo['FileStock']
                if disk in par:
                    diskpars.append({'parinfo': i.mountpoint.replace('\\', '/'),
                                     'parsizetotal': self.ComTol.size_format(mount.total),
                                     'parsizeused': self.ComTol.size_format(mount.used),
                                     'parper': mount.percent})
            else:
                diskpars.append({'parinfo':i.mountpoint.replace('\\','/'),'parsizetotal':self.ComTol.size_format(mount.total),'parsizeused':self.ComTol.size_format(mount.used),
                        'parper':mount. percent})
        SerInfos = {}
        SerInfos['Mem'] = {'MemTotal':self.ComTol.size_format(MemTotal),'MemUsed':self.ComTol.size_format(MemUsed),'MemPercent':MemPercent}
        SerInfos['Cpu'] = {'cpu_counts_phs':cpu_counts_phs,'cpu_counts_logi':cpu_counts_logi,'cpu_percent':cpu_percent}
        SerInfos['Disk'] = {'diskpars':diskpars}
        SerInfos['Net'] = self.get_net_speed(0.5)
        return SerInfos


    def DelStockFiles(self,req):
        info = json.loads(req.body)
        Files = info['Files']
        Serinfo = self.GetSerInfo()
        getuserpath = GetUserPath.GetUserPath()
        usermange = UserManage.usermange()
        for i in Files:
            Path = Serinfo['FileStock'] + i['MD5'] + '#' + i['FileName']
            if 'linkuser' in i:
                AllUserFIles = UserFileRecord.objects.filter(FileMd5 = i['MD5'])
                for va in AllUserFIles.values():
                    info = va
                    path = info['FilePath']
                    useremail = info['useremail']
                    userPath = getuserpath.getuserserpath(useremail, path)
                    DirsSize = os.path.getsize(userPath)
                    os.remove(userPath)
                    usermange.DelUsedCap(useremail, DirsSize)
                    os.remove(userPath)
            try:
                os.remove(Path)
            except:
                pass





    def GetFilesAll(self):
        AllUserFIles = UserFileRecord.objects.all()
        AllStockFiles = FilesStock.objects.all()
        # allstockFiles = [{'MD5':i.FileMd5,'FileName':i.FileName,'FilePath':i.FilePath} for i in AllStockFiles]
        # alluserFiles = [{'MD5':i.FileMd5,'FileName':i.FileName,'FileType':i.FileType,'UserEmail':i.useremail,'FileSize':i.FileSize} for i in AllUserFIles]

        alluserFiles = {}
        for i in AllUserFIles:
            alluserFiles[i.FileMd5] = {'MD5':i.FileMd5,'FileType':i.FileType,'UserEmail':i.useremail,'FileSize':i.FileSize}
        FileNoUser = []
        allstockFiles = []
        for i in AllStockFiles:
            FileName = i.FileName.replace(i.FileMd5+'#','')
            info0 = None
            info1 = None
            if i.FileMd5 in alluserFiles:
                info0 = {'linkuser':alluserFiles[i.FileMd5],'MD5':i.FileMd5,'FileName':FileName,'FileType':alluserFiles[i.FileMd5]['FileType'],'FileSize':alluserFiles[i.FileMd5]['FileSize'],'FileSizestr':self.ComTol.size_format(alluserFiles[i.FileMd5]['FileSize'])}
            else:
                if os.path.exists(i.FilePath):
                    FileSize = os.path.getsize(i.FilePath)
                    info1 = {'MD5': i.FileMd5, 'FileName': FileName, 'FileType': self.ComTol.GetImgConPath(i.FilePath), 'FileSize': FileSize,'FileSizestr':self.ComTol.size_format(FileSize)}
                else:
                    info1 = {'MD5': i.FileMd5, 'FileName': FileName, 'FileType': 'O',
                            'FileSize':-1, 'FileSizestr': '-1'}
                    # info = {}
                info0 = info1
                FileNoUser.append(info1)
            allstockFiles.append(info0)
        for i in allstockFiles:
            if 'time2' in i['FileName']:
                print('ALL:',i)
        for i in FileNoUser:
            if 'time2' in i['FileName']:
                print('FileNoUser:',i)
        return {'all':allstockFiles,'NoUser':FileNoUser}

    def InitSerPath(self):
        FileUsersPath = ''
        FileStockPath = ''
        Serinfo = self.GetSerInfo()
        if Serinfo:
            SBCPath = Serinfo['FileStock'] + '/'
            SBCPath = SBCPath.replace('//', '/')
            FileStockPath = SBCPath + 'SBCstock'
            FileUsersPath = SBCPath + 'SBCUsers'
            if not os.path.isdir(FileStockPath):
                os.makedirs(FileStockPath)
            if not os.path.isdir(FileUsersPath):
                os.makedirs(FileUsersPath)
        return {'stock':FileStockPath+'/','user':FileUsersPath+'/'}
    def GetSerInfo(self):
        Info = SBCManagemodels.SBCManager.objects.all()
        if Info:
            info = {}
            info['SBCStockSize'] = Info[0].SBCStockSize
            info['FileStock'] = Info[0].FileStock
            info['UserStock'] = Info[0].UserStock
            return info
        return 0

    def ModCap(self,request):

        info = request.POST
        GetSerInfo = self.GetSerInfo()
        Total = GetSerInfo['SBCStockSize']
        if int(info['ModCap']) > Total:
            info['ModCap'] = Total
        user = info['user']
        ModCap = 1024*(int(info['ModCap'])*1024*1024*1024)/1000
        Userfo = User.objects.get(username=user)
        Userfo.totalcapacity = ModCap
        Userfo.save()
