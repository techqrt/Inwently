#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# from kafka import KafkaAdminClient
# from kafka.admin import NewTopic

from biller.config import Configurations
# from kafka_consumer_producer.consumer import KafkaTopicConsumer


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biller.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
        



if __name__ == '__main__':
    main()
