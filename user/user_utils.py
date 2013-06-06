import hashlib
import random

def getNewAPIKey():
	return hashlib.sha224( str(random.getrandbits(256)) ).hexdigest()

def main():
    print getNewAPIKey()

if __name__ == '__main__':
    main()