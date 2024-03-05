import pika
import pandas as pd
from random import randrange
from csv import reader
from time import sleep

filename = "Temperaturen.csv"

queue_name = 'hello'
user = "Derrick"
key = "hello"
csv_length = len(pd.read_csv(filename))

def main():
    while True:
        rdm = randrange(0, csv_length)
        def random_temp():
            with open(filename, newline='') as my_file:
                file_reader = reader(my_file, delimiter=',')

                for index, row in enumerate(file_reader):
                    if index == rdm:
                       
                        pos1 = row[0].find(';')
                        date = row[0][pos1+1 : pos1+17]
                        temp = row[0][pos1+18 : pos1+20]
            return date, temp

        date, temp = random_temp()
        payload = "%s %s %s" % (key, str(date), str(temp))
   
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)

            channel.basic_publish(exchange='',
                                routing_key=key,
                                body=payload)
            connection.close()
            print("\nHello %s, die Temperatur am %s betrug %s Grad Celsius." % (user, date, temp))

            sleep(5)
            
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            connection.close()

        except:
            print("\nOups! An Error occured...")
            connection.close()

if __name__ == "__main__":
        main()
        
