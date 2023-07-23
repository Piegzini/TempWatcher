import subprocess
import redis
import schedule
import time
from gpiozero import CPUTemperature

def get_cpu_temperature():
    try:
        # Run the vcgencmd measure_temp command and capture the output
        result = CPUTemperature()
        temperature_output = result.stdout.strip()

        print(temperature_output)

        # Extract the temperature value from the output

        return temperature_output
    except Exception as e:
        print("Error getting CPU temperature:", e)
        return None


def add_temperature_to_redis(redis_host, redis_port, temperature):
    try:
        # Connect to the Redis server
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

        # Add the temperature entry to the Redis database
        time_stamp = time.time()
        redis_client.set(time_stamp, temperature)
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
    redis_host = 'redisdatabase'
    redis_port = 6379

    measure_and_store_temperature(redis_host, redis_port)
    # Schedule the measure_and_store_temperature function to run every 10 minutes
    # schedule.every(10).minutes.do(measure_and_store_temperature, redis_host, redis_port)
    #
    # while True:
    #     # Run the scheduled tasks
    #     schedule.run_pending()
    #     time.sleep(1)
