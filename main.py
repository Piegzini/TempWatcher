import json
from datetime import datetime
import redis
import schedule
import time
from gpiozero import CPUTemperature


def get_cpu_temperature():
    try:
        # Run the vcgencmd measure_temp command and capture the output
        raw_output = CPUTemperature()
        temperature = raw_output.temperature

        return temperature
    except Exception as e:
        print("Error getting CPU temperature:", e)
        return None


def add_temperature_to_redis(redis_host, redis_port, temperature):
    try:
        # Connect to the Redis server
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

        data = {
            'time': str(datetime.now()),
            'temperature': temperature
        }

        # Convert the data to a JSON string
        json_data = json.dumps(data)

        # Add the JSON entry to the Redis database
        redis_client.rpush('temperatures', json_data)
        # Add the temperature entry to the Redis database
        print(f"Temperature entry added to Redis: {temperature}°C")
    except Exception as e:
        print("Error adding temperature to Redis:", e)


def measure_and_store_temperature(redis_host, redis_port):
    # Get the CPU temperature
    cpu_temperature = get_cpu_temperature()
    if cpu_temperature is not None:
        # Add the temperature entry to Redis
        add_temperature_to_redis(redis_host, redis_port, cpu_temperature)


if __name__ == "__main__":
    # Replace 'your_redis_host' and 'your_redis_port' with your Redis server details
    redis_host = 'localhost'

    # dev settings
    # redis_host = 'respberrypi.local'

    redis_port = 6379

    measure_and_store_temperature(redis_host, redis_port)
    # Schedule the measure_and_store_temperature function to run every 10 minutes
    schedule.every(10).minutes.do(measure_and_store_temperature, redis_host, redis_port)
    #
    while True:
        # Run the scheduled tasks
        schedule.run_pending()
        time.sleep(1)
