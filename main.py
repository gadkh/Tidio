from app.client import TidioClient
from configuration.conf import TOKEN


def main():
    client = TidioClient(token=TOKEN)
    client.run()


if __name__ == '__main__':
    main()
