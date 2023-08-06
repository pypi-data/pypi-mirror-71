Signet - Protect your users and customers from hackers
======================================================

FULL HTML Documentation: <http://jamercee.github.io/signet/>

Signet provides support for building and delivering tamper resistant
python to your users and customers.

Signet creates a custom python loader which you deliver with your
script. On each invocation, the loader will verify no tampering has
ocurred before it runs the python script.

Users have the confidence of knowing their scripts are safe and yet
retain full access to the python source for code review and enhancement.
And you know your users are running the right version of code.

Signet is fully integrated with
[distutils](https://docs.python.org/2.7/library/distutils.html) to make
the process of building and installing new python projects as simple and
painless as possible.

How does it work?
-----------------

Signet relies on the strength of cryptographic hash to reliably detect
file modifications. Signet builds hashes of your script and all it's
dependencies. These hashes are incorporated into a custom python loader
which will handle re-verifying the hashes before it will run your
script.

If your script or any of it's dependencies are tampered with, the loader
will emit an error and exit. If everything matches, the loader will run
your script.

Example usage
-------------

For example, if you had a simple script `hello.py`:

    import os
    print('hello from %s' % os.name)

And you deployed it with this simple `setup.py`:

    from distutils.core import setup, Extension
    from signet.command.build_signet import build_signet

    setup(name = 'hello',
        cmdclass = {'build_signet': build_signet, },
        ext_modules = [Extension('hello', sources=['hello.py'])],
        )

Build your loader:

    python setup.py build_signet

On Windows you'll have `hello.exe` and on Linux you'll have `hello`.

The signet system also provides facilities for code signing:

    from distutils.core import setup, Extension
    from signet.command.build_signet import build_signet, sign_code

    setup(name = 'hello',
        cmdclass = {'build_signet': build_signet,
                    'sign_code': sign_code,
                   },
        ext_modules = [Extension('hello', sources=['hello.py'])],
        )

Build your loader:

    python setup.py build_signet
    python setup.py sign_code --savedpassword --pfx-file {path-to-pfx}

Installing Signet
-----------------

Signet is hosted on github at <https://github.com/jamercee/signet>

Installation using git:

    git clone https://github.com/jamercee/signet
    cd signet
    python setup.py install

Signet can also be installed with pip:

    pip install signet

Features
--------

-   Multiplatform: works under
    -   Windows (32/64-bit)
    -   Linux
    -   FreeBSD
-   Integrated with Distutils
-   Protection from tampering (SHA1 hashed content)
-   On Windows
    -   Provides code signing executables
    -   PE executable verification
    -   Automatic resource file generation
    -   Customizable program icon
-   Customizable python loader (full c++ included)
-   Unique process name
    -   show `hello` rather than `python hello.py`
-   Compatible with virtualenv

Project Background
------------------

### What is a *signet*?

Signet took it's name from the ancient practice of sealing documents by
pressing personal jewelery into hot wax. This uniquely identified the
documents origin. The jeweley usually took the form a rign worn by the
sender --a **signet ring**.

### Project Motivation

[Carroll-Net](http://carroll.net) provides a commercial multiplatform
backup application written in python. By delivering the source code to
our clients, they can audit the entire code base to ensure it meets
their needs, and even make changes to suit their individual tastes and
enterprise requirements.

But distributing commercial applications in python introduces new
security challenges. Hackers who become aware of our large installation
base could seek to inject changes into our application to assist in
their criminal activity. To make matters worse, backup software requires
full admin privileges to be able to to do its job. Hackers who
successfully inject new code into this environment would have unfettered
control over their victim.

The security challenge is therefore to protect our clients from hackers
while still providing full python source code. The solution we developed
is to deploy our application with a custom python loader.

### What is a python loader?

Python is an interpreted language. To run your python applications
involves reading your source code, compiling it to python op-codes, then
passing this compiled code to the python interpreter for execution.

Running your python application is therefore handled by the python
program (ie: on windows, python.exe and on linux /use/bin/python). The
python program is your loader -- the program that loads and executes
your application.

But the python program is only one example of how you can load and
execute your python application. The python website provides
comprehensive documentation on how you can create your own loader and
replace the default one provided with your system. [Read
more](https://docs.python.org/2/extending/embedding.html)

### Solve the python security challenge

A custom loader can take steps to validate your application before
running it. Correctly implemented, it would detect tampering and then
take appropriate measures to counter the tampering. In an ideal world,
it could undo the tampering by reverting your application back to its
original version. But at a minimum, it will emit an error and refuse to
run. The beauty of the custom loader approach is there is no limit to
the security you choose to implement --you have complete control.

### The Signet Loader

[Carroll-Net](http://carroll.net) has created a custom python loader
called signet \<signet.command.build\_signet\>. It is fully integrated
into distutils to make the process of building your own custom loader as
simple and painless as possible. Also, by using distutils, it guarantees
your clients will have a quick no-nonsense installation experience when
they choose your software.

The signet approach is simple. Your python app is scanned and a sha1
hash of it's content is calculated. Signet then recursively scans it's
dependencies and calculates sha1 hashes for each of them. These hashes
are then incorporated into a loader which is compiled to an executable
program which will act as your application's loader.

You deliver these two files to your client; your newly built loader and
your application with instructions they should run the loader. When
invoked, it will recalculate the sha1 hashes for your app and it's
dependencies to confirm they match the pre-calculated values. If they
match, execution is transferred to your application. If tampering is
detected, it emits an error message and terminates without ever running
any of the tampered coded.

For example, say you had application called *hello.py*. On windows,
Signet would create a loader for this app called *hello.exe* (on linux
it would create *hello*). This is the program your clients would run.
But the logic for your application would still be within hello.py, which
means your client retains full access to your source.

### Code signing

[Carroll-Net](http://carroll.net) delivers our backup application as a
multiplatform system (windows, unix, linux, freebsd, etc). If it's a
platform that can run python, we fully support it for backup. But we
also want to take advantage of any extra security available to us on
each platform. This is the case with code signing available on Windows.

Windows has had code signing available for many years. With code
signing, a software developer can add a signature to his software that
cannot be faked. Even better, the signature can be used to detect if the
code has been tampered with. [Read
more](https://en.wikipedia.org/wiki/Code_signing)

You may wonder -- why would you need code signing in addition to
signet's custom loader technology? The answer is simple -- while signet
can detect if your script or it's dependencies have been tampered with,
signet cannot detect if the signet loader itself has been tampered with
(eg: if the *hello.exe* file was changed).

The signet system provides code signing \<signet.command.sign\_code\>
for projects you deploy to windows.

### Code signing with Signet

To use code signing \<signet.command.sign\_code\> with your windows
projects will require you purchase a code signing certificate. These
certificates can be purchased from a number of commercial entities.
You'll find a list of some of these vendors at the end of this page.

Once you've purchased your certificate, you'll need to convert this file
to a Personal Information Exchange File (also referred to as a [PKCS\#12
file](https://en.wikipedia.org/wiki/PKCS12) ), with a file extension of
\*.pfx. The vendor who provides your cert will have directions on how to
convert their cert to this format.

Signet will need to know the full path to where you store your \*.pfx
file. It will also need to know the password you choose to unlock and
use your pfx file. Signet will offer you the option to save your
password (encrypted of course) to make repeated
*edit-compile-build-debug* cylces faster.

Code signing usage introduces an interrelated topic, Windows Resource
Files. While not strictly required, they are strongly recommended when
offering secure computing solutions to your clients.

Windows resource files allow you to embed your company details in your
executable. Your customers can inspect your programs and have the
confidence of knowing they came from you. Signet provides all the tools
you need to automatically generate Resource Files and to embed them in
your custom loader.

### Extra Perks

One downside of deploying python based solutions is the ambiguous
process list presented to your customers. When your applications are
running, your customers only see another instance of python running. To
determine the actual program name, a client needs to expand the process
list to display the command line.

A custom loader does not suffer form this. The loader is the process
name displayed in the process list. In the example we used in this
document, your customer would see *hello.exe*. This makes for simpler
system administration for your clients.

Additionally, signet code signing \<signet.command.sign\_code\> enables
you to associate a custom icon with your application. Administrative
tools such as process explorer and task manager will render these icons
adjacent to your running instances, further enhancing your clients admin
experience.

### Commercial certificates vendors

There many companies offering to sell code signing certificates. We're
only listing three here These three companies offer free timestamp
servers for public use and code signing \<signet.command.sign\_code\>
uses them, so it seemed only fair to highlight their offerings. But any
valid code certificate should work.

-   Comodo - <https://www.instantssl.com/code-signing/index.html>
-   Global Sign - <https://www.globalsign.com/>
-   Symatec - <http://www.symantec.com/code-signing>

### License

Signet is licensed under the 3-clause BSD License:

    Copyright (c) 2014, Carroll-Net, Inc. (http://carroll.net)
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * Neither the name of the Carroll-Net, Inc. nor the
          names of its contributors may be used to endorse or promote products
          derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL CARROLL-NET, INC. BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Contents
--------

Indices and tables
------------------

-   genindex
-   search

