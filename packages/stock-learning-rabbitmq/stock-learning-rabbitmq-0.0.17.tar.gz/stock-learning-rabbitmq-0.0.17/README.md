# stock-learning-rabbitmq

### Rodando o projeto
Tendo o node instalado na sua máquina, basta rodar um `python -m pip install pika`

### Publicando uma versão no PyPI

- Inicialmente deve-se rodar os dois comandos abaixo, para instalar as bibliotecas que publicam o código ao PyPI
- `python -m pip install --user --upgrade setuptools wheel`
- `python -m pip install --user --upgrade twine`
- Logo em seguida devem ser rodados os dois comandos abaixo, para efetivamente gerar uma versão e upar ao PyPI
- `python setup.py sdist bdist_wheel`
- `python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*`
- Ao ser requisitado por credenciais, digite `__token__` no username, e requisite o token de acesso aos administradores do sistema
