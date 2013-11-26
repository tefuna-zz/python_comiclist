'''
Created on 2013/11/26

@author: tefuna
'''

# coding: utf-8

import re

PAGELIST_PATH = "D:/work/filelist.txt"
PREFIXLIST_PATH = "D:/work/prefixlist.txt"
COMMANDLIST_DIR = "D:/work/"


# prefixlistを読み込む
def setup_prefix(prefixfile):

    prefixfile = open(PREFIXLIST_PATH, "r")
    prefixdict = {}
    print("header = " + prefixfile.readline())
    for line in prefixfile:
        line = line.strip()
        line_items = line.split('\t')
        prefixdict[line_items[0]] = line_items[1]

    prefixfile.close()
    return prefixdict


# edit_fixedpath
def edit_fixedpath(oldpath, prefix, vol, pagenum):

    match = re.search(r'第\d+巻', vol)
    if match == None:
        raise

    volstr = match.group()
    volnum = volstr[1:-1]
    oldname = oldpath[oldpath.rindex('\\') + 1: len(oldpath)]
    ext = oldname[oldname.rindex('.'): len(oldname)]

    fixedname = prefix + '-' + volnum + '-' + "{0:0>3}".format(pagenum) + ext
    fixedpath = oldpath.replace(oldname, fixedname)
    print(fixedpath)

    return fixedpath


# main
if __name__ == '__main__':

    # prefixlistを読み込む
    prefixdict = setup_prefix(PREFIXLIST_PATH)
    print(prefixdict)

    commandfile = open(COMMANDLIST_DIR + "cmd.txt", 'w')

    # filelistを読み込み、処理開始
    pagefile = open(PAGELIST_PATH, 'r')
    title = ""
    vol = ""
    pagenum = 1
    print("header = " + pagefile.readline())
    for line in pagefile:
        line = line.strip()
        nodelist = line.split("\\")

        if vol != nodelist[3]:
            pagenum = 1
        else:
            pagenum = pagenum + 1

        title = nodelist[2]
        vol = nodelist[3]
        filename = nodelist[4]

        print (line)
        fixedpath = edit_fixedpath(line, prefixdict.get(title), vol, pagenum)
        commandfile.write("move \"" + line + "\" \"" + fixedpath + "\"\n")

    commandfile.close()
    pagefile.close()
