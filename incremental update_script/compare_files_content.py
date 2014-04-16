#!/usr/bin/python
# author:hudsondeng

import filecmp,os,sys,shutil, time

import logging, ConfigParser


##
## Function sync (src, dst, dst_2)
##
##    update process
##
##
def sync(src, dst, dst_2):
    global add_file_num, change_file_num, all_change_num
    if not os.path.exists(dst):
        os.mkdir(dst)

    if not os.path.exists(dst_2):
        os.mkdir(dst_2)

    filenames = os.listdir(src)

    for name in filenames:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        dst_2_name = os.path.join(dst_2, name)

        if os.path.isdir(srcname):
            if not os.path.exists(dstname):
                os.mkdir(dstname)

            if not os.path.exists(dst_2_name):
                os.mkdir(dst_2_name)

            sync(srcname, dstname, dst_2_name)
            
        elif os.path.isfile(srcname):
            if not os.path.exists(dstname):
                shutil.copy2(srcname, dstname)
                shutil.copy2(srcname, dst_2_name)

                add_file_num=add_file_num+1
                if log_flag:
                    logging.info('add file: ' + name)
                
            elif not filecmp.cmp(srcname, dstname):
                shutil.copy2(srcname, dstname)
                shutil.copy2(srcname, dst_2_name)
                
                change_file_num=change_file_num+1
                if log_flag:
                    logging.info('change file: ' +name)




#read config file
cf = ConfigParser.ConfigParser()
real_path = os.path.split(os.path.realpath(__file__))[0]
config_path = os.path.join(real_path, "config.conf")
cf.read(config_path)

#source data folder is exist
srcFolder = cf.get("path", "srcFolder")
if not os.path.exists(srcFolder):
    print '[Error] No such srcFolder directory: ' , srcFolder
    sys.exit()

if not os.path.isdir(srcFolder):
    print '[Error] srcFolder is not directory: ' , srcFolder
    sys.exit()
    
compareFolder = cf.get("path", "compareFolder")
destFolder = cf.get("path", "destFolder")

log_flag = cf.getint("comm", "log")
log_path = cf.get("comm", "log_path")

#log or not
if log_flag:
    today_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_file_name = '%s/content_change_statistic_%s.log' % (log_path, today_date)
    logging.basicConfig(level=logging.INFO,
                                     format='%(asctime)s %(message)s',
                                     datefmt='[%Y-%m-%d %H:%M:%S]',
                                     filename=log_file_name,
                                     filemode='a+')

#stat varible
change_file_num=0
add_file_num=0
all_change_num=0


#comparison start from here
print 'start...'   
sync(srcFolder , compareFolder, destFolder)

all_change_num=add_file_num+change_file_num

print 'new file num : ' , add_file_num
print 'modify file num : ' , change_file_num
print 'all change num : ' , all_change_num

if log_flag:
    logging.info('\n' + 'add_file_num=' + str(add_file_num) + '\n' +
                 'change_file_num=' + str(change_file_num) + '\n' +
                 'all_change_num=' + str(all_change_num) + '\n')

print 'done...'

