try:
        import RPi.GPIO as GPIO
        from time import sleep



        leds = [17, 27, 22, 5, 6, 26]

        GPIO.setmode(GPIO.BCM)
         
        GPIO.setup(leds, GPIO.OUT)

        GPIO.output(leds, GPIO.HIGH)
        GPIO.output(leds[5], GPIO.OUT)

        # Sequentially turn off the green LED's over a time period of 8 seconds
        # After the first five LED's turn off, turn on the red LED
        for i in range(6):
                if i <= 4:
                        sleep(1.6)
                        GPIO.output(leds[i], GPIO.OUT)
                        
                else:
                        
                        GPIO.output(leds[5], GPIO.HIGH)
                        sleep(2)
                
        GPIO.cleanup()


except:
        pass

