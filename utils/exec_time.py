from datetime import datetime


def exec_time_wrapper(original_function):
    def new_function(*args, **kwargs):
        start_time = datetime.now()

        result = original_function(*args, **kwargs)

        end_time = datetime.now()
        print(f'Время выполнения: {end_time - start_time}')

        return result

    # Return the new function
    return new_function