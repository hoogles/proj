
import bsddb
import time
import sys
import os
from ctypes import cdll
lib = cdll.LoadLibrary('./libfoo.so')


# Make sure you run "mkdir /tmp/my_db" first!
DA_FILE = "/tmp/my_db/sample2_db"
DB_SIZE = 100000
SEED = 10000000

def destroy():
    os.remove(DA_FILE)
    print "File deleted"
    #os.rmdir(TMP_PATH)
    #print "tmp folder deleted"
    
def writing(key, data):
    File = open('answers', 'w+')
    File.write(key)
    File.write('\n')
    File.write(data)
    File.write('\n')
    File.write('\n')
    File.close()
    
def retrieve_key(db):
    #according to notes, this is how its done
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
    x= db.first()[1]
    i =0
    found = 0
    while x!= test:   
        x = db.next()
        i+=1
        if test== x[1]:
            print "key of found data=",x[0]
            found += 1
        if i>= DB_SIZE-2:
            break
        
    if found ==0:
        print "not found"
        return False
    print "found"
    return True


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
            found.append(db[str(i)])
    return found
    
def main():
    try:
        db = bsddb.hashopen(DA_FILE, "w")
    except:
        print "DB doesn't exist, creating a new one"
        db = bsddb.hashopen(DA_FILE, "c")
    lib.set_seed(SEED)

    for index in range(1, DB_SIZE):
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
        db[key] = value
        
    #try:
        #time1 = time.time()*1000
        #if db.has_key('999'):
            #print db['998']
        #time3 = time.time()*1000 - time1
        #time1 = time.time()*1000
        
        #test = db['999']
        #x= db.first()[1]
        #while x!= test:                 
            #x = db.next()[1]
        #time4 = time.time()*1000 - time1
        
        #time1 = time.time()*1000
        #for i in range(30):
            #x= db.has_key('999')
        #time2 = time.time()*1000 - time1   
        #print "execution time for key", time3
        #print "execution time for data",time2
        #print "execution time for key range", time4
    #except Exception as e:
        #print e
    return db

if __name__ == "__main__":
    main()
