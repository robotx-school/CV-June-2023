import subprocess

# Python-скрипт, который вы хотите выполнить
script_code = '''
import math
result = math.sqrt(16)
print result
'''

try:
	# Запуск скрипта и получение вывода
	result = subprocess.check_output(['python', '-c', script_code], universal_newlines=True)
except Exception as e:
	result = e

# Вывод результата
#print(result)