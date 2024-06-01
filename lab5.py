import multiprocessing as mp
import time


def f(x):
    time.sleep(6)
    return x > 0

def g(x):
    time.sleep(7)
    return x < 0


def process_function(func, x, q, name):
    try:
        result = func(x)
        q.put((name, result))
    except Exception as e:
        q.put((name, e))


def main(x):
    q = mp.Queue()

    f_process = mp.Process(target=process_function, args=(f, x, q, 'f'))
    g_process = mp.Process(target=process_function, args=(g, x, q, 'g'))

    f_process.start()
    g_process.start()

    results = {}
    dont_ask = False  
    continue_computation = True
    ask_interval = 10  # Інтервал юзера у секундах
    last_ask_time = time.time()

    while continue_computation:
        current_time = time.time()

        if not dont_ask and current_time - last_ask_time > ask_interval:
            last_ask_time = current_time
            answer = input("Do you want to continue? [ y / n / d(don't ask me again) ]: ")
            if answer == 'n':
                print('Program stopped by user')
                f_process.terminate()
                g_process.terminate()
                f_process.join()
                g_process.join()
                return
            elif answer == 'd':
                print('Program will not ask again')
                dont_ask = True

        try:
            name, value = q.get_nowait()
            if isinstance(value, Exception):
                print(f"Function {name} raised an exception: {value}")
                continue
            print(f"Function {name} returned: {value}")
            results[name] = value

            # Логіка Кліні: x || true == true
            if 'f' in results and results['f']:
                print('f(x) || g(x) result: True')
                break
            if 'g' in results and results['g']:
                print('f(x) || g(x) result: True')
                break

            # Логіка Кліні: якщо обидві функції повернули результат
            if 'f' in results and 'g' in results:
                logic_or_result = results['f'] or results['g']
                print(f"f(x) || g(x) result: {logic_or_result}")
                break  
        except mp.queues.Empty:
            continue

    f_process.terminate()
    g_process.terminate()
    f_process.join()
    g_process.join()


if __name__ == '__main__':
    x = int(input("Enter value for x: "))
    main(x)
