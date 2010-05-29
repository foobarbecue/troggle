Troggle is an application for caving expedition data management, originally created for use on Cambridge University Caving Club expeditions and licensed under the GNU Lesser General Public License.

Troggle setup
==========

Python, Django, and Database setup
-----------------------------------
Troggle requires Django 1.1 or greater, and any version of Python that works with it. As of writing this readme, there was no actual Django 1.1 release, so Troggle required the SVN version of Django. Check Django out to somewhere on your PYTHONPATH with the following command:

svn co http://code.djangoproject.com/svn/django/trunk/

If you have an older installation of Django installed on your system, the easiest way to make sure troggle is using the newest version of Django is to simply checkout into your top troggle directory, into a folder called django.

If you want to use MySQL or Postgresql, download and install them. However, you can also use Django with Sqlite3, which is included in Python and thus requires no extra installation.



Troggle itself
-------------
Choose a directory where you will keep troggle, and svn check out Troggle into it using the following command:

svn co http://troggle.googlecode.com/svn/

If you want to work on the source code and be able to commit, you will need to use https instead of http, and your google account will need to be added to the troggle project members list. Contact aaron dot curtis at cantab dot net to get this set up.

Next, you need to fill in your local settings. Copy either localsettingsubuntu.py or localsettingsserver.py to a new file called localsettings.py. Follow the instructions contained in the file to fill out your settings.

Setting up tables and importing legacy data
------------------------------------------
Run "python databaseReset.py reset" from the troggle directory.

Once troggle is running, you can also log in and then go to "Import / export" data under "admin" on the menu.

Running a Troggle server
------------------------
For high volume use, Troggle should be run using a web server like apache. However, a quick way to get started is to use the development server built into Django.

To do this, run "python manage.py runserver" from the troggle directory.

