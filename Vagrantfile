# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.hostname = "complion"
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "192.168.50.10", netmask: "255.0.0.0"
  config.ssh.forward_agent = true
  config.vm.provider :virtualbox do |vb|
    vb.memory = 2048
    vb.cpus = 2
  end

  config.vm.provision :shell do |shell|
    # Read in ~/.gitconfig from host machine
    shell.args = "'#{File.read(Dir.home + '/.gitconfig').strip.gsub!(/\n/, '\n')}'"
    shell.inline = ''
    shell.inline += setup_variables
    shell.inline += setup_environment

    shell.inline += run_ansible_provisioning
  end
end

def setup_variables
  return <<-EOS
    export VAGRANT_USER=vagrant
    export VAGRANT_HOME=/home/$VAGRANT_USER
  EOS
end

def setup_environment
  return <<-EOS
    apt-get update

    # general stuff
    apt-get -y install git ansible

    # python stuff
    apt-get -y install python-setuptools python-pip

    # postgresql stuff
    # from: http://stackoverflow.com/questions/5420789/how-to-install-psycopg2-with-pip-on-python
    apt-get -y install libpq-dev python-dev

    if ! grep -q 'export PS1' $VAGRANT_HOME/.bashrc; then
      echo >> $VAGRANT_HOME/.bashrc
      echo 'export PS1=" \\W $ "' >> $VAGRANT_HOME/.bashrc

      echo >> $VAGRANT_HOME/.bashrc
    fi

    if ! grep -q 'cd /vagrant' $VAGRANT_HOME/.bashrc; then
      echo >> $VAGRANT_HOME/.bashrc
      echo 'alias v="cd /vagrant"' >> $VAGRANT_HOME/.bashrc

      echo >> $VAGRANT_HOME/.bashrc
    fi

    # Write ~/.gitconfig copied from host machine onto guest machine
    echo -e $1 > $VAGRANT_HOME/.gitconfig
    chown $VAGRANT_USER.$VAGRANT_USER $VAGRANT_HOME/.gitconfig
  EOS
end

def run_ansible_provisioning
  return <<-EOS
    mkdir -p /etc/ansible
    echo -e "[local]\nlocalhost  ansible_connection=local\n" > /etc/ansible/hosts
    source $VAGRANT_HOME/.bashrc
    set -e
    PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true ansible-playbook /vagrant/provisioning/site.yml -c local
  EOS
end
