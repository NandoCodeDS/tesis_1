from pymodbus.client.sync import ModbusTcpClient
import math
import requests , json
import asyncio,time
from datetime import datetime, timedelta

import mysql.connector as sql
from BD import crear_registro, leer_registros, actualizar_registro, eliminar_registro
while True:
    leer_registros()
    
    class ConnectionModbusClient:
        def __init__(self,_host,_port, _timeout=3) -> None:
            self.ip= _host
            self.port= _port
            self.timeout= _timeout 
            self.client = ModbusTcpClient(host=self.ip, port=self.port, timeout=self.timeout)
            print("conec")
            self.client.connect()
            print("se conecto")
    
        
        def takeDataDevice(self,_address:str):
            print("inicio...")
            for i in range(0,100):
                a=1
                #print(self.client.read_holding_registers(address = 0x23 ,count = 1, unit=1))
                #print("="*30)
            AddressConst=[0x23,0x24] #    [23->[DPT, DCT]], [[24->[DPQ]]
            arrayConst=[self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0] for i in AddressConst] #constantes
            #print("arrayConst",arrayConst,len(arrayConst))
    
            U=[0x25,0x26,0x27,0x28,0x29,0x2A]
            arrayV= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/10 for i in U] # voltaje
            #print("arrayV",arrayV,len(arrayV))
    
    
            I=[0x2B,0x2C,0x2D]
            arrayI= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/100 for i in I] # corriente
            #print("arrayI",arrayI,len(arrayI))
    
    
            P=[0x2E,0x2F,0x30,0x31]
            arrayP= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/100 for i in P] # potencia activa
            #print("arrayP",arrayP,len(arrayP))
    
            Q=[0x32,0x33,0x34,0x35]
            arrayQ= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/100 for i in Q] # potencia reactiva
            #print("arrayQ",arrayQ,len(arrayQ))
    
            PF=[0x36,0x37,0x38,0x39]
            arrayPF= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/1000 for i in PF] # factor de potencia
            #print("arrayPF",arrayPF,len(arrayPF))
    
            S=[0x3A,0x3B,0x3C,0x3D]
            arrayS= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/100 for i in S] # potencia aparente
            #print("arrayS",arrayS,len(arrayS))
    
            F=[0x3E]
            arrayF= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0]/100 for i in F] # Frecuentcia
            #print("arrayF",arrayF,len(arrayF))
    
            WE=[0x3F,0x40,0x41,0x42,0x43,0x44,0x45,0x46,0x47,0x48,0x49,0x4A,0x4B,0x4C,0x4D,0x4E]
            arrayWE= [self.client.read_holding_registers(address = i ,count = 1, unit=1).registers[0] for i in WE] #demas variables
            #print("arrayWE",arrayWE,len(arrayWE))
    
    
            AngulosFactoresPotencia=self.convertirAnguloPotencia(arrayPF)
    
    
            array= [arrayConst,arrayV,arrayI,arrayP,arrayQ,arrayPF,arrayS,arrayF,arrayWE,AngulosFactoresPotencia]
            #print(array)#variables
            now = str(datetime.utcnow())
            address= "0x4F864643d41477787093b5028b2A41B04429568C"
    
            Voltaje = {"node": _address,"timestamcreation": now,"va": array[1][0],"vb": array[1][1],"vc": array[1][2]}
            Corriente = {"node": _address,"timestamcreation": now,"ia": array[2][0],"ib": array[2][1],"ic": array[2][2]}
            PotenciaActiva = {"node": _address,"timestamcreation": now,"pa": array[3][0],"pb": array[3][1],"pc": array[3][2]}
            PotenciaReactiva = {"node": _address,"timestamcreation": now,"qa": array[4][0],"qb": array[4][1],"qc": array[4][2]}
            PotenciaAparente = {"node": _address,"timestamcreation": now,"sa": array[5][0],"sb": array[5][1],"sc": array[5][2]}
            FactoresPotencia = {"node": _address,"timestamcreation": now,"pfa": array[6][0],"pfb": array[6][1],"pfc": array[6][2]}
            Frecuencia = {"node": _address,"timestamcreation": now,"f": array[7][0]}
            AngulosFactoresPotencia = {"node": _address,"timestamcreation": now,"Phia": array[9][0],"Phib": array[9][1],"Phic": array[9][2]}
            
            print("Meloooooo")
            print(array[1][0],array[7][0])
            nombre_a_eso=[array[1][0],array[7][0]]
            print(nombre_a_eso)
    
            array= [Voltaje,Corriente,PotenciaActiva,PotenciaReactiva,PotenciaAparente,FactoresPotencia,Frecuencia,AngulosFactoresPotencia ]
            
            
            crear_registro(nombre_a_eso)
    
            return array
            # return [arrayConst,arrayV,arrayI,arrayP,arrayQ,arrayPF,arrayS,arrayF,arrayWE,angulo_Potencia]
            #registros = array[0]
            
    
    
            # mycursor = conexion.cursor()
            # insert = "INSERT INTO monitor (voltaje,frecuencia) VALUES (%s, %s)"
            # val = registros
            # mycursor.executemany(insert, val)
    
    
        def convertirAnguloPotencia(self,data):
            angulo_Potencia= []
            try:
                angulo_Potencia= []#    [math.acos( i )*57.2958 for i in arrayPF]
                for i in data:
                    try:
                        angulo_Potencia.append(i*57.2958)
                    except:
                        angulo_Potencia.append(0)
    
                return angulo_Potencia
            except:
                return [0,0,0,0]
    
    
    
        def dataSend(self,__address:str):
            data= self.takeDataDevice(__address)
            # print(data)
            
            return data
            
    
    
    #dispositivos modbus
    config = [
        #{"host": "192.168.20.200", "port":502},#Aria 2G
        {"host": "192.168.91.63", "port":502},
        # {"host": "", "port":},
    ]
    
    
    
    arrayObj= [ConnectionModbusClient(_host=i["host"],_port=i["port"],_timeout=2) for i in config]
    
    #data= arrayObj[0].sendDataApi()
    data= arrayObj[0].takeDataDevice("sdfsdf")
    # conexion.commit()
    # conexion.close()
    
    # print(data)