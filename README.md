# Complion Coding Challenge

The purpose of this challenge is to take a small amount of direction, hack together some code so I can see your coding style. Here is the problem that I would like to see solved:

I would like to see a small portion of the flexible meta data structure white boarding implemented. Specifically only spend a couple of hours or as much time as you feel comfortable where you want to present your work.

## RUNNING THE APP
---

To get up and running:

#### Install Vagrant from http://www.vagrantup.com/downloads.html

    # if using brew cask on mac os x
    brew cask install vagrant

#### Install VirtualBox from https://www.virtualbox.org/wiki/Downloads

    # if using brew cask on mac os x
    brew cask install virtualbox

#### Clone this project

#### Checkout the submodules

    git submodule init
    git submodule update

#### Start virtual server using Vagrant

    cd ~/path/to/cloned/project
    vagrant up

#### Log in to the virtual server

    vagrant ssh

#### Run setup

    # execute the POSTGRESQL commands as root
    # - see NOTES.md (section: POSTGRESQL SQL QUERIES)
    # run db migration commands
    python complion/manage.py db init
    python complion/manage.py db migrate
    python complion/manage.py db upgrade
    python complion/manage.py fixtures init

#### Run development server

    python complion/api.py

#### Navigate to the web app:

  [http://192.168.50.10](http://192.168.50.10)

## REQUIREMENTS
---

### Problem:

The end result should be a UI that would allow a user to search a document management repository.

The document types to use should be Protocol, Consent and Contract

    Protocol Document Type has a metadata property field called IRB number
    Consent Document Type has a metadata property field called IRB number
    Contract Document Type has a metadata property field called contract number

    The user should be able to search by one or more metadata properties across all document types
        User want to search the repository by IRB number regardless of document type.
    The user should be able to search by one or more document types and the related metadata properties.
        User wants to search by a protocol and a consent where the IRB is i.e. 12345678


### Technology:
You can you any language or framework you would like. I do not want tools and frameworks to be a limiting factor. I am more interested in the code.
For a database, you can use anything you would like (MySQL or Postgres etc). From a speed point of view, if you want to use Mongo for the configuration tables, that is cool as well.

### Other Notes:
If you remember, the key to this architecture is to create a metadata table for each metadata property to store the metadata value. [I have created a Powerpoint that contains the suggested table architecture that we discussed the other day.](docs/suggested-db-schema.pdf) However please do not hesitate to call or ask questions.

The most important item I am looking for is how you write the database access layer models and the app controllers to present the UI. If you want, you can use a JS framework but straight HTML is cool for now. Again looking for a balance of speed and quality.

You do not need to create a configuration UI to build a document. You can manually create the tables including the 1-2 metadata tables. You can prepopulate the tables in the database as I do not expect a UI to import a document.
