import pika, os, sys
import Producer

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.queue_declare(queue= Producer.key)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
    channel.basic_consume(queue=Producer.queue_name,
                        auto_ack=True,
                        on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

