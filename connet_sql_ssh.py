import mysql.connector
import paramiko
import os
from stat import S_ISDIR as isdir
#import pysftp as sftp

class Connect:
    def get_auto_id(self):
        cnx = mysql.connector.connect(user='root', password='spotsign@123!',
                                      host='10.10.5.74',
                                      database='spotsign_demo_seafoods')
        cursor = cnx.cursor()
        query = ("SELECT  first_name,last_name,auto_id FROM inndata_emp_details")
        cursor.execute(query)
        result=cursor.fetchall()
        return result
        cursor.close()
        cnx.close()


    def down_from_remote(self,sftp_obj, remote_dir_name, local_dir_name):
        "" "download files remotely" ""
        remote_file = sftp_obj.stat(remote_dir_name)
        if isdir(remote_file.st_mode):
            # Folder, can't download directly, need to continue cycling
            self.check_local_dir(local_dir_name)
            print('Start downloading folder: ' + remote_dir_name)

            for remote_file_name in sftp_obj.listdir(remote_dir_name):
                sub_remote = os.path.join(remote_dir_name, remote_file_name)
                sub_remote = sub_remote.replace('\\', '/')
                sub_local = os.path.join(local_dir_name, remote_file_name)
                sub_local = sub_local.replace('\\', '/')
                self.down_from_remote(sftp_obj, sub_remote, sub_local)
        else:
            # Files, downloading directly
            print('Start downloading file: ' + remote_dir_name)
            sftp_obj.get(remote_dir_name, local_dir_name)


    def check_local_dir(sel,local_dir_name):
        "" "whether the local folder exists, create if it does not exist" ""
        if not os.path.exists(local_dir_name):
            os.makedirs(local_dir_name)


    def __call__(self):
        "" "program main entry" ""
        # Server connection information
        host_name = '10.10.5.74'
        user_name = 'inndata'
        password = '123!@#'
        port = 22
        # Remote file path (absolute path required)
        remote_dir = '/home/inndata/inndata_emp_images/'
        # Local file storage path (either absolute or relative)
        local_dir = '/home/anish/PycharmProjects/attendance_system/inndata_emp_images'

        # Connect to remote server
        t = paramiko.Transport((host_name, port))
        t.connect(username=user_name, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)

        # Remote file start download
        self.down_from_remote(sftp, remote_dir, local_dir)

        # Close connection
        t.close()

a=Connect()
a()
