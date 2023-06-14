import subprocess

PROCESS = []

while True:
    ANSWER = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')

    if ANSWER == 'q':
        break
    elif ANSWER == 's':
        PROCESS.append(subprocess.Popen('python server.py -p 8076 -a 127.0.0.1', shell=True))
        for i in range(5):
            PROCESS.append(subprocess.Popen(f'python3 client.py 127.0.0.1 8076 -n test{i}', shell=True))
    elif ANSWER == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()