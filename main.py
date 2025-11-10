import utils.constants as consts
from utils.data_loader import load_data


if __name__ == "__main__":
    status = load_data([consts.COMPRESSOR_TABLE])
    print(status)