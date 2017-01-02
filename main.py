import time
from pyfirmata import Arduino, util
from GSM import GSM_Module

class Controller:
    def __init__(self,gsm,number):
        port = 'COM22'
        print ('CONNECTING TO ARDUINO, WAIT...')
        self.board = Arduino(port)
        print ('CONNECTED')
        time.sleep(2)
        self.gsm = gsm
        self.mob_number = number

        # START ON A NEW THREAD TO PREVENT OVERFLOW
        it = util.Iterator(self.board)
        it.start()

    def process(self):
        ration = lambda x: '' if not x else x
        
        sensor0 = self.board.get_pin('a:0:i')   # PHONE ALERT
        sensor1 = self.board.get_pin('a:1:i')   # MOTOR
        load1 = self.board.get_pin('d:11:o')   # MOTOR
        sensor0_value = None
        sensor1_value = None

        ###########################
        cutoff0 = 0.5
        cutoff1 = 0.3
        ###########################
        
        try:
            messege_sent = False
            while True:
                #print ('KEEP')
                sensor0_value = sensor0.read()
                sensor1_value = sensor1.read()
                print ("SENSOR 0: {0:<10}SENSOR 1: {1}".format(ration(sensor0_value),ration(sensor1_value)))
                
                if sensor0_value:
                    if sensor0_value > cutoff0 and not messege_sent:
                        self.gsm.call_utility(self.mob_number)
                        message_sent = True
                    else:
                        message_sent = False

                if sensor1_value:
                    if sensor1_value > cutoff1:
                        load1.write(1)
                    else:
                        load1.write(0)
                else:
                    load1.write(0)

        except KeyboardInterrupt:
            self.board.exit()
            
            os._exit()




if __name__ == '__main__':
    obj = GSM_Module()
    number = '+917004196160'
    c = Controller(obj,number)
    c.process()
