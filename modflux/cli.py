import argparse

def download_command(args):
    """Handle the download subcommand"""
    nxm = args.nxm
    print(f"Downloading with NXM: {nxm}")
    # Add your download logic here

def import_command(args):
    """Handle the import subcommand"""
    archive = args.archive
    print(f"Importing archive: {archive}")
    # Add your import logic here

def main():
    # Create the main parser
    parser = argparse.ArgumentParser(description="CLI tool for downloading and importing")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create parser for the "download" command
    download_parser = subparsers.add_parser('download', help='Download command')
    download_parser.add_argument('--nxm', required=True, help='NXM parameter for download')
    
    # Create parser for the "import" command
    import_parser = subparsers.add_parser('import', help='Import command')
    import_parser.add_argument('--archive', required=True, help='Archive to import')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute appropriate command
    if args.command == 'download':
        download_command(args)
    elif args.command == 'import':
        import_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
