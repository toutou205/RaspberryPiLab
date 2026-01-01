import sys
import os
import traceback

# Add src to path exactly as the main script does
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

print(f"sys.path: {sys.path}")

print("Attempting to import epd2in7b...")
try:
    import epd2in7b
    print("SUCCESS: epd2in7b imported")
    
    print("Attempting to create EPD object...")
    epd = epd2in7b.EPD()
    print("SUCCESS: EPD object created")
    
    print("Attempting EPD init...")
    # This might interact with hardware
    if epd.init() == 0:
        print("SUCCESS: EPD init returned 0")
    else:
        print("FAILURE: EPD init returned non-zero")
        
except Exception as e:
    print(f"FAILURE: {e}")
    traceback.print_exc()
