import CI.action
import CI.builder.system

CI.builder.system.features(packages=['git'])

description = 'configure Git settings and local repositories'

import os

class G:
    base_directory = None
    repository_urls = []
    gitconfig = None
    link_gitconfig = False

def features(
        base_directory='~/git',
        repository_urls=[],
        gitconfig=None,
        link_gitconfig=False
    ):
    G.base_directory = os.path.expanduser(os.path.expandvars(base_directory))
    G.repository_urls.extend(repository_urls)
    if gitconfig:
        G.gitconfig = os.path.expandvars(os.path.expanduser(gitconfig))
    G.link_gitconfig = link_gitconfig

class GitCloneAction(object):

    # Git clone fails if directory exists.
    destructive = True

    def __init__(self, repo_url):
        self.description = 'clone Git repository: %s' % repo_url
        self.repo_url = repo_url

    def check(self, runner):
        dir_name = os.path.splitext(os.path.basename(self.repo_url.split(':')[-1]))[0]
        return not os.path.exists(os.path.join(G.base_directory, dir_name))

    def perform(self, runner):
        if not os.path.exists(G.base_directory):
            os.makedirs(G.base_directory)
        with runner.chdir(G.base_directory):
            runner.run('git', 'clone', self.repo_url)

def actions(runner):
    if G.gitconfig:
        if G.link_gitconfig:
            yield CI.action.CreateLink(G.gitconfig, '~/.gitconfig')
        else:
            yield CI.action.CopyFile(G.gitconfig, '~/.gitconfig')
    for repository_url in G.repository_urls:
        yield GitCloneAction(repository_url)