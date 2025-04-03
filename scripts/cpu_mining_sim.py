import math
import multiprocessing
import argparse
from itertools import count

def cpu_intensive_task():
    
    for n in count(start=1):
        
        math.factorial(100000)
        
        
        math.exp(n) ** math.pi
        
        
        sum(math.sqrt(i) for i in range(1000000))

def main(num_processes):
    print(f"🚀 Starting CPU stress test with {num_processes} processes...")
    print("⚠️ Warning: This will significantly increase CPU usage!")
    print("Press Ctrl+C to stop\n")

    
    pool = multiprocessing.Pool(processes=num_processes)
    
    try:
        
        pool.map_async(lambda x: cpu_intensive_task(), range(num_processes))
        while True:
            pass  # Keep main thread alive
    except KeyboardInterrupt:
        print("\n🛑 Stopping CPU stress test...")
        pool.terminate()
        pool.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CPU Mining Simulator')
    parser.add_argument('-p', '--processes', type=int, default=multiprocessing.cpu_count(),
                       help='Number of parallel processes (default: all cores)')
    args = parser.parse_args()

    main(args.processes)
# This script is for educational purposes only. Use it responsibly and legally.
# Port scanning Script - by Cristhian Zamora
