# Boringit

Ferramenta de linha de comando, escrita em python, cuja finalidade é abstrair a rotina de uso dos comandos git.

## Instalação

    pip install boringit

## Como utilizar

i) A partir de um projeto existente e de repositórios remotos vazios:

> Crie o arquivo remotes.yml:

```yml
remote_1:
    name: "gitlab"
    url: git@gitlab.com:marcusmello/boringit

remote_2:
    name: "github"
    url: git@github.com:marcusmello/boringit
```

> Rode os comandos:

    boringit init  
    boringit add_remotes

> (opcional) Faça o checkout para criar uma branch de trabalho

    git checkout -b  <your_work-branch>

> Trabalhe normalmente nos aquivos do projeto  
> Para add, commitar e dar push para os remotos:

    boringit acp

## Releases

[0.1.0.dev] - 2020-06-12

Esta versão requer que o desenvolvedor tenha acesso ssh aos repositórios remotos, além de ter de criar manualmente o arquivo "*remotes.yml*".

## Plano de refactoring

* [ ] Suportar o input de usuário e senha dos servidores remotos, a fim de permitir um tracking via https;
* [ ] Gerar automaticamente o "*remotes.yml*", caso não exista, a partir de inputs do usuário;
* [ ] Lidar melhor com outros cenários de init, como repositório não vazios (locais ou remotos);
* [ ] Estudar a possibilidade de adoção da biblioteca [GitPython](https://github.com/gitpython-developers/GitPython), ou mesmo abandono da boringit se eu me entender bem com a GitPython.
