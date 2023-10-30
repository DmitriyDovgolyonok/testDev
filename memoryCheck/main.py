import psutil
import requests

threshold = 70
api_url = 'https://example.com/api/alarm'


def check_memory_usage():
    memory_percent = psutil.virtual_memory().percent
    print(memory_percent)
    if memory_percent > threshold:
        send_alarm()


def send_alarm():
    data = {'message': 'High memory usage alarm!'}
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        print('Alarm sent successfully')
    else:
        print(f'Failed to send alarm. Status code: {response.status_code}')


if __name__ == '__main__':
    while True:
        check_memory_usage()