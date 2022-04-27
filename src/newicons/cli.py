import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="Change file icons")
    parser.add_argument(
        "rootpath",
        type=str,
        help="directory to start in"
    )

    parser.add_argument(
        "--dumb",
        action="store_true",
        required=False,
        help="If dumb, does not check the time file was created"
    )

    parser.add_argument(
        "--nice",
        action="store_true",
        required=False,
        help="If nice, sets script to low priority"
    )

    return parser

def main():
    args = get_parser().parse_args()

    
