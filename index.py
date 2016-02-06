# Berkeley DB Example

__author__ = "Bing Xu"
__email__ = "bx3@ualberta.ca"

import bsddb
import time
import sys
import os
from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')

# Make sure you run "mkdir /tmp/my_db" first!
#DA_FILE = sys.path[0]+"/tmp/lramsey_db"
DA_FILE_K = "/tmp/my_db/sample4_db"
DA_FILE_D = "/tmp/my_db/sample5_db"
DB_SIZE = 1000
SEED = 10000000

#if not os.path.exists(DA_FILE):
    #os.makedirs(DA_FILE)


def destroy():
    os.remove(DA_FILE_K)
    os.remove(DA_FILE_D)
    print "Files deleted"
    #os.rmdir(TMP_PATH)
    #print "tmp folder deleted
    
def writing(key, data):
    File = open('answers', 'w+')
    File.write(key)
    File.write('\n')
    File.write(data)
    File.write('\n')
    File.write('\n')
    File.close()

def retrieve_key(db):
    key = '-1'
    while int(key) not in xrange(0, DB_SIZE):
        try:
            key = str(int(input("Please enter a valid key:  \n")))
        except:
            print "invalid input"

    try:
        if db.has_key(key):
            writing(key, db[key])
            return db[key]
    except:
        print "key not found"
    return False

def retrieve_data(db):
    test = " "*62
    invalid = True
    while invalid and len(test) not in xrange(64,128):
            try:
                test = str(raw_input("Please enter data, must be between 64 and 127 characters:  \n"))
                if len(test) not in xrange(64, 128):
                    raise Exception
                if test == 'q':
                    return False
                invalid = False
            except:
                print "invalid input"    
    try:
        if db.has_key(test):
            keys = db[test].split()
            for key in keys:
                writing(key, test)
            return db[test]
        else:
            print "NO DATA FOUND"
            return False            
    except:
        print "NO DATA FOUND"
        return False


def retrieve_key_range(db):
    key1 = '-1'
    while int(key1) not in xrange(0, DB_SIZE):
        try:
            key1 = str(int(input("Please enter a valid starting key:  \n")))
        except:
            print "invalid input"   
            
    key2 = '-1'
    invalid = True
    while int(key2) not in xrange(0, DB_SIZE) or invalid== True:
        try:
            key2 = str(int(input("Please enter a valid ending key:  \n")))
            if int(key2)<=int(key1):
                print "the ending key must be more than the first"
            else:
                invalid = False
        except:
            print "invalid input"
            
    found = []        
    for i in range(int(key1), int(key2)):
        if db.has_key(str(i)):
            writing(str(i),db[str(i)]) 
            found.append(db[str(i)])
    return found








def main():
    try:
        db_key = bsddb.hashopen(DA_FILE_K, "w")
    except:
        print "DB doesn't exist, creating a new one"
        try:
            db_key = bsddb.hashopen(DA_FILE_K, "c")
        except:
            print "the database was not created."
            return
    try:
        db_data = bsddb.hashopen(DA_FILE_D, "w")
    except:
        print "DB doesn't exist, creating a new one"
        try:
            db_data = bsddb.hashopen(DA_FILE_D, "c")
        except:
            print "the database was not created."
            return    
    lib.set_seed(SEED)

    for index in range( DB_SIZE):
        krng = 64 + lib.get_random() % 64
        key = str(index)
        #for i in range(krng):
         #   key += str(unichr(lib.get_random_char()))
        vrng = 64 + lib.get_random() % 64
        value = ""
        ck = key
        for i in range(vrng):
            value += str(unichr(lib.get_random_char()))
        #print key
        #print value
        #print ""
        db_key[key] = value
    
    for index in xrange(DB_SIZE-1):
        key = str(index)
        keys = key
        data = db_key[key]
        #if db_data.has_key(data):
            #continue
        #for index2 in xrange(index+1, DB_SIZE):
            #if index2==index:
                #continue
            #else:
                #key2 = str(index2)
                #current = db_key[key2]
                #if current == data:
                    #keys += " " + key2
            #print keys
        if db_data.has_key(data):
            db_data[data] = db_data[data]+" "+keys
        else:
            db_data[data] = keys
            
    
    #data= db_key[str(DB_SIZE-1)]    
    #if db_data.has_key(data)==False:
     #   db_data[data] = str(DB_SIZE-1)
       
       
    #for x in db_data:
       # print db_data[x]
    #print db_data
    #try:
        #retrieve_key()
        ##retrieve_data(db_data)
        ##retrieve_key_range(db_key)
        #time1 = time.time()*1000
        #print db_key["54"]
        #time2 = time.time()*1000 - time1   
        #print time2, 'millisexobnds for key'
        
        #time1 = time.time()*1000
        #print db_data[db_key['65']]
        #time2 = time.time()*1000 - time1   
        #print time2, 'millisexobnds for data'        
        #'''
        ##time1 = time.time()*1000
        ##if db.has_key('999'):
         ##   print db['999']
        ##time3 = time.time()*1000 - time1
        ##print time3
        #'''
        #time1 = time.time()*1000
        
        #for i in range(30):
            #soemthi = db_key.has_key('999')
        #time2 = time.time()*1000 - time1   
        
        #print time2, 'millisexobnds for range'
        #'''
        ##print "difference" ,time2/time3
        ##db.close()
        #'''
    #except Exception as e:
        #print e
        
    return (db_key, db_data)    
if __name__ == "__main__":
    main()
   
