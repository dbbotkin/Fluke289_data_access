import serial
import time

ser = serial.Serial()

# Setup logging
ser.port = '/dev/cu.usbserial-AC00FZQJ'    # MY Serial port; find your . . .
logging_period = 1 # seconds
no_of_records = 5 # how many records to record


# Serial port setup and open
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.timeout = 0.1  # seconds
try:
    ser.open()
except:
    print("Cannot open serial port...")
    exit()


def do_recordings(records):
  nb_recordings = int(qsls()['nb_recordings'])
  if len(records) != 0:
    if records[0] == 'list':
      print ('Index','Name','Start','End','Duration','Measurements',sep=sep)
      for i in range (1,nb_recordings + 1):
        recording = qrsi(str(i-1))
        #print ('recording',recording)
        seconds = time.mktime(recording['end_ts']) - time.mktime(recording['start_ts'])
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        name = recording['name'].decode()
        sample_interval = recording['sample_interval']
        num_samples = recording['num_samples']
        debut_d = time.strftime('%Y-%m-%d %H:%M:%S',recording['start_ts'])
        fin_d = time.strftime('%Y-%m-%d %H:%M:%S',recording['end_ts'])
        print(f'{i:d}',name,debut_d,fin_d,f'{d:02d}:{h:02d}:{m:02d}:{s:02d}',num_samples,sep=sep)
      sys.exit()
  interval = []
  for i in range(1,nb_recordings + 1):
    interval.append(str(i))
  found = False
  if len(records) == 0:
    series = interval
  else:
    series = records

  for i in series:
    if i.isdigit():
      recording = qrsi(str(int(i)-1))
      #print ('recording digit',recording)
      seconds = time.mktime(recording['end_ts']) - time.mktime(recording['start_ts'])
      m, s = divmod(int(seconds), 60)
      h, m = divmod(m, 60)
      d, h = divmod(h, 24)
      duration = f'{d:02d}:{h:02d}:{m:02d}:{s:02d}'
      print ('Index %s, Name %s, Start %s, End %s, Duration %s, Measurements %s' \
            % (str(i), (recording['name']).decode(),time.strftime('%Y-%m-%d %H:%M:%S',recording['start_ts']),time.strftime('%Y-%m-%d %H:%M:%S',recording['end_ts']), duration, recording['num_samples']))
      print ('Start Time','Primary','','Maximum','','Average','','Minimum','','#Samples','Type',sep=sep)

      for k in range(0,recording['num_samples']):
        measurement = qsrr(str(recording['reading_index']), str(k))
        #print ('measurement',measurement)
        duration = str(round(measurement['readings']['AVERAGE']['value'] \
            / measurement['duration'],measurement['readings']['AVERAGE']['decimals'])) \
            if measurement['duration'] != 0 else 0
        print (time.strftime('%Y-%m-%d %H:%M:%S', measurement['start_ts']), \
              str(measurement['readings2']['PRIMARY']['value']), \
              measurement['readings2']['PRIMARY']['unit'], \
              str(measurement['readings']['MAXIMUM']['value']), \
              measurement['readings']['MAXIMUM']['unit'], \
              duration, \
              measurement['readings']['AVERAGE']['unit'], \
              str(measurement['readings']['MINIMUM']['value']), \
              measurement['readings']['MINIMUM']['unit'], \
              str(measurement['duration']),sep=sep,end=sep)
        print ('INTERVAL' if measurement['record_type'] == 'INTERVAL' else measurement['stable'])
      print
      found = True
    else:
      for j in interval:
        recording = qrsi(str(int(j)-1))
        #print ('recording non digit',recording)
        if recording['name'] == i.encode():
          found = True
          print ('Index %s, Name %s, Start %s, End %s, Duration %s, Measurements %s' \
            % (str(j), (recording['name']).decode(),time.strftime('%Y-%m-%d %H:%M:%S',recording['start_ts']),time.strftime('%Y-%m-%d %H:%M:%S',recording['end_ts']), duration, recording['num_samples']))
          print ('Start Time','Primary','','Maximum','','Average','','Minimum','','#Samples','Type',sep=sep)
          for k in range(0,recording['num_samples']):
            measurement = qsrr(str(recording['reading_index']), str(k))
#            print ('measurement',measurement)
            duration = str(round(measurement['readings']['AVERAGE']['value'] \
                / measurement['duration'],
                  measurement['readings']['AVERAGE']['decimals'])) \
                if measurement['duration'] != 0 else 0
            print (time.strftime('%Y-%m-%d %H:%M:%S', measurement['start_ts']), \
                  str(measurement['readings2']['PRIMARY']['value']), \
                  measurement['readings2']['PRIMARY']['unit'], \
                  str(measurement['readings']['MAXIMUM']['value']), \
                  measurement['readings']['MAXIMUM']['unit'], \
                  duration, \
                  measurement['readings']['AVERAGE']['unit'], \
                  str(measurement['readings']['MINIMUM']['value']), \
                  measurement['readings']['MINIMUM']['unit'], \
                  str(measurement['duration']),sep=sep,end=sep)
            print ('INTERVAL' if measurement['record_type'] == 'INTERVAL' else measurement['stable'])
          print
          break
  if not found:
    print ("Saved names not found")
    sys.exit()

