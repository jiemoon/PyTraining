import re
import os
import wget
import json
import pprint
import shutil
import filecmp
import zipfile
from core import Core_rsync
from conf import Conf_summary

def f_download(svn_key,svn_url,svn_note):
    """Download firmwares from svn and create files.

    :param svn_key: Conf_summary dict common key
    :param svn_url: svn url
    :param svn_note:svn releasenote
    :reutrn: None
    """
    # start download release note file.
    level = 'info'
    download_dir = Conf_summary.dest_dict[svn_key]
    os.chdir(download_dir)
    release_note = os.path.join(download_dir,'ReleaseNote')
    if os.path.exists(release_note):
        os.remove(release_note)
    message = 'succ download %s' % svn_note
    try:
        wget.download(svn_note)
    except Exception as e:
        level = 'critical'
        message = 'fail download %s' % svn_note
        Conf_summary.logg_dict[svn_key](message,level)

        # download with error, remove it
        os.remove(release_note)
        return
    # Conf_summary.logg_dict[svn_key](message,level)
    # start concert releasenote to dict
    bin_dict = f_note2dict(svn_key,release_note)
    pprint.pprint(bin_dict)

    # start match releasenote and create files
    bin_info = None
    bin_keys = None
    bin_file = os.path.basename(svn_url)
    real_bin = os.path.join(download_dir,bin_file)
    # start download firmware file.
    if os.path.exists(real_bin):
        os.remove(real_bin)
    message = 'succ download %s' % svn_url
    try:
        wget.download(svn_url)
    except Exception as e:
        level = 'error'
        message = 'fail download %s' % svn_note
        Conf_summary.logg_dict[svn_key](message,level)

        # download with error, remove it
        os.remove(real_bin)
        return
    # Conf_summary.logg_dict[svn_key](message,level)
    for cur_key in bin_dict.iterkeys():
        cur_date = cur_key[0].replace('-','')
        print cur_key,bin_file
        if cur_date in bin_file and cur_key[1] in bin_file:
            bin_keys = cur_key
            bin_info = bin_dict[cur_key]
            break
    if not bin_info:
        message = '%s has no record in releasenot file' % real_bin
        Conf_summary.logg_dict[svn_key](message,'error')

        # has no record in releasenote, remove it
        os.remove(real_bin)
        return
    # start try to get devid from bin files
    alldevid = f_unzipfile(svn_key,real_bin)
    if len(alldevid) != 24:
        message = '%s has wrong with DevID field' % real_bin
        Conf_summary.logg_dict[svn_key](message,'error')

        # has wrong devid in firmware, remove it
        os.remove(real_bin)
        return
    # start convert devid with source devid filed
    alldevid = f_idconvert(alldevid)
    download_devidir = os.path.join(download_dir,alldevid)
    download_dstdate = os.path.join(download_devidir,bin_keys[0])

    # start move firmware dirs to download
    rsync_upload_dir = Conf_summary.sync_dict[svn_key]
    upload_devid_dir = os.path.join(rsync_upload_dir,alldevid)
    upload_dstdate = os.path.join(upload_devid_dir,bin_keys[0])

    if os.path.exists(upload_dstdate):
        # firmware exists in upload_files , remove it
        os.remove(real_bin)
        return
    if not os.path.exists(download_dstdate):
        os.makedirs(download_dstdate)
    else:
        shutil.rmtree(download_dstdate,ignore_errors=True)
        os.makedirs(download_dstdate)
    ll_level = os.path.join(download_dstdate,'Level_%s.dat' % bin_info['Level'])
    cc_loggs = os.path.join(download_dstdate,'ChangeLog_Chinese.dat')
    ce_loggs = os.path.join(download_dstdate,'ChangeLog_English.dat')
    dst_file = os.path.join(download_dstdate,bin_file)
    with open(ll_level,'w') as whandler:
        whandler.write('')
    with open(cc_loggs,'w') as whandler:
        cc_info = map(lambda s: s + '\n',bin_info['ChangeLog_SimpChinese'])
        whandler.writelines(cc_info)
    with open(ce_loggs,'w') as whandler:
        ce_info = map(lambda s: s + '\n',bin_info['ChangeLog_English'])
        whandler.writelines(ce_info)
    shutil.copy2(real_bin,dst_file)
    os.remove(real_bin)
    f_copyfiles(download_devidir, upload_devid_dir)

    # message = 'succ move %s to %s for rsync' % (download_devid_dir,upload_devid_dir)
    # Conf_summary.logg_dict[svn_key](message,'info')


