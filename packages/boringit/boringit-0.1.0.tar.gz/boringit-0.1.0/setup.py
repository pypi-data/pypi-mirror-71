# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boringit']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['boringit = boringit.boringit:main']}

setup_kwargs = {
    'name': 'boringit',
    'version': '0.1.0',
    'description': 'A tool to optimize git Add, Commit and Push routine.',
    'long_description': '# Boringit\n\nFerramenta de linha de comando, escrita em python, cuja finalidade é abstrair a rotina de uso dos comandos git.\n\n## Instalação\n\n    pip install boringit\n\n## Como utilizar\n\ni) A partir de um projeto existente e de repositórios remotos vazios:\n\n> Crie o arquivo remotes.yml:\n\n```yml\nremote_1:\n    name: "gitlab"\n    url: git@gitlab.com:marcusmello/boringit\n\nremote_2:\n    name: "github"\n    url: git@github.com:marcusmello/boringit\n```\n\n> Rode os comandos:\n\n    boringit init  \n    boringit add_remotes\n\n> (opcional) Faça o checkout para criar uma branch de trabalho\n\n    git checkout -b  <your_work-branch>\n\n> Trabalhe normalmente nos aquivos do projeto  \n> Para add, commitar e dar push para os remotos:\n\n    boringit acp\n\n## Releases\n\n[0.1.0.dev] - 2020-06-12\n\nEsta versão requer que o desenvolvedor tenha acesso ssh aos repositórios remotos, além de ter de criar manualmente o arquivo "*remotes.yml*".\n\n## Plano de refactoring\n\n* [ ] Suportar o input de usuário e senha dos servidores remotos, a fim de permitir um tracking via https;\n* [ ] Gerar automaticamente o "*remotes.yml*", caso não exista, a partir de inputs do usuário;\n* [ ] Lidar melhor com outros cenários de init, como repositório não vazios (locais ou remotos);\n* [ ] Estudar a possibilidade de adoção da biblioteca [GitPython](https://github.com/gitpython-developers/GitPython), ou mesmo abandono da boringit se eu me entender bem com a GitPython.\n',
    'author': 'marcusmello',
    'author_email': 'marcus@vintem.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcusmello/boringit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
