import os
from shutil import rmtree
from subprocess import check_call

from charms.reactive import when, when_not, set_state, hook
from charmhelpers.core import hookenv


SRC_DIR = os.path.join(hookenv.charm_dir(), 'mailinabox')


@hook('install')
def install():
    config = hookenv.config()

    if os.path.exists(SRC_DIR):
        # Recover from a botched prior attempt
        rmtree(SRC_DIR)

    # TODO: configurable git repo?
    check_call(['git', 'clone', 'https://github.com/mail-in-a-box/mailinabox'], cwd=hookenv.charm_dir())
    # TODO: configurable verification key?
    # TODO: improve obtaining & importing key?
    os.system('curl -s https://keybase.io/joshdata/key.asc | gpg --import')
    # TODO: configurable git branch?
    check_call(['git', 'verify-tag', 'v0.18c'], cwd=SRC_DIR)
    check_call(['git', 'checkout', 'v0.18c'], cwd=SRC_DIR)
    set_state('mailinator.installed')


@when('mailinator.installed')
@when_not('mailinator.configured')
def config_changed():
    config = hookenv.config()
    if not config.get('hostname'):
        hookenv.status_set('blocked', 'waiting for "hostname" configuration to be set')
        return
    set_state('mailinator.configured')


@when('mailinator.configured')
@when_not('mailinabox.setup')
def setup():
    hookenv.status_set('maintenance', 'setting up mailinabox')
    password = "1234"  # TODO: generate a decent password
    config = hookenv.config()
    setup_env = {}
    setup_env.update(os.environ)
    setup_env.update({
        'NONINTERACTIVE': '1',
        'DISABLE_FIREWALL': '1',  # Juju manages this
        'SKIP_NETWORK_CHECKS': '1',
        'PUBLIC_IP': hookenv.unit_public_ip(),
        'PUBLIC_IPV6': 'auto',
        'PRIMARY_HOSTNAME': config['hostname'],
        'EMAIL_ADDR': 'me@%s' % (config['hostname']),
        'EMAIL_PW': password,
    })
    hookenv.open_port(53, protocol='UDP')
    for port in (25, 80, 443, 587, 993, 4190):
        hookenv.open_port(port)
    check_call(['setup/start.sh'], shell=True, cwd=SRC_DIR, env=setup_env)
    set_state('mailinabox.setup')
    hookenv.status_set('active', 'Admin console: https://%s/admin' % (hookenv.unit_public_ip()))
    # TODO: change status once DNS lookup for configured hostname matches public ip
