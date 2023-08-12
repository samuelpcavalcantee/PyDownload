from urllib3 import PoolManager, Timeout
import os
import threading
import time

defaul_header = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

class download():  
    def __init__(self, url:str, path:str, file_name:str = None, header:dict = {},  human:bool = False, sucess = None, sucess_args = None, error = None, error_args = None, change = None, change_args = None):
        
        self.__url = url
        self.__path = path
        self.__file_name = file_name if file_name is not None else self.__url.split('/')[-1]
        self.__header = defaul_header     
        self.__header.update(header)
        
        self.__human = human
        
        self.__success_target = sucess
        self.__success_args = sucess_args
        self.__error_target = error
        self.__error_args = error_args
        self.__change_target = change
        self.__change_args = change_args
        
        self.__size_total = 0
        self.__time_total = 0
        self.__size_downloaded = 0
        self.__size_remainer = 0
        self.__speed = 0 
        self.__status_code = 0      

        self.__http = PoolManager()
        self.__time_start_duration = time.time()

        if self.__verify_header():   
            threading.Thread(target=self.__download).start()
    
    def info(self):
        self.__size_remainer = self.__size_total - self.__size_downloaded 
        self.__time_total = time.time() - self.__time_start_duration
        duration_prev = self.__size_remainer/self.__speed if self.__speed > 0 else 0

        response = {
            "computer" : {
                "size" : self.__size_total,
                "downloaded" : self.__size_downloaded,
                "download_remainer" : self.__size_remainer,
                "speed" : self.__speed,
                "duration" : self.__time_total,
                "duration_prev" : duration_prev,
                "status_code" : self.__status_code
            }
        } 
               
        if self.__human:          
            response.update({
                "human" : {
                    "size" : self.__human_size(self.__size_total),
                    "downloaded" : self.__human_size(self.__size_downloaded),
                    "download_remainer" : self.__human_size(self.__size_remainer),
                    "speed" : self.__human_size(self.__speed),
                    "duration" : self.__human_time(self.__time_total),
                    "duration_prev" : self.__human_time(duration_prev),
                    "status_code" : self.__status_code
                }
            })
         
        return response 

    def __download(self):        
        try:
            response = self.__http.request(method="GET", url=self.__url, preload_content=False, headers=self.__header)           
            
            if not os.path.exists(self.__path):
                os.makedirs(self.__path)
            
            start_time = time.time()
            temp_buffer = 0
                   
            with open(self.__path + self.__file_name, 'wb') as file:
                while True:                  
                    buffer = response.read(1024)                                   
                    if not buffer:
                        break                
                    file.write(buffer)             
                    
                    count_byte = len(buffer)                           
                    temp_buffer += count_byte
                    self.__size_downloaded += count_byte                    
       
                    final_time = time.time() - start_time            
                    if final_time > 3:
                        self.__change_exec()
                        self.__speed = int(temp_buffer / final_time)
                        temp_buffer = 0
                        start_time = time.time()
                                 
            response.release_conn()
            self.__success_exec()             
        except:
            self.__error_exec()

    def __verify_header(self):             
        info_headers = self.__header
        info_headers.update({"Range" : "bytes=0-3"})
        try:
            response = self.__http.request(method="HEAD", url=self.__url, preload_content=False, headers=info_headers, timeout=Timeout(10))
            self.__status_code = response.status
            if response.status == 206:
                self.__size_total = int(response.headers.get("Content-Range").split('/')[-1]) 
                return True   
            elif response.status == 200:
                self.__size_total = int(response.headers.get("Content-Length")) 
                return True
        
        except:
            self.__error_exec()
            return False

    def __human_time(self, value):
        value = abs(value)     
        hours = int(value // 3600)
        minutes = int((value % 3600) // 60)
        seconds = int(value % 60)
        return "{}h {}m {}s".format(hours, minutes, seconds)

    def __human_size(self, value):
        value = abs(value)
        suffix = (" kB", " MB", " GB", " TB", " PB", " EB", " ZB", " YB")
        
        for i, s in enumerate(suffix):
            unit = 1024 ** (i + 2)
            if value < unit:
                break

        response = "%.1f" % (1024 * value / unit) + s
        return response
    
    def __success_exec(self):
        if self.__success_target and self.__success_args:
            self.__success_target(self.info(), *self.__success_args)
        elif self.__success_target:
            self.__success_target(self.info())
     
    def __error_exec(self):
        if self.__error_target and self.__error_args:
            self.__error_target(self.info(), *self.__error_args)
        elif self.__error_target:
            self.__error_target(self.info())

    def __change_exec(self):
        if self.__change_target and self.__change_args:
            self.__change_target(self.info(), *self.__change_args)
        elif self.__change_target:
            self.__change_target(self.info())