# Homework 2: When a Wreck Reaches the World Wide Web

## Introduction

Unfortunately it seems your company never learns. Yet again the company
has decided to cut costs and hire Shoddycorp's Cut-Rate Contracting to 
write another program. But after all, your company insists, their *real*
strength is web sites, and this time they were hired to create a high 
quality web site. As usual they did not live up to that promise, and
are not answering calls or emails yet again. Just like last time, the
task of cleaning up their mess falls to you.

The project Shoddycorp's Cut-Rate Contracting was hired to create a 
web site that facilitated the sale, gifting, and use of gift cards.
They seemed to have delivered on *most* of the bare funcitonality of
the project, but the code is not in good shape. Luckily Kevin Gallagher
(KG) has read through the code already and left some comments around
some of the lines that concern him most. Comments not prefaced by KG were
likely left by the original author. Like with all of Shoddycorp's
Cut-Rate Contracting deliverables, this is not code you would like to
mimic in any way.

## Part 0: Setting up Your Environment

In order to complete this assignment you will need the git VCS, Travis or GitHub Actions, 
python 3 and the Django web framework. You can install Django using the 
following command:

```
sudo pip3 install django
```
NOTE: It is better practice to do this within a virtual environment and 
not use sudo, however, learning virtual environments adds an additional
learning curve that is not part of the class. If you already know how to
do this, we recommend the virtual environment approach.

Some additional tools that may be useful for this assignment (but are
not necessary) are sqlite, burp suite, the python requests library,
and the web development console of your favorite browser. If you are
runing a \*NIX system, these tools should be pre-installed and/or
available in your distribution's package manager. Like in the last
assignment we will not be checking for git best practices like writing good
commit messages. However, we will be checking for signed commits, since
they are security relevant. Additionally, it is in your best interest to
continue to follow git best practices.

When you are ready to begin the project, please create a repository 
on GitHub for your second assignment. Like before, be sure to make 
the repository **private**. Create a travis.yml file, which you will 
use to test your program later.


## Part 1: Auditing and Test Cases

Start off by copying the files from this repository into your own, and
add them to git. The files and directories you need are:

```
GiftcardSite LegacySite images templates manage.py
```

After you compy these directories and files over, be sure to generate 
the database that django relies on. This can be done by running the commands:

```
python manage.py makemigrations LegacySite
python manage.py makemigrations
python manage.py migrate
sh import_dbs.sh
```

Read through the `models.py` and `views.py` files (and the helper
functions in `extras.py`) in the LegacySite folder to get a feel 
for what the web site is doing and how. You can also try running
the test server and interacting with the site by running the
following command and browsing to 127.0.0.1:8000.
```
python manage.py runserver
```

For this part, your job will be to find some flaws in the program, and
then create test cases that expose flaws in the program. You should
write:

1. *One* attack, that exploits a XSS (cross-site scripting) 
   vulnerability.
2. *One* attack that allows you to force another user to gift
   a gift card to your account without their knowledge.
3. *One* attack that allows you to obtain the salted password for a user
   given their username. The database should contain a user named 
   ``admin.''
4. *One* attack that exploits another attack not listed above on the server.
   Some hints for this section are: looking at the way the passwords are
   stored, or looking at how interactions are done with the giftcardreader
   binary.
5. A text file, `bugs.txt` explaining the bug triggered by each of your
   attacks, and describing any other vulnerabilities or broken 
   functionalities you came across. There are more than the bugs mentioned
   above.

These attacks can take the form of a supplied URL, a POST made to the 
web page, a gift card file, a web page, a javascript function, or some
other method of attack. To create your attacks, you may want to look at 
the HTML source code of the templates and the code of each view, and 
find a way they can be exploited. Tools like burp suite can help in
finding ways to attack the site, but are not required. Please submit 
these attacks in a folder called "part 1" in your git repository.

Finally, fix the vulnerabilites that are exploited by your attacks, 
and verify that the attacks no long succeed on your site. You are 
allowed to use django plugins and other libraries to fix these 
vulnerabilities. To make sure that these bugs don't come up again as
the code evolves, write some test cases for django that test for 
these vulnerabilites. Then have Travis run these tests with each push.

When you are finished with this section, please mark your part 1 
submission by tagging the desired commit with the tag "part_1_complete"

## Part 2: Encrypting the Database 

Currently the website uses a database that contains valuable gift card
data. If an attacker gets access to this gift card data, they can use 
the cards they got to obtain free merchandise, or even pay of their
tuition with the NYU tuition gift cards! For this reason your company 
needs to make sure that even if the database somehow leaks, the attacker
will have a hard time using the cards.

Your company asked Shoddycorp's Cut-Rate Contracting to encrypt the 
database, but it seems they did not know how to do that, or did not want
to. The code you received does not encrypt the database at all, but your
company wants to ensure the data's protection at rest.

Your second job, therefore, is to modify this code to encrypt the data in
the database. You are allowed to use django plugins or external libraries
to implement this. Please see the lecture content for tips on proper key
management and the different methods of doing database encryption.

When you are finished with this part of the assignment, please briefly
explain how you implemented the database encryption, how you managed keys,
and why you choose to manage keys that way. This should be stored in a
file called "encryption_explanation.txt" in a folder called "part 2" in
the git repository. 

When you finish this part of the assignment, please mark your part 2 
submission by tagging the desired commit with the tag "part_2_complete"

## Grading

Total points: 100

Part 1 is worth 65 points:

* 25 points for your attack cases
* 15 points for all fixes
* 10 points for the bug writeup
* 10 points for Travis or GitHub Actions regression testing
* 05 points for signed git commits.

Part 2 is worth 35 points:

* 10 points for encrypted database models
* 10 points for proper key management
* 15 points for your writeup.

## What to Submit

On NYU Classes, submit a link to your GitHub repository. The repository
should be **private**, and you should add the instructor/TA's GitHub
account as a contributor to give them access for grading.

For this section, your instructors are: Kevin Gallagher, GitHub ID `kcg295` and
Dean Christakos, GitHub ID `Deanchristakos`.

For this section, your TAs are Gaurav Chauhan, GitHub ID to be added, Sarthak
Bohra, GitHub ID to be added, and more TAs to be added.

The repository should contain:

* Part 1
  * Your .travis.yml
  * At least one signed commit
  * A directory named `part1` that contains your attack cases.
  * An updated .travis.yml that runs your tests.
  * A commit with the fixed version of the code (if you like, this
    commit can also contain the files mentioned above) tagged as
    part_1_complete.
* Part 2
  * A directory named `part2` which contains your 
    `encryption_explanation.txt' file.
  * A commit with the version of the code that supports DB encryption
    (if you like, this commit can also contain the files mentioned above)
    tagged as part_2_complete.

## Concluding Remarks

Despite the fixes you've made, there are almost certainly still many
bugs lurking in the program. Although it is possible to get to a secure
program by repeatedly finding and fixing bugs, it's a lot of work.

Though this program may be salvagable in its current state, it would be 
better in this case to rewrite it from scratch, using proper style, 
using Django addons for security purposes, and sticking to using ORMs 
and avoiding reflected unfiltered user input to the users. The code as
it exists now is difficult to read, and therefore difficult to fix. It
also unecessarily uses home-brewed solutions for things that can be solved
easily with common libraries or Django built-ins. This is certainly not
code that you should seek to reproduce, or use as an example of good code.

A cleanly written version of this will be released after the assignment is
over. When this is released, compare it to the code you have and see what
the differences are, and how much simpler things could be if standard
solutions were used. We suspect that the cleanly written version will be
relatively bug-free, but you are encouraged to try to attack it and
prove us wrong!
