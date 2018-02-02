PartyBarge Car Catalog:

Final Project: The Backend:Databases & Applications. 

Project: Build an Item Catalog

Developed an application that provides a list of items within a variety of categories as well as provide 
a user registration and authentication system(Google+). Registered users have the ability to post, edit and 
delete their own items. Users will also be abble to query Catolog Database using JSON API calls.

Required installed software/applications:

1. Unix/Linux Terminal, Windows Users - GitBash Program
2. Browser (ie. Google Chrome,Firefox..etc).
3. VM VirtualBox - VirtualBox actually runs the VM. Download 
   @ https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
4. Vagrant - Vagrant is the software that configures the VM and lets you share files between your host computer and the 
   VM's filesystem. You can download it from vagrantup.com. Install the version for your operating system. 
   Downlaod @ https://www.vagrantup.com/downloads.html
5. From Github: Fork or clone Partybarge Car Catalog respository into a directory.


To Run Catolog Project:

Set up a Google Plus auth application.
1. go to https://console.developers.google.com/project and login with Google.
2. Create a new project
3. Name the project
4. Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5. Select Web Application
6. On the consent screen, type in a product name and save.
7. In Authorized javascript origins add:
    http://0.0.0.0:8000
    http://localhost:8000 
8. Click create client ID
9. Click download JSON and save it into the root director of this project. 
10. Rename the JSON file "client_secret.json"
11. In login.html replace the line
	"data-clientid="117774169906-v8mh2gpdput21q5g70fvcsut5irgrl1h.apps.googleusercontent.com" so that it uses your Client 
	ID from the web applciation. 

Setup the Database & Start the Server
1. In the Directory that you created earlier , use the command "vagrant up"
2. The vagrant machine will install.
3. Next type "vagrant ssh"
4. At the cmd prompt, cd /vagrant
5. Load the database setup file: $python catalog_dbsu.py
6. Then load some database with some initial data: $python Cats_Items.py
7. Now start the server: $python catalog.py 

Open in a Web Browser:
1. Use following addresses to access Partybarge Car Catolog:
    http://0.0.0.0:8000
    http://localhost:8000


Thanks:

1. Udacity
2. Stack Overflow
3. Google
4. w3schools

