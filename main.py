import voice_handler as vh
import logging
logging.basicConfig(filename='DesktopAssistant.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger("comtypes.client._code_cache").setLevel(logging.ERROR) # Suppress INFO messages from comtypes.client._code_cache logger


def main():
    try:
        vh.listen(True)
    except Exception as e:
        print(f'Error: {e}')
        logging.error(e)


if __name__ == '__main__':
    main()