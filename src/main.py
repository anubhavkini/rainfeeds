# main.py
import argparse
from src.commands import synchronise, list, add, remove, edit


def main():
    parser = argparse.ArgumentParser(
        prog="rainfeeds", description="Send entries from RSS and Atom feeds to Raindrop")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # Define list command
    subparsers.add_parser("ls", help="List feeds")

    # Define add command
    parser_add = subparsers.add_parser("add", help="Add a new feed")
    parser_add.add_argument("url", help="URL of the RSS/Atom feed")
    parser_add.add_argument("-t", "--title", help="Title of the feed")
    parser_add.add_argument("-c", "--category", help="Category of the feed")

    # Define remove command
    parser_remove = subparsers.add_parser("rm", help="Remove a feed")
    parser_remove.add_argument("url", help="URL of the RSS/Atom feed")

    # Define edit command
    parser_edit = subparsers.add_parser("edit", help="Edit a feed")
    parser_edit.add_argument("url", help="URL of the RSS/Atom feed")
    parser_edit.add_argument("-t", "--title", help="New title of the feed")
    parser_edit.add_argument(
        "-c", "--category", help="New category of the feed (leave empty to remove)")

    # Define synchronise command
    subparsers.add_parser(
        "sync", help="Synchronise new entries to Raindrop")

    args = parser.parse_args()

    # Route to appropriate command
    if args.command == "ls":
        list.execute(args)
    elif args.command == "add":
        add.execute(args)
    elif args.command == "rm":
        remove.execute(args)
    elif args.command == "edit":
        edit.execute(args)
    elif args.command == "sync":
        synchronise.execute(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
