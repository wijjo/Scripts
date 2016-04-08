import castiron.main
import castiron.action.filesystem

import os

class G:
    private_key_file = os.path.expanduser('~/.ssh/id_rsa')
    public_key_file = os.path.expanduser('~/.ssh/id_rsa.pub')
    authorized_keys_file = os.path.expanduser('~/.ssh/authorized_keys')

class SSHGenerateKeyAction(object):

    description = 'generate SSH private/public keys'
    destructive = True

    def check(self, runner):
        return not os.path.isfile(G.private_key_file)

    def execute(self, runner):
        runner.run_command('ssh-keygen -t rsa -q -f %s' % G.private_key_file)
        public_key = runner.read_file(G.public_key_file)
        runner.info('===== Paste the following to https://github.com/settings/ssh =====\n%s\n=====' % public_key)
        runner.read_text('Press Enter to continue')

class SSHAuthorizeKeyAction(object):

    description = 'authorize the initial SSH public key'
    # Don't overwrite an existing authorized_keys file.
    destructive  = True

    def check(self, runner):
        return not os.path.isfile(G.authorized_keys_file)

    def execute(self, runner):
        public_key = runner.read_text('RSA public key')
        runner.write_file(G.authorized_keys_file, '%s\n' % public_key, permissions=0600)

@castiron.main.builder('ssh', 'initialize SSH user configuration')
def _builder(runner):
    yield castiron.action.filesystem.CreateDirectory('~/.ssh', permissions=0700)
    yield SSHGenerateKeyAction()
    yield SSHAuthorizeKeyAction()
