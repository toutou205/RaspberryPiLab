import sys
print("Checking hardware imports...")
try:
    import spidev
    print("SUCCESS: spidev imported")
    try:
        spi = spidev.SpiDev()
        spi.open(0, 0)
        print("SUCCESS: SPI device opened")
        spi.close()
    except Exception as e:
        print(f"FAILURE: SPI open failed: {e}")

    import gpiozero
    print("SUCCESS: gpiozero imported")
    
    # Try creating a dummy LED object to check pin access permissions
    try:
        from gpiozero import LED
        led = LED(17)
        print("SUCCESS: gpiozero LED(17) created")
        led.close()
    except Exception as e:
        print(f"FAILURE: gpiozero pin access failed: {e}")

except ImportError as e:
    print(f"FAILURE: Import error: {e}")
except Exception as e:
    print(f"FAILURE: Unexpected error: {e}")
