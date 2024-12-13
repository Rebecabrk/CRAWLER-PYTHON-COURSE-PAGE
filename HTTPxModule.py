import httpx
import re

class RequestWebPage:
    """
    Clasa care permite obtinerea continutului unei pagini web.
    """
    def __init__(self, url):
        """
        Constructorul clasei RequestWebPage.
        :param url: URL-ul paginii web.
        """
        if RequestWebPage._check_url(url) == False:
            raise ValueError('URL is not valid.')
        self.url = url

    @staticmethod
    def _check_url(url):
        """
        Metoda care verifica daca un URL este valid.
        :param url: URL-ul care trebuie verificat.
        """
        pattern = re.compile(
            r'^(http?|https):\/\/' # protocoale acceptate: http, https
            r'([a-zA-Z0-9\-._~%]+|(\[[a-fA-F0-9:]+\])|(\b\d{1,3}(\.\d{1,3}){3}\b))' # domeniu sau adresa IP (v6 si v4)
            r'([0-9]{0,5})?' # port (optional)
            r'(\/[a-zA-Z0-9\-.~%]*)*' # cale (optional)
            r'(\?[;&a-zA-Z0-9\-.~%=_]*)*' # query string (optional)
            r'(\#.*)?$' # fragment (optional)
        )
        return pattern.match(url) is not None

    def get_web_page(self):
        """
        Metoda care obtine continutul paginii web,
        ridicand o exceptie in caz de eroare.
        """
        response = httpx.get(self.url)
        if response.status_code == httpx.codes.OK:
            return response.text
        else:
            raise ValueError(f'Error when trying to get the url: {response.reason_phrase}')
        
class RequestPythonCoursePage(RequestWebPage):
    """
    Clasa care permite obtinerea continutului paginii web a cursului de Python de la FII.
    """
    def __init__(self):
        """
        Constructorul clasei RequestPythonCoursePage.
        """
        super().__init__('https://gdt050579.github.io/python-course-fii/labs.html')
    
    def get_web_page(self):
        """
        Metoda care obtine continutul paginii web a cursului de Python de la FII.
        """
        return super().get_web_page()

    def get_base_url(self):
        """
        Metoda care returneaza URL-ul de baza al paginii web de python de la FII.
        """
        return 'https://gdt050579.github.io/python-course-fii/'
    

if __name__ == '__main__':
    try:
        python_webpage = RequestPythonCoursePage()
        text = python_webpage.get_web_page()
        with open('Resources/python_webpage.html', 'w') as f:
            f.write(text)
    except ValueError as e:
        print(e)
