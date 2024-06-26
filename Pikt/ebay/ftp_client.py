import os
import csv
import paramiko
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class FTPClient:
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def upload_file(self, local_path, remote_path):
        try:
            print(f"Uploading {local_path} to {remote_path}")
            self.sftp.put(local_path, remote_path)
            print("Upload successful.")
        except FileNotFoundError as e:
            print(f"FileNotFoundError: {e}")
        except Exception as e:
            print(f"Failed to upload file: {e}")

    def close(self):
        self.sftp.close()
        self.transport.close()

    def list_directories(self, remote_path='/'):
        try:
            for entry in self.sftp.listdir_attr(remote_path):
                print(entry.filename, 'd' if entry.st_mode == 16877 else 'f')
        except Exception as e:
            print(f"Failed to list directories: {e}")
        
    def list_files(self, remote_path='/'):
        try:
            files = self.sftp.listdir(remote_path)
            for file in files:
                print(file)
            # return files
        except Exception as e:
            print(f"Failed to list files: {e}")
            # return None
    
    def connect(self):
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(transport)
            print("Connection established.")
        except Exception as e:
            print(f"Failed to connect to SFTP: {e}")
    
    def download_file(self, remote_path, local_path):
        self.sftp.get(remote_path, local_path)
        print(f"File downloaded successfully from {remote_path} to {local_path}")
