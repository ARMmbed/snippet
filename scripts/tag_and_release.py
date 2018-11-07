# --------------------------------------------------------------------------
#  Snippet
# (C) COPYRIGHT 2018 Arm Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------
"""Part of the CI process"""

import os
import subprocess


def git_url_ssh_to_https(url):
    """Convert a git url

    url will look like
    https://github.com/ARMmbed/snippet.git
    or
    git@github.com:ARMmbed/snippet.git
    we want:
    https://${GITHUB_TOKEN}@github.com/ARMmbed/snippet.git
    """
    path = url.split('github.com', 1)[1][1:].strip()
    new = 'https://{GITHUB_TOKEN}@github.com/%s' % path
    print('rewriting git url to: %s' % new)
    return new.format(GITHUB_TOKEN=os.getenv('GITHUB_TOKEN'))

VERSION_FILE='src/snippet/_version.py'

def main():
    """Tags the current repository

    and commits changes to news files
    """
    # see:
    # https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi
    twine_repo = os.getenv('TWINE_REPOSITORY_URL') or os.getenv('TWINE_REPOSITORY')
    print('tagging and releasing to %s as %s' % (
        twine_repo,
        os.getenv('TWINE_USERNAME')
    ))

    if not twine_repo:
        raise Exception('cannot release to implicit pypi repository. explicitly set the repo/url.')

    version = subprocess.check_output([ 'python', 'setup.py', '--version']).decode().strip()
    if 'dev' in version:
        raise Exception('cannot release unversioned project: %s' % version)

    print('Preparing environment')
    subprocess.check_call(['git', 'config', '--global', 'user.name', 'monty-bot'])
    subprocess.check_call(['git', 'config', '--global', 'user.email', 'monty-bot@arm.com'])
    url = subprocess.check_output(['git', 'remote', 'get-url', 'origin'])
    branch_name = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    new_url = git_url_ssh_to_https(url.decode())
    subprocess.check_call(['git', 'remote', 'set-url', 'origin', new_url])
    branch_spec = 'origin/%s' % branch_name.decode('utf-8').strip()
    subprocess.check_call(['git', 'branch', '--set-upstream-to', branch_spec])
    print('Generating a release package')
    subprocess.check_call(
        [ 'python', 'setup.py', 'clean', '--all', 'bdist_wheel', '--dist-dir', 'release-dist'])
    print('Uploading to PyPI')
    subprocess.check_call(['python', '-m', 'twine', 'upload', 'release-dist/*'])
    print('Committing the changelog & version')
    subprocess.check_call(['git', 'add', VERSION_FILE])
    subprocess.check_call(['git', 'add', 'CHANGELOG.md'])
    subprocess.check_call(['git', 'add', 'docs/news/*'])
    message = ':checkered_flag: :newspaper: Releasing version %s\n[skip ci]' % version
    subprocess.check_call(['git', 'commit', '-m', message])
    print('Tagging the project')
    subprocess.check_call(['git', 'tag', '-a', version, '-m', 'Release %s' % version])
    print('Pushing changes back to GitHub')
    subprocess.check_call(['git', 'push', '--follow-tags'])
    print('Marking this commit as latest')
    subprocess.check_call(['git', 'tag', '-f', 'latest'])
    subprocess.check_call(['git', 'push', '-f', '--tags'])
    print('Done.')

if __name__ == '__main__':
    main()
