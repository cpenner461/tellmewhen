'''
tellmewhen

## Overview
tellmewhen is a project built during HackTennessee 7 in Nashville, TN by the
likes of:

    - [Charlie Penner](https://github.com/cpenner461)
    - [Jared Bunting](https://github.com/jbunting)
    - [Cale Mooth](https://github.com/cale)
    - [Addison Bean](https://github.com/addisonbean)
    - [Nick Dominguez](https://github.com/nickdominguez)
    - [Jesse Gray](https://github.com/lifeingray)

It is a simple utility to watch things on the web and tell you when some
condition is met.  Common use cases are:

    - tell me when a certain response code is returned
    - tell me when a web page contains a certain string
    - tell me when a web page matches some regex pattern

Designed for an individual user, most likely in a developer/devops/admin type
of role, who wants to be notified when things happen on their web
infrastructure.

## Configuration
tellmewhen needs to be told how you'd like to be told about things.  Running
`tmw configure_tells` will let you configure supported options.

## Basic Usage
The cli is self documenting (`tmw --help`), or you can fire up the built in web
server with `tmw serve`.  Enter a url, specify the criteria, and wait to be
notified.

'''
