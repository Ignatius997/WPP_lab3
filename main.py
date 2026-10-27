from args import parse_arguments
import file_manager

def main():
    args, action, file_format = parse_arguments() 
    
    paths = file_manager.generate_paths(args)
    
    if action == 't':
        file_manager.create_files(paths, file_format)
    elif action == 'o':
        file_manager.read_files(paths, file_format)

    print(args)

if __name__ == '__main__':
    main()
