# type: ignore

from invoke import task
from github3 import GitHub
from textwrap import dedent
from os import environ as env

README = dedent(
    """
    <div align="center">

    # stars

    ![License][license]
    [![Gitmoji][gitmoji-badge]][gitmoji]
    [![Code style: black][black-badge]][black]

    ## My GitHub ⭐s, curated.

    </div>

    <div align="justify">

    {contents}

    </div>

    <div align="center">

    Credits to [**@maguowei**][maguowei] for coming up the idea [**here**][starred].
    My code is a modified version of their code, simplified to just work as I want.
    Copyright (c) 2021, Ujjwal Panda

    </div>

    [gitmoji]: https://gitmoji.dev
    [black]: https://github.com/psf/black
    [maguowei]: https://github.com/maguowei
    [starred]: https://github.com/maguowei/starred
    [license]: https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge
    [black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
    [gitmoji-badge]: https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=for-the-badge
    """
)


@task
def stars(c):

    """
    Curating my GitHub stars.

    This sorts through all of my GitHub stars and sorts them into
    separate categories by the primary programming language used
    in each project. This allows me to go through them all easily
    and find exactly what I am looking for when the time comes to
    use them.
    """

    user = env["GITHUB_USER"]
    token = env["GITHUB_TOKEN"]

    api = GitHub(token=token)

    stars = api.starred_by(user)

    starred = {}
    for star in stars:
        url = star.html_url
        name = star.full_name
        language = star.language or "Others"
        if star.description:
            description = star.description.replace("\n", "").strip()
        else:
            description = "*No description*"
        if language not in starred:
            starred[language] = []
        starred[language].append((name, url, description))
    starred = dict(sorted(starred.items()))

    toc = "\n".join(
        [
            f"* [**{language}**](#{'-'.join(language.lower().split())})"
            for language in starred.keys()
        ]
    )

    cards = []
    for language, repositories in starred.items():
        repolist = "\n".join(
            [
                f"* [**{name}**]({url}): {description}"
                for (
                    name,
                    url,
                    description,
                ) in repositories
            ]
        )
        cards.append(f"## {language}\n\n{repolist}")
    contents = "\n\n".join([toc, *cards])

    with open("README.md", "w+") as f:
        f.write(README.format(contents=contents))
