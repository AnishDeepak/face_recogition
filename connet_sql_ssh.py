import mysql.connector
import paramiko
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
    def get_images(self):
        # Update the next three lines with your
        # server's information
        host = "10.10.5.74"
        username = "inndata"
        password = "123!@#"
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout, _stderr = client.exec_command("cp -r inndata_emp_images /home/anish/PycharmProjects/attendance_system/")
        print(_stdout.read().decode())
        client.close()
    def __call__(self):
         self.get_auto_id()
         self.get_images()
a=Connect()
a()
