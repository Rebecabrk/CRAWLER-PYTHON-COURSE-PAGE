import os, sys, re
from bs4 import BeautifulSoup
from HTTPxModule import RequestWebPage, RequestPythonCoursePage

exercise_lenghts = 0

def write_function_name(statement, exercise_number, file):
    if re.search(r'\bclass\b', statement):
        pattern = r'(?<!\.\s)(\b[A-Z][a-zA-Z]*)'
        class_names = re.findall(pattern, statement)
        class_names = [n for n in class_names if n != 'Write' and n != 'Create' and n != 'Python' and n != 'None' and n != 'Design' and n != 'NxM' and len(n) > 1]

        if class_names == []:
            class_names.append('Matrix')

        for class_name in class_names:
            exercise_class = f'class {class_name}:\n    pass\n'
            file.write(exercise_class)
    elif re.search(r'\bThe\s(\w+)\sfunction\b', statement):
        function_name = re.search(r'\bThe\s(\w+)\sfunction\b', statement).group().split()[1]
        exercise_function = f'def {function_name}():\n    pass\n'
        file.write(exercise_function)
    elif '(' in statement:
        pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\('
        function = re.search(pattern, statement)
        if function and function.group(1) != 'len':
            function_name = function.group(1)
        else:
            function_name = f'ex{exercise_number}'
        exercise_function = f'def {function_name}():\n    pass\n'
        file.write(exercise_function)
    else:
        exercise_function = f'def ex{exercise_number}():\n    pass\n'
        file.write(exercise_function)

def pretty_format_exercise_statement(statement):
    exercise_statement = f'"""\n{statement.replace("\n", "")}\n"""\n'
    words = exercise_statement.split()
    lines = [' '.join(words[i:i+15]) for i in range(0, len(words), 15)]
    exercise_statement = '\n'.join(lines)
    exercise_statement = exercise_statement.replace('"""', f'"""\n')
    return exercise_statement

def parse_ol_tag(ol_tag, index, file, pre_tag=None):
    global exercise_lenghts
    li = ol_tag.find_all('li')

    for i in range(len(li)):
        if index == 0:
            exercise_number = i + 1
        else:
            exercise_number = exercise_lenghts + i + 1
        statement = li[i].text
        if i == len(li) - 1 and pre_tag is not None:
            statement += ' ' + pre_tag.text
        file.write(pretty_format_exercise_statement(statement))
        write_function_name(statement, exercise_number, file)
        
    if index == 0:
        exercise_lenghts = len(li)
    else:
        exercise_lenghts += len(li)

if len(sys.argv) > 1 and sys.argv[1] == 'help':
    print('This script downloads the Python course page and all the labs from the course page.')
    print('Usage: python Template.py <directory_name>')
    sys.exit(0)
elif len(sys.argv) != 2:
    print('Invalid number of arguments. Use "python Template.py help" for more information.')
    sys.exit(1)
else:
    directory = sys.argv[1]
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f'Directory {directory} created.')
    os.chdir(directory)
    print(f'Changed directory to {directory}.')

python_webpage = RequestPythonCoursePage()
python_webpage_content = ''

try:
    python_webpage_content = python_webpage.get_web_page()
    print('Starting parsing html code of the main labs page...')
except ValueError as e:
    print(e)
    sys.exit(2)
    
soup = BeautifulSoup(python_webpage_content, 'html.parser')
main = soup.find('main')
filtered_a_tags = [a for a in main.find_all('a') if a.find_parent('h1') is None]

base_url = python_webpage.get_base_url()

print()
for lab_number, anchor in enumerate(filtered_a_tags):

    link = base_url + anchor['href']
    lab_page = RequestWebPage(link)
    lab_content = lab_page.get_web_page()

    soup = BeautifulSoup(lab_content, 'html.parser')
    main = soup.find('main')
   
    if not os.path.exists(f'lab{lab_number + 2}'):
        os.mkdir(f'lab{lab_number + 2}')
    
    with open(f'lab{lab_number + 2}/lab{lab_number + 2}.py', 'w') as f:
        for index, ol_tag in enumerate(main.find_all('ol')):
            if ol_tag.find_next_sibling('pre') is not None:   
                parse_ol_tag(ol_tag, index, f, pre_tag=ol_tag.find_next_sibling('pre'))
            else:
                parse_ol_tag(ol_tag, index, f)
        print('Lab', lab_number + 2, 'successfully created.') 

print()
print('All labs successfully created.')
sys.exit(0)
