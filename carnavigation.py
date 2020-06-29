import pandas as pd
from json import loads
import pymysql
from math import radians, cos, sin, asin, sqrt
from mysql_connect import db

class car:

    def __init__(self,data):
        location = loads(data)
        db_obj = db()
        db_obj.insertTable('car',location)
        print(location)
        #df = pd.read_sql('SELECT * FROM car', con=connection)
        df = db_obj.getAll()
        car1=df[df.uid==location['uid']]
        car2=df[df.uid!=location['uid']]
        self.value = self.processData(car1,car2)
        print("valor: ", self.value)
    
    def __str__(self):
        return str(self.value)

    def processData(self,car1,car2):
        #connection = pymysql.connect(host='localhost', user='pi', password='raspberry', db='carnavigation', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        #df = pd.read_sql('SELECT * FROM car', con=connection)
        #car1=df[df.uid=='100']
        #car2=df[df.uid!='100']
        if(len(car2) > 0):
            for index, row in car2.iterrows():
                    if float(car1['speed']) < 90:
                        radius_max = 0.30 # kilometros
                    else:
                        radius_max = 0.40
                    radius_min = 0.12
                    distance = self.haversine(float(car1['latitude']), float(car1['longitude']), float(row.latitude), float(row.longitude))	#Distancia entre los dos coches
                    print (distance)
                    if distance <= radius_max and distance > radius_min:
                        if self.nearby(float(car1['latitude']), float(car1['longitude']), float(car1['latitude_old']), float(car1['longitude_old']), float(row.latitude), float(row.longitude), float(row.latitude_old), float(row.longitude_old)):
                            print ('near')
                            carConfiguration = filter(lambda y: y.uid == x.uid, Configuration.objects.all())
                            direction = self.get_direction(float(car1['latitude']), float(car1['longitude']), float(row.latitude), float(row.longitude), float(car1['latitude_old']), float(car1['longitude_old']), float(row.latitude_old), float(row.longitude_old))
                            print (direction)
                            isBehind = self.behind(float(car1['latitude']), float(car1['longitude']), float(row.latitude), float(row.longitude), float(car1['latitude_old']), float(car1['longitude_old']), direction)
                            #self.send_alert(x.tokenId, isBehind, carConfiguration[0], distance, car1['speed'],direction, car1['uid'])
                        else:
                            print ('far')
                    else:
                        print ('lejos')
                    return str(distance)

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        cálculo de la distancia de círculo máximo entre dos puntos de un globo
        sabiendo su longitud y su latitud.
        """
        # decimales a radianes
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radio de la tierra en kilometros.
        return c * r

    def nearby(self, lat1, lon1, lat1_old, lon1_old, lat2, lon2, lat2_old, lon2_old):
        print(lat1, lon1, lat1_old, lon1_old, lat2, lon2, lat2_old, lon2_old)
        """
        Comprobacion de si el coche2 esta mas cerca del coche1
        que en un momento anterior
        """
        dis = haversine(lat2,lon2,lat1, lon1)
        dis_old = haversine(lat2_old,lon2_old,lat1_old,lon1_old)
        print(dis)
        print(dis_old)	
        if(dis < dis_old):
            return True
        else:
            return False


    def behind(self, lat1, lon1, lat2, lon2, lat1_old, lon1_old, direction):
        """
        Comprobacion de si el coche2 esta detras del coche1
        """
        if(direction == 0):
            d_lat1 = lat1-lat1_old
            d_lon1 = lon1-lon1_old
            d_lat = lat2-lat1
            d_lon = lon2-lon1

            if(d_lat1 > 0 and d_lon1 > 0): 	
                if(d_lat > 0 and d_lon > 0):
                    return True
                else:
                    return False
            elif(d_lat1 < 0 and d_lon1 < 0):
                if(d_lat < 0 and d_lon < 0):
                    return True
                else:
                    return False
            elif(d_lat1 > 0 and d_lon1 < 0):
                if(d_lat > 0 and d_lon < 0):
                    return True
                else:
                    return False
            elif(d_lat1 < 0 and d_lon1 > 0): 		
                if(d_lat < 0 and d_lon > 0):
                    return True
                else:
                    return False	
        else:
            return None


    def get_direction(self, lat1, lon1, lat2, lon2, lat1_old, lon1_old, lat2_old, lon2_old):
        """
        Calculo de la direccion de un coche respecto a otro
        0 -> Misma direccion
        1 -> Direcciones opuestas
        2 -> Direcciones que se cruzan
        """
        d_lat1 = lat1-lat1_old
        d_lon1 = lon1-lon1_old
        d_lat2 = lat2-lat2_old
        d_lon2 = lon2-lon2_old

        if(d_lat1 > 0 and d_lon1 > 0):
            if(d_lat2 < 0 and d_lon2 < 0):
                return 1
            elif(d_lat2 > 0 and d_lon2 < 0):
                return 2
            elif(d_lat2 < 0 and d_lon2 > 0):
                return 2
            elif(d_lat2 > 0 and d_lon2 > 0):
                return 0
        elif(d_lat1 < 0 and d_lon1 < 0):
            if(d_lat2 > 0 and d_lon2 > 0):
                return 1
            elif(d_lat2 > 0 and d_lon2 < 0):
                return 2
            elif(d_lat2 < 0 and d_lon2 > 0):
                return 2
            elif(d_lat2 < 0 and d_lon2 < 0):
                return 0
        elif(d_lat1 > 0 and d_lon1 < 0):
            if(d_lat2 > 0 and d_lon2 > 0):
                return 2
            elif(d_lat2 < 0 and d_lon2 < 0):
                return 2
            elif(d_lat2 < 0 and d_lon2 > 0):
                return 1
            elif(d_lat2 > 0 and d_lon2 < 0):
                return 0
        elif(d_lat1 < 0 and d_lon1 > 0):
            if(d_lat2 > 0 and d_lon2 > 0):
                return 2
            elif(d_lat2 < 0 and d_lon2 < 0):
                return 2
            elif(d_lat2 > 0 and d_lon2 < 0):
                return 1
            elif(d_lat2 < 0 and d_lon2 > 0):
                return 0

    def send_alert(self, to, behind, carConfiguration, distance, speed, direction, uid):
        if(direction == 0 and carConfiguration.alertAccident):
            if(behind != None):
                if(behind):
                    body = {"to": to, "data": {"title": "ALERTA POR POSIBLE COLISION TRASERA","body": "Un coche a " + str(distance*1000)[:3] + " metros se aproxima a " + speed + " k/h por detras"}}
                    postNotification(body, uid)

        elif(direction == 1 and carConfiguration.alertAccident):
            body = {"to": to, "data": {"title": "ALERTA POR POSIBLE COLISION DELATERA","body": "Un coche a " + str(distance*1000)[:3] + " metros se aproxima a " + speed + " k/h por delante"}}
            postNotification(body, uid)

        elif(direction == 2 and carConfiguration.alertHelp):
            body = {"to": to, "data": {"title": "ALERTA POR VEHICULO APROXIMANDOSE A INTERSECCION","body": "Un coche a " + str(distance*1000)[:3] + " metros se aproxima a " + speed + " k/h en la interseccion"}}
            postNotification(body, uid)

    def postNotification(body, uid):
        print (body)

        headers = {"content-type": "application/json", "Authorization": "key=AAAApRo1WOU:APA91bFro_aJI-puTK_zRwdMtPnNxgfQPbrC0QE6qaMjpHHAvYXnhhAUI3Pposz8fQJfE3GgxXv1J0i1SsmnHFSETOZQ-0V6QjuUZaQRij9UwE1St7C1I7xMcLtNApGe0_NPc0EkNBgG"}
        url = "https://fcm.googleapis.com/fcm/send"
        requests.post(url, data = json.dumps(body), headers=headers)
        credential = filter(lambda y: y.tokenId == body['to'], Credential.objects.all())
        Alert.objects.create(sender = uid, receiver = credential[0].uid,title = body['data']['title'], description = body['data']['body']).save()
	