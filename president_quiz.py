import time

answer = input('Who was the first president of United States? ')

if answer.strip().lower() == 'george washington':
    print('checking...')
    time.sleep(3)
    print('correct!')
else:
    print('wrong!')
