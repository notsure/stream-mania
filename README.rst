============
Stream Mania
============

Sandboxed Development Setup
===========================

buildout
--------

The following ports need to be installed::

    sudo port install python27 npm

Or if you are a brew user::

    brew install python npm

Bootstrap with python 2.7::

    /opt/local/bin/python2.7 bootstrap.py

Run buildout::

    bin/buildout -N


Start Dev Setup
===============

Start the application with::

  ./bin/app

The frontend is now running at http://localhost:8080


Tests
=====

Backend
-------

To run all python backend and api tests run::

  ./bin/test


Frontend
--------

To test the frontend run the karma tests via::

  ./bin/karma-test

It is also possible to have the test runner watching the changes in
the spec files, this is useful if you dont want to run the tests
while writing tests but directly see if there are errors::

   open app/Gruntfile.js

edit the section 'Test settings' as follows::

    // Test settings
    karma: {
      unit: {
        configFile: 'karma.conf.js',
        singleRun: false,
        autoWatch: true
      }
    }

