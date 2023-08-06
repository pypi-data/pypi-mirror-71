codetree
========

Codetree is a tool for assembling directories of code from disparate sources. You might, for example, want to keep your application code separate from your deployment code and local configuration, then bring them all together as part of your build process. Codetree helps you do that.

Usage
-----

Codetree assumes that you'd like to assemble your code in the current working directory. It expects a configuration file whose syntax is detailed below.

Configuration Files
-------------------

[Config-manager](https://launchpad.net/config-manager) configuration files should be compatible with codetree. Codetree has a few more features, and therefore some additional config syntax.

Configuration files consist of directives, one per line, consisting of a local destination and a source. Blank lines and lines whose first character is "#" are ignored.

Here's an example config:

    app                     lp:myapp;lightweight=true
    app/plugins/woohoo      lp:myapp-woohoo;revno=44
    app/images/logo.gif     http://content.internal/myimage.gif;overwrite=true
    app/downloads           @
    app/content             /home/contentbot/appcontent;method=link
    app/mytag               git://github.com/myapp;revno=mytag
    app2                    git+ssh://git@github.com/me/app2.git
    app3                    git+https://github.com/me/my3rdapp.git
    mycharm                 cs:trusty/mycharm
    othercharm              cs:trusty/othercharm;channel=edge,overwrite=true

Taking that line-by-line:

* the app directory contains a copy of the latest version of myapp, a bzr repo hosted on launchpad.net. Since "lightweight" is specified a lightweight checkout will be used rather than the default branching behavior.
* the app/plugins/woohoo directory contains revision number 44 of lp:myapp-woohoo
* app/image/logo.gif is a single image file. If it exists it will be overwritten.
* app/downloads is an empty directory
* app/content is a symlink of the local directory /home/contentbot/appcontent.
* app/mytag is a git checkout of the git repository from github at the tag 'mytag'
* app2 is also a git checkout but using a different format for the git url
* app3 is another git checkout but using the https style git url understood by codetree
* mycharm is a Juju charm from the [charm store](https://jujucharms.com/)

### Source URLs

There are currently five handlers, each registered for a number of URL schemes:

* Bzr: bzr, bzr+ssh, lp, bzr+http, bzr+https
* HTTP/S: http, https
* Local: (empty scheme)
* Git: git, git+ssh, git+http, git+https
* Charm Store: cs

If you're familiar with Bzr, you'll note that bzr+http and bzr+https are not valid schemes for Bzr URLs. No two handlers may handle the same scheme. In order to definitively identify the handler you want for a source, the scheme you use may be slightly non-standard.

Similarly git+http and git+https are not valid schemas for git URLs, but are used in codetree for exactly the same reason.

Other handlers are planned, such as an archive handler (variant of the http/s handler).

### Source options

Sources may accept various arguments. As in the lp:myapp-woohoo example above, you see that they come at the end of the source, separated by a semicolon. Arguments take the form key=value. More than one option is comma separated.

Supported options are:
revno: Checkout a specific revision. For Git branches this is any git branch, tag or ref understood by git checkout, defaulting to master. The charm store does not support revno as the revision is specified as part of the url.
overwrite: If the destination directory already exists, just overwrite it. Otherwise it is an error.

**Git Only**
depth:  Use "git clone --depth n" to create a shallow clone only up to n revisions.
branch: Use "git clone -b <branch> --single-branch" to clone a single branch rather than clone all then checkout.

**BZR Only**
lightweight: Use "bzr checkout --lightweight" rather than "bzr branch".  Only supported for Bazaar branches.

**Local Only**
method: copy, rsync, link or hardlink - rsync is default

Copy does not remove files, rsync will. The method link uses a symbolic link, hardlink obviously a
hardlink.

**Charm Store Only**
base_url: By default it is assumed to be the public store 'https://api.jujucharms.com/charmstore/v5' so few will need to modify this. Note only https is always supported.

channel: By default it is assumed to be the stable channel, you can specify 'unpublished', 'edge', 'beta', 'candidate', or 'stable'. Note that because there is no charmstore auth at the moment they must be granted read access to everyone.

