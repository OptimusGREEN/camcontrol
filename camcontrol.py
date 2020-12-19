import telnetlib, time, threading, logging, os

# def setupLogging(DEBUG_MODE=False):
#     log_filename = '/home/john/scripts/python_scripts/logs/system2mqtt.log'
#     old_log_filename = '/home/john/scripts/python_scripts/logs/old_system2mqtt.log'
#     if os.path.exists(log_filename):
#         if os.path.exists(old_log_filename):
#             try: os.remove(old_log_filename)
#             except: print("Couldn't remove old log")
#         os.rename(log_filename, old_log_filename)
#     if DEBUG_MODE:
#         log_level = logging.DEBUG
#     else:
#         log_level = logging.INFO
#     format = "OptiSERVE [%(levelname)s] [%(module)s:%(lineno)d] " + " - %(asctime)s - %(message)s"
#     if DEBUG_MODE:
#         logging.basicConfig(level=log_level,format=format,handlers=[logging.FileHandler(log_filename),logging.StreamHandler()])
#     else:
#         logging.basicConfig(filename=log_filename, level=log_level, format=format)
#
# setupLogging(False)

class CamControl(object):

    def __init__(self, host, user="root", password="cxlinux", port=23):

        self.cam = telnetlib.Telnet(host, port)
        self.cam.read_until(b"login: ")
        self.cam.write(user.encode('ascii') + b"\n")
        if password:
            self.cam.read_until(b"Password: ")
            self.cam.write(password.encode('ascii') + b"\n")

        self.main_loop = threading.Thread(target=self.loop)
        self.main_loop.start()

    def loop(self):
        logging.debug("Main loop started")
        while True:
            pass

    def light_on(self, pin=30):
        logging.debug("Turning on light")
        self.cam.write("gio -s {} 1\n".format(pin).encode('ascii'))

    def light_off(self, pin=30):
        logging.debug("Turning off light")
        self.cam.write("gio -s {} 0\n".format(pin).encode('ascii'))

    def light_toggle(self, pin=30):
        logging.debug("Toggling light")
        self.cam.write("gio -g {}\n".format(pin).encode('ascii'))
        time.sleep(0.5)
        state = self.cam.read_some().decode('utf-8')
        # print("#######   -   ", state)
        if int(state) == 0:
            self.light_on()
        elif int(state) == 1:
            self.light_off()
        else:
            logging.error("Pin state was {}, which was unexpected".format(state))

    def close(self):
        logging.debug("Closing telnet session")
        self.cam.close()
