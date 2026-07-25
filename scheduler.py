import schedule
import time
import subprocess

print("=" * 60)
print("⏰ AI Trading Scheduler Started")
print("=" * 60)

def run_manager():
    print("\n🚀 Running Manager AI...\n")

    subprocess.run([
        "py",
        "-m",
        "manager_ai.manager_ai"
    ])

# Run immediately once
run_manager()

# Then run every hour
schedule.every(1).hours.do(run_manager)

while True:
    schedule.run_pending()
    time.sleep(1)