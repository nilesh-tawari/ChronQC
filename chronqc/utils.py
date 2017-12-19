# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 13:02:26 2017

@author: tawarinr
"""
import ntpath
import sys
from datetime import date, timedelta
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
try:
    import configparser
    Config = configparser.ConfigParser()  # ver. < 3.0
except:
    import ConfigParser
    Config = ConfigParser.ConfigParser()

def path_leaf(path):
    """
    split the path in tail and head
    str -> str, str
    """
    head, tail = ntpath.split(path)
    return head, tail or ntpath.basename(head)

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
    """
    Call in a loop to create terminal progress bar

    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def json_to_dict(config_json):
        '''
        Read the configuration json file
        :param config_json : Path of the configuration file
        '''
        json_data = open(config_json)
        data = json.loads(json_data.read())
        json_data.close()

        return data

def send_email(TO, FROM, TEXT, SUB, smtp_server, CC=[]):
        '''
        Creates a HTML-based email with clickable link and send it out using sendmail
        '''

        ## make text MIME format
        msg = MIMEMultipart('alternative')
        body = MIMEText(TEXT, 'html')
        msg.attach(body)

        ## for displaying only
        msg['Subject'] = SUB
        msg['From'] = ','.join(FROM)

        ## list to string, check if its a string first
        msg['To'] = ','.join(TO)
        msg['Cc'] = ','.join(CC)

        email_addresses = TO + CC

        ## real address that sendmail module use shld be a list
        ## Send the message via our own SMTP server, but don't include the envelope header
        s = smtplib.SMTP( smtp_server )
        s.sendmail(msg['from'], email_addresses, msg.as_string())
        s.quit()

class custparser(Config):
	'''
	Reads an .ini file using ConfigParser and transform it into a dictionary for easy reading
	'''
	def as_dict(self):

		d = dict(self._sections)
		for k in d:
			d[k] = dict(self._defaults, **d[k])
			d[k].pop('__name__', None)

		return d

