import pywinauto
import csv, glob, sys
import subprocess
import time

class GSM_Module():
    def __init__(self):
        self.key_map = {'+':u'+Button',
                        '0':u'0Button',
                        '1':u'1Button',
                        '2':u'2Button',
                        '3':u'3Button',
                        '4':u'4Button',
                        '5':u'5Button',
                        '6':u'6Button',
                        '7':u'7Button',
                        '8':u'8Button',
                        '9':u'9Button',
                        'Back_Space':u'CButton',
                        'Call':u'CallButton'}

        self.pwa_app = pywinauto.application.Application()

        PID = self.initial_status()
        if PID is None:
            self.pwa_app.start(u"C:\Program Files (x86)\Mobile Partner\Mobile Partner.exe")
            time.sleep(10)
        else:
            self.pwa_app.connect(process=PID)

    def initial_status(self):
        cmd = 'tasklist /fo csv'
        p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        resp = p.communicate()[0].decode('utf-8').splitlines()
        reader = csv.DictReader(resp)
        for event in reader:
            if event['Image Name'] == 'Mobile Partner.exe':
                print ('APPLICATION ACTIVE AT PID - ',event['PID'])
                return int(event['PID'])
        return None

    def get_object_from_style_id(self,id):
        window = self.pwa_app.top_window_()
        window.Wait('ready')
        child = None
        for _ in window.Children():
            if _.Style() == id:
                child = _
                break
        if child is None:
            print ('ERROR : {0} ASSUMPTION WRONG'.format(id))
            sys.exit()
        else:
            return child

    def call_utility(self,number):
        window = self.pwa_app.top_window_()
        upper_toolbar = self.get_object_from_style_id(1409292382)
        call_area = upper_toolbar.Button(2)
        call_area.Click()

        self.type_number(window,number)
        window[self.key_map['Call']].Click()

    def type_number(self,window,number):
        for i in range(12):
            window[self.key_map['Back_Space']].Click()
        for digit in number:
            window[self.key_map[digit]].Click()

    def message_utility(self,number):
        window = self.pwa_app.top_window_()
        upper_toolbar = self.get_object_from_style_id(1409292382)
        message_area = upper_toolbar.Button(3)
        message_area.Click()

        messaging_toolbar = self.get_object_from_style_id(1409288526)
        messaging_toolbar.Button(0).Click()

        new_message_handle = pywinauto.findwindows.find_windows(title=u'New')[0]
        new_message_window = self.pwa_app.window_(handle=new_message_handle)

        message_content = 'ALERT:{SPACE}HOME{SPACE}SECURITY{SPACE}COMPROMISED.'
        new_message_window.TypeKeys('%s{TAB}'%number)
        new_message_window.TypeKeys(message_content)
        new_message_window.TypeKeys('{TAB}{TAB}{ENTER}')
