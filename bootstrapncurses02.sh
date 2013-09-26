# shebang not working, try using bash directly

if [ ! -d "$HOME/.rbenv/" ]; then

    #update OS
    sudo apt-get update
    sudo apt-get -y upgrade
    
    # ensure correct kernel headers are installed
    sudo apt-get -y install linux-headers-$(uname -r)
    
    # for debugging use
    sudo apt-get install -y vim
    
    # install pre-requisite for ncurses
    sudo apt-get install libncurses-dev
    
    # install git
    sudo apt-get install -y git-core
    
    # build essential
    sudo apt-get install -y build-essential git
    
    # other libraries needed for bvenv
    sudo apt-get install -y libxml2-dev libxslt-dev libssl-dev
    
    # install rbenv and setup ruby 1.9.3 from scratch
    git clone git://github.com/sstephenson/rbenv.git $HOME/.rbenv
    echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> $HOME/.bashrc
    echo 'eval "$(rbenv init -)"' >> $HOME/.bashrc
    exec $SHELL -l

else
    # Install ruby-build, provides 'install' function to rbenv
    git clone git://github.com/sstephenson/ruby-build.git $HOME/.rbenv/plugins/ruby-build

    # now a direct intallation of ruby via rbenv
    rbenv install 1.9.3-p448
    rbenv rehash
    rbenv global 1.9.3-p448
    
    # get modified gem for ncurses and install from local
#    wget http://github.com/downloads/rkumar/rbcurse/ncurses-0.9.2.gem
#    gem install --local ncurses-0.9.2.gem
 
    gem install rbcurse-core

    cd /lib/x86_64-linux-gnu
    sudo rm libncursesw.so
    sudo ln -s /lib/x86_64-linux-gnu/libncursesw.so.5 libncursesw.so

    cd
    git clone https://github.com/rkumar/rbcurse-core.git
    cd rbcurse-core/examples
    ruby alpmenu.rb
   
    # install demo repo
    git clone https://github.com/whoward/ruby-curses.git
    cd ruby-curses
    ruby 01-hello_world.rb

fi
