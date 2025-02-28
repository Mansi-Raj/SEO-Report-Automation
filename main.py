import subprocess

print("Step 1: Fetching SEO Data...")
subprocess.run(["python", "data_collection.py"])
print("Step 1: Fetching SEO Data completed")

print("\nStep 2: Generating SEO Report...")
subprocess.run(["python", "report_generator.py"])
print("Step 2: Generating SEO Report completed")

print("\nStep 3: Sending Report via Email...")
subprocess.run(["python", "report_sender.py"])
print("Step 3: Sending Report via Email completed")

print("\n All Steps Completed Successfully!")
