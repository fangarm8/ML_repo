import os
def remove_empty_lines(lst_of_filenames):
    for file_path in lst_of_filenames:
        with open(file_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        modified_content = ' '.join(non_empty_lines)
        with open(file_path, 'w', encoding='utf-8') as outfile:
            outfile.write(modified_content)

root = '../data/web_pages/html_codes'
lst_filenames = [os.path.join(path, name) for path, subdirs, files in os.walk(root) for name in files]
remove_empty_lines(lst_filenames)

print("Пустые строки удалены.")