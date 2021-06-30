import atexit
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from home_assistant.schedulers.models import Scheduler
from home_assistant import db
from w1thermsensor import W1ThermSensor
from . import mail
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

engine = create_engine('sqlite:///db.sqlite3')
session = Session(engine)
cron_scheduler = BackgroundScheduler()
cron_time_list = ["second", "minute", "hour", "day", "month", "day_of_week"]

def get_current_temperature():
    sensor = W1ThermSensor()
    temperature_raw = sensor.get_temperature()
    return f"{'%.1f' % temperature_raw} °C"

def set_gpio_appliances(appliances) -> None:
    for appliance in appliances:
        GPIO.setup(appliance.pin_num,GPIO.OUT)
        if appliance.running_state == "continuous":
            energy_state = GPIO.HIGH
            if appliance.state >= 1:
                energy_state = GPIO.LOW
            GPIO.output(appliance.pin_num,energy_state)
        elif appliance.running_state == "initial":
            if appliance.previous_state != appliance.state:
                servo = GPIO.PWM(appliance.pin_num,50)
                servo.start(0)
                servo.ChangeDutyCycle(2+(appliance.state/18))
                time.sleep(0.5)
                servo.ChangeDutyCycle(0)
                
                appliance.previous_state = appliance.state
                db.session.commit()

def set_gpio_appliances_from_scheduler(appliances, appliances_state) -> None:
    print(time.strftime("%H:%M:%S", time.localtime()), appliances_state)
    for appliance in appliances:
        if appliance["running_state"] == "continuous":
            GPIO.setup(appliance["pin_num"], GPIO.OUT)
            energy_state = GPIO.HIGH
            if int(appliances_state) >= 1:
                energy_state = GPIO.LOW
            GPIO.output(appliance["pin_num"],energy_state)

def initialize_schedulers(schedulers) -> None:
    for scheduler in schedulers:
        if scheduler.state != 0:
            add_scheduler(scheduler)
        
def remove_scheduler(scheduler) -> None:
    if cron_scheduler.get_job(scheduler.name):
        print("Removeing scheduler")
        cron_scheduler.remove_job(scheduler.name)
        
def add_scheduler(scheduler) -> None:
    # TODO: Schedulers should have priority otherwise there is no strict definition of which scheduler should be first, hence disorder happens
    if not cron_scheduler.get_job(scheduler.name):
        print("Adding new scheduler")
        # Mapping Applications list to dict(DAO -> DTO) 
        # becasue sessions are not possible to be controlled
        # inside a job 
        # If changes to are made to the Appliaction Model, this code
        # may break!!!
        print(scheduler)
        appliances = []
        for appliance in scheduler.__dict__["appliances"]:
            appliances.append({
                "running_state": appliance.running_state,
                "pin_num": appliance.pin_num
            })
        dict_args = {cron_time_list[i]: val for i, val in enumerate(scheduler.cron.split())}
        cron_scheduler.add_job(func=set_gpio_appliances_from_scheduler, id=scheduler.name, trigger="cron", args=[appliances, scheduler.__dict__["appliance_state"]], **dict_args)
    

def intialize_app_cron_jobs():
    """Execute cron tasks"""
    session = Session(engine)
    schedulers = session.query(Scheduler).all()
    initialize_schedulers(schedulers)
    session.close()

cron_scheduler.start()
atexit.register(lambda: cron_scheduler.shutdown())