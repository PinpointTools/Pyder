import src.interactive as init
import src.print as print

if __name__ == "__main__":
    try:
        init.start()
    except KeyboardInterrupt:
        print.warning("Keyboard interuption. Exiting...")