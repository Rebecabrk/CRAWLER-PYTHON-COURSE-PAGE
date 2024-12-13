import os, sys, re
from bs4 import BeautifulSoup
from HTTPxModule import RequestWebPage, RequestPythonCoursePage

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
    
for lab_number, anchor in enumerate(filtered_a_tags):

    link = base_url + anchor['href']
    lab_page = RequestWebPage(link)
    lab_content = lab_page.get_web_page()

    soup = BeautifulSoup(lab_content, 'html.parser')
    main = soup.find('main')
    li = main.select('ol > li')

    if not os.path.exists(f'lab{lab_number + 2}'):
        os.mkdir(f'lab{lab_number + 2}')
        with open(f'lab{lab_number + 2}/lab{lab_number + 2}.py', 'w') as f:
            for i in range(len(li)):
                exercise_statement = f'"""\n{li[i].text.replace("\n", "")}\n"""\n'
                words = exercise_statement.split()
                lines = [' '.join(words[i:i+15]) for i in range(0, len(words), 15)]
                exercise_statement = '\n'.join(lines)
                exercise_statement = exercise_statement.replace('"""', f'"""\n')
                f.write(exercise_statement)

                if re.search(r'\bclass\b', exercise_statement):
                    pattern = r'(?<!\.\s)(\b[A-Z][a-zA-Z]*)'
                    class_names = re.findall(pattern, exercise_statement)
                    class_names = [n for n in class_names if n != 'Write' and n != 'Create' and n != 'Python' and n != 'None' and n != 'Design' and n != 'NxM' and len(n) > 1]

                    if lab_number + 2 == 5 and i == len(li) - 1:
                        class_names.append('Matrix')

                    for class_name in class_names:
                        exercise_class = f'class {class_name}:\n    pass\n'
                        f.write(exercise_class)
                else:
                    exercise_function = f'def ex{i+1}():\n    pass\n'
                    f.write(exercise_function)
        print(f'Lab {lab_number + 2} created.')
    else:
        print(f'Lab {lab_number + 2} already exists.')
