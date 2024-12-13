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
                f.write(exercise_statement)
                exercise_function = f'def ex{i+1}():\n    pass\n'
                f.write(exercise_function)
        print(f'Lab {lab_number + 2} created.')
    else:
        print(f'Lab {lab_number + 2} already exists.')
