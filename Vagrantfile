# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.provision :shell,
    inline: "sudo -u vagrant /vagrant/setup.sh"
  config.vm.network "forwarded_port", guest: 8080, host: 8080
end