def f_copyfiles(sou_path, dst_path):
    """Copy from souce path to destination path.

    :param sou_path: source path
    :param dst_path: destination path
    :return: None
    """
    for root, dirs, files in os.walk(sou_path):
        for cur_file in files:
            dw_file_path = os.path.join(root, cur_file)
            up_file_path = dw_file_path.replace(sou_path,dst_path)
            up_dirs_name = os.path.dirname(up_file_path)
            if not os.path.exists(up_dirs_name):
                os.makedirs(up_dirs_name)
            shutil.copy2(dw_file_path,up_file_path)
    shutil.rmtree(sou_path)

def f_idconvert(dev_id):
    """Convert devid to special format.

    :param dev_id: DevID in InstallDesc
    :return: None
    """
    res_id = ''
    if dev_id[5] < '5':
        res_id = dev_id[:8] + 'XXXXXXXXXXX' + dev_id[19:]
    else:
        res_id = dev_id[:8] + dev_id[8:13].replace('2','0').replace('3','1') + '0000' + dev_id[17:]
    return res_id


def f_unzipfile(svn_key,bin_file):
    """Unzip file and read DevID

    :param svn_key: svn_key for logging
    :param bin_file: firmware bin file
    :return: None
    """
    dev_id = ''
    try:
        zfile = zipfile.ZipFile(bin_file,'r')
    except Exception as e:
        message = 'unzip %s with error.' % bin_file
        Conf_summary.logg_dict[svn_key](message,'error')
    else:
        for z in zfile.namelist():
            if z == 'InstallDesc':
                zdata = zfile.read(z)
                if 'DevID' in zdata:
                    dev_id = json.loads(zdata)['DevID']

    return dev_id


def f_note2dict(svn_key,svn_note):
    """Read release note and convert to dict.

    :param svn_key: svn key for logging
    :param svn_note: svn release note
    :return: dict
    """
    date2firmware = {}
    note2firmware = {}
    start_records = False
    with open(svn_note,'r+b') as rhandler:
        for cur_line in rhandler:
            match = re.match('(\\d{4}-\\d{1,2}-\\d{1,2})\\W+([A-Z-0-9_a-z]+)',cur_line)
            if match:
                cur_date,cur_type = match.groups()
                date2firmware.update({(cur_date,cur_type): []})
                start_records = True
            if start_records:
                date2firmware[cur_date,cur_type].append(cur_line)

    for cur_key,cur_val in date2firmware.iteritems():
        if not cur_val[2:]:
            message = '%s with wrong releasenote format:%s %s' % (svn_note,cur_key[0],cur_key[1])
            Conf_summary.logg_dict[svn_key](message,'warning')
            continue
        if cur_key[0] not in cur_val[2]:
            message = '%s with wrong releasenote format:%s %s' % (svn_note,cur_key[0],cur_key[1])
            Conf_summary.logg_dict[svn_key](message,'warning')
            continue
        change_dict = {'Level': None,
         'XmCloudUpgrade': None,
         'ChangeLog_SimpChinese': [],
         'ChangeLog_English': []}
        add_flag = True
        for cur_item in cur_val[3:]:
            cur_item = cur_item.rstrip()
            match = re.match('(Level|XmCloudUpgrade|ChangeLog_SimpChinese|ChangeLog_English)\\s*=\\s*(.*)',cur_item)
            if match:
                match_key,match_val = match.groups()
                match_key = match_key.strip()
                match_val = match_val.strip()
                if not match_val:
                    match_val = []
                # filter XmCloudUpgrade != 1,don't upgrade
                if match_key == 'XmCloudUpgrade' and not match_val == '1':
                    add_flag = False
                    break
                change_dict.update({match_key: match_val})
            else:
                try:
                    change_dict[match_key].append(cur_item)
                except Exception,e:
                     message = '%s with wrong releasenote format:%s %s' % (svn_note,cur_key[0],cur_key[1])
                     Conf_summary.logg_dict[svn_key](message,'error')
        if add_flag:
            note2firmware.update({cur_key: change_dict})

    return note2firmware
