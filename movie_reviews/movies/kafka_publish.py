from kafka import KafkaProducer


def get_producer():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    return producer


def publish(producer,movie,review,score):
    topic_name = 'second_topic'

    data = {
        'review':review.content,
        'label':review.label,
        'score':score,
        'movie':movie.title
    }

    message = str(data).encode()
    producer.send(topic_name, message)

    