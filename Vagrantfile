# encoding: utf-8
# This file originally created at http://rove.io/da3543a91d67b31f9b6ad3044f7019e1

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "opscode-ubuntu-12.04_chef-11.4.0"
  config.vm.box_url = "https://opscode-vm-bento.s3.amazonaws.com/vagrant/opscode_ubuntu-12.04_chef-11.4.0.box"
  config.ssh.forward_agent = true

  config.vm.network :forwarded_port, guest: 80, host: 8080
  config.vm.provision :shell, :path => "bootstrap.sh"
end
