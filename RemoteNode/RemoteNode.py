from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
import azure.common
import time 
import paramiko

block_blob_service = BlockBlobService(account_name='imagezeiss',account_key='eS2RdS7Zbt2WtejZfKzUQHXjihKds2c9YNjwo/G5RjtLhZK0k+hKbhdyWWtC5tTBL9TP+MAqK3VCiyzXlOtaIQ==')

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

val = 1
while(True):
	try:
		ssh_client.connect(hostname='192.168.1.154',username='zeiss',password='kedia123')
		ftp_client = ssh_client.open_sftp() 
		ftp_client.get("C:\Users\praked\Pictures\Snap_00"+str(val)+".jpg","out"+str(val)+".jpg")
		ftp_client.close()
		block_blob_service.create_blob_from_path('uplink',"firstblood"+str(val)+".jpg","out"+str(val)+".jpg" ,content_settings=ContentSettings(content_type='image/jpeg'))
		val = val + 1
	except IOError:
		pass
	time.sleep(3)	
