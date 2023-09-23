from datetime import datetime
import os
import pickle
from threading import Thread, Lock

lock = Lock()

class Cache:
    def __init__(self):
        self.FILENAME = './cache/cache.pickle'
        self.LIST_FILENAME = './cache/list.pickle'
        self.SYNC_TIME_LIMIT = 1 # seconds
        self.MINUTE = 60
        self.SCRAPPING_TIME_LIMIT = 5 * self.MINUTE
        self.TASKS_LIMIT = 5
        self.updatedAt = 0 # indicates the last time the cache was updated
        self.dict = {}
        self.writeList = []

        # obtém os dados do cache utilizado thread
        thread1 = Thread(target=self.getFromDisk)
        thread2 = Thread(target=self.getWriteListFromDisk)

        thread1.start()
        thread2.start()

        # thread1.join()
        # thread2.join()

    def getFromMemory(self, task):
        operation, *params = task.split(" ")

        if operation == 'last_news_if_barbacena':
            if (datetime.now().timestamp() - self.updatedAt) >= self.SCRAPPING_TIME_LIMIT:
                self.clearOperationInMemory(operation)
                return None
            for key in self.writeList:
                keyOperation, keyParams = key.split(" ")
                if keyOperation == operation and int(keyParams[0]) > int(params[0]):
                    task = key
                    break

            if task in self.dict:
                return self.dict[task][:int(params[0])]
        else:
            if task in self.dict:
                return self.dict[task]

        return None

    def getFromDisk(self):
        try:
            with open(self.FILENAME, 'rb') as f:
                cache = pickle.load(f)
        except:
            cache = {}
            
        self.dict = cache
        if 'updatedAt' in cache:
            self.updatedAt = cache['updatedAt']
    
    def getWriteListFromDisk(self):
        try:
            with open(self.LIST_FILENAME, 'rb') as f:
                writeList = pickle.load(f)
        except:
            writeList = []

        self.writeList = writeList

    def writeInMemory(self, task, data):
        if len(self.dict) >= self.TASKS_LIMIT + 1:
            first = self.writeList.pop(0)
            del self.dict[first]
        
        self.dict[task] = data # add task result to cache
        self.dict['updatedAt'] = datetime.now().timestamp() # update timestamp
        self.writeList.append(task)

    def writeInDisk(self):
        print('writing to disk')
        def saveCache():
            with lock:
                os.makedirs(os.path.dirname(self.FILENAME), exist_ok=True)
                with open(self.FILENAME, 'wb') as f:
                    pickle.dump(self.dict, f)
                self.updatedAt = datetime.now().timestamp()
        
        def saveList():
            with lock:
                os.makedirs(os.path.dirname(self.LIST_FILENAME), exist_ok=True)
                with open(self.LIST_FILENAME, 'wb') as f:
                    pickle.dump(self.writeList, f)

        thread1 = Thread(target=saveCache)
        thread2 = Thread(target=saveList)

        thread1.start()
        thread2.start()

    def write(self, task, data):
        self.writeInMemory(task, data)
        # print(datetime.now().timestamp() - self.__updatedAt, self.__SYNC_TIME_LIMIT)
        if (datetime.now().timestamp() - self.updatedAt) >= self.SYNC_TIME_LIMIT:
            self.writeInDisk()

    def clearOperationInMemory(self, operation):
        for key in self.writeList:
            keyOperation = key.split(" ")[0]
            if keyOperation == operation:
                if key in self.dict:
                    del self.dict[key]
        
    