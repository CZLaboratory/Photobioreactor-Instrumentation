##Guarda en archivo cada dia 
import time
import datetime

#Variables a guardar
algoethash=10
diffethash=5
coinethash=89
dayEUethash=5.2
#mainname="bio"
data=10
   
def savedata(direct, mainname, datain):
    ts = time.time()
    h = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S') #Formato de hora
    d = datetime.datetime.fromtimestamp(ts).strftime('%d_%m_%Y') #Formato de fecha

    # Write on file, mientras se llame igual va a rellenar, cuando se llame diferente genera un nuevo archivo y se mantiene el ciclo
    with open(direct+'/'+mainname+'_{}.txt'.format(d), 'a') as profit:
        profit.write(','.join([str(x) for x in [d, h, datain,'\n']]))
    
    #print("data saved")
    #time.sleep(1)  ##save time
    
#while True:
#    savedata(data)