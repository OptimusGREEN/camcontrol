from camcontrol import CamControl
from myqtt import Myqtt
import logging, os

def setupLogging(DEBUG_MODE=False):
    log_filename = '/Users/john/BT Cloud/Development/DevTest/logs/cam_control_test.log'
    old_log_filename = '/Users/john/BT Cloud/Development/DevTest/logs/old_cam_control_test.log'
    if os.path.exists(log_filename):
        if os.path.exists(old_log_filename):
            try: os.remove(old_log_filename)
            except: print("Couldn't remove old log")
        os.rename(log_filename, old_log_filename)
    if DEBUG_MODE:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    format = "OptiSERVE [%(levelname)s] [%(module)s:%(lineno)d] " + " - %(asctime)s - %(message)s"
    if DEBUG_MODE:
        logging.basicConfig(level=log_level,format=format,handlers=[logging.FileHandler(log_filename),logging.StreamHandler()])
    else:
        logging.basicConfig(filename=log_filename, level=log_level, format=format)

setupLogging(True)

driveway = CamControl("192.168.7.112")
garden = CamControl("192.168.7.111")

def dcb(client, userdata, message):
    logging.debug("")
    if int(message) == 0:
        driveway.light_off()
    if int(message) == 1:
        driveway.light_on()
    if int(message) == 3:
        driveway.light_toggle()

def gcb(client, userdata, message):
    logging.debug("")
    if int(message) == 0:
        garden.light_off()
    if int(message) == 1:
        garden.light_on()
    if int(message) == 3:
        garden.light_toggle()


def get_subscription_calbacks():
    logging.debug("")
    sub_dict = {"camera_test/driveway/light/cmnd": dcb,
                "camera_test/garden/light/cmnd": gcb}
    return sub_dict

myqtt = Myqtt()
myqtt.topic_callbacks = get_subscription_calbacks()


garden.light_toggle()
