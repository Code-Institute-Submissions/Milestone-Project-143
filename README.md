## Introduction

The idea for my Milestone 3 project was to create a Project Management tool. As an engineering consultant, I work as a project manager or as part of a project team on a daily basis. I find often PM software are overly complex and result in PMs not using the correctly (or at all!) which reduces efficiency and the accuracy of business forecasts and resourcing. I wanted to see if I could create something simplier and more useable. 

The live webpage can be found [here](http://ms3-project-manager-tool.herokuapp.com/index). Note I have created restrictions based on admin rights. To avail of the admin rights and explore the full functionality of the webpage create a user name beginning with "admin_". 

# UX

## Goals

### Employee Goals
- Find/edit tasks assigned to me
- Find deadline information for tasksr
- Mark tasks complete when finished
- Get contact details for other employees
- Edit employee profile

### Project Manager Goals
- Create, assign, edit and delete tasks as required
- Create, view, edit and delete tasks as required
- Create teams for my projects
- Contact employees and team members

### Company/admin Goals
- Provide easy platforrm for employees to use
- See details of all projects and clients
- View all employee details easily
- Full control to edit and delete all data

## User Stories

### Employee Stories

As an employee I expect:

1. To easily be able to navigate tasks assigned to me and understand the deadline and description.
2. To be able to easily find contact details for other employees.
3. See all tasks assigned to me on employee profile
4. Update my current progress on tasks. 
5. Edit my employee details easily

### Project Manager Stories

As a Project Manager I expect:

1. To easily view  projects I manage.
2. To create new my projects as needed. 
3. To create, read, update my clients.
4. To be able to add and review project details such as start date, end date view, team members etc.
5. Delete projects I manage.

### Company Stories

As a Company/Admin I expect: 

1. To be able to easily create, read, update and delete clients, projects, tasks.
2. To see all client detail, project details and employee details with ease.

## Design

The website is overall intended to be simplistic with information easy to see and navigate. The following design choices were made with this in mind:

### Fonts
- Fonts used were Roboto and opens sans, chosen as they are easy to read and clear.  

### Icons
- font awesome icons were used throughout to simplify the user experience and complement the modern design.

### Colours
- Neutral colours were chosen for the background of the main pages, with the exception of the home,login and register pages which used an image background for impact.
The colours were used to frame the website and draw attention to section of data. The main accent colours used are show below. 

<img src="./static/images/colours.jpg" width="75%" >

### Styling

In terms of general styling the website was created using bootstrap and while customised used many of bootstrap inbuilt styling features.

## Wireframes

These wireframes were created using [Balsamiq](https://balsamiq.com/) during the planning process for this project. Whilst, the design evolved during development the wireframes still give a distinct impression of what the design intention was at the project outset. 

- Home/ Login Page 
    - [Desktop](project_planning/wireframes/desktop_home.png)
    - [Tablet](project_planning/wireframes/tablet_home.png)
    - [Mobile](project_planning/wireframes/mobile_home.png)
- User Profile/Dashboard
    - [Desktop](project_planning/wireframes/desktop_profile.png)
    - [Tablet](project_planning/wireframes/tablet_profile.png)
    - [Mobile](project_planning/wireframes/mobile_profile.png)
- [Client/Project/Employee/task Directories (Same Layout for each)
    - [Desktop](project_planning/wireframes/desktop_directories.png)
    - [Tablet](project_planning/wireframes/tablet_directories.png)
    - [Mobile](project_planning/wireframes/mobile_directories.png)
- [Project Home Page]()
- [Admin Home Page]()

### Flowchart

The intital webpage flowchart done as part of the planning process is saved [here](project_planning/flowcharts/flowchart.png)

This flowchart was created using [draw.io](https://www.draw.io) to plan and explain the flow and interactions between webpages. 

# Features
 
## Existing Features

### Elements on every page
- Navbar: The navbar contains links to all other pages. The content is dynamic with the navlink that are displayed based on whether the user/employee is logged in. 
The active nav link is changed using jquery as it couldn't be applied statically due to use of templates.
- Logo & Company Name: The logo was designed specifally for the website and appear on all page, the company name appear depending on the screen width. 
    
### Employee Profile
The employee is brought to their personalised profile page upon login or registering. 
This contains the followinf features:

- Profile: Display image of the employee (stored on aws) with all their details beneath including title, email, etc. Display manager name which can be clicked to navigate to manager's profile. 
- Project Info: Page displays both Projects the employee is manager off and projects for which they are on the team. Project Name, client, fee, start and end date. The project description can be read via the 'read more' button which is implemented using JQuery. There is a link to edit projects for project which the signed in user, or admin, manages. 
- Task Info: With the task display, there are 3 section for tasks to do, task in progress and task completed all of which have been assigned to the employee. These tasks also have a link to edit form the profile page. 

### Directories

There are 4 directories for Clients, Projects, Employees and tasks which can be navigated to via the dropdown nav menu. 

The directories are all designed in a similar way and contain the following:
- Collaspsible button to display form to add new client, project, task. Note new employees can only be added through registration. 
- Search box. Indexes have been developed for each directories based on the following:
1. Clients: Name, Contact Person, address and id
2. Employees: First & Last name
3. Tasks: task name and description
4. Projects: task name and description
- Directory list. When the page loads this display all documents within each directory/collection which can then be filtered based on the above search box. There is a reset button next to the search box to return to all results in the collection. 
The accordian collapible can be clicked to reveal more info on the results. Dependent on the right of the user there will also be options to edit or delete the result/document from the collection. Admin can delete all results. Other users will need to the owner/manager of the document. 


## Features Left to Implement

I wanted to try develop a basic project management tool as its relevent to my work. In reality with more time and resoucres there would be many features worth adding, some of which I've listed below. 

- In practice the data would be more suited to being implemented with a relation database which would project the integrity more. Having foreign and primary keys would also cut done on the amount of loops. 
- Link task deadline and project dates to calender
- Assign tasks only to team members of a project
- Notification system to let employees know when they been assigned a new task or project

# Technologies Used

### Database Choice
As stated above, a rdms would be have been better suited to the project but as this was not the requirements of the project [MongoDB](https://www.mongodb.com/) has been used. A S£ bucket was also used for [AWS server](https://eu-west-1.console.aws.amazon.com/console/home?region=eu-west-1#) for the storage of images the url of which is passed back to MongoDB

### Tools
- ....

### Languages

* [HTML5](https://en.wikipedia.org/wiki/HTML5)
* [CSS3](https://en.wikipedia.org/wiki/Cascading_Style_Sheets)
* [JavaScript](https://www.javascript.com/) 
* [Python](https://www.python.org/)

### Frameworks, Libraries and Programs Used

- [Bootstrap v4.5.0](https://getbootstrap.com/) - Used for the responsove layout as well as custom components such as forms, modal popups, navigation bar, footer, cards and collapsable element.
- [jquery](https://jquery.com/) - Used in some of the clickable elements such as collapsable 'hamburger' nav bar.
- [popper.js](https://popper.js.org/) - Used in some of the clickable elements such as collapsable 'hamburger' nav bar. 
- [Font Awesome](https://fontawesome.com/) - Font Awesome was used to add icons to hero image and social media icons.
- [Google Fonts](https://fonts.google.com/) - Google Fonts was used to import 'Roboto' and 'Amatic SC' fonts in the style.css stylesheet.
- [Git](https://git-scm.com/) - Git was used to allow for tracking of any changes in the code and for the version control.
- [GitPod](https://www.gitpod.io/) - GitPod, conected to GitHub, hosted the coding space and allowed the projected to be commited to the Github repository.
- [Github](https://github.com/) - GitHub is used to host the repository and publish the live website by using Git Pages.
- [Google Chrome developer tools](https://developers.google.com/web/tools/chrome-devtools) for testing and troubleshooting.
- [W3C Markup Validation](https://validator.w3.org/) used to validate HTML.
- [W3C CSS validation](https://jigsaw.w3.org/css-validator/) used to validate CSS.
- [Tiny jpg](https://tinyjpg.com/) - Used to reduce image size.
- [Resize Image](https://resizeimage.net/) -  Used to Further reduce images.
- [PyMongo](https://api.mongodb.com/python/current/) for communication between Python and MongoDB.
- [Flask](https://flask.palletsprojects.com/en/1.0.x/) to construct and render pages.
- [Jinja](http://jinja.pocoo.org/docs/2.10/) to display data from the project backend in the rendered html.

## Testing

#### Code Validation

Each page was ran through the W3C HTML validator, the stylesheet through the CSS validator and the javascript files through JS hint. The following errors were flagged and corrected:

- Images missing alt attribute;
- Frameborder obselete for iframe;
- type for javascript sources not required;
- Missing semicolons and unnesscessary semicolons in JS files;

There was additional warnings for the JavaScript files which highlighted undefined functions and variables, however these are defined in external JS libraries read in prior to the project JS files. There was also some warnings in relation to Internet Explorer compatibility which could not be addressed.

#### Browser Compatibility

The live website, hosted on gitpages, has been opened and tested on multiple browsers for responsives and intended appearance. Browers tested included:

* Google Chrome
* Safari
* Microsoft Edge
* Internet Explorer
* Firefox
* Opera

Overall the website worked well and appeared as intended on different sizes across different browsers. 

#### Responsiveness

The website has been tested across multiple screen sizes using [Google Chrome developer tools](https://developers.google.com/web/tools/chrome-devtools) for a range of screen sizes, portrait and landscape, including:

- Moto G4
- Galaxy S5
- Pixel 2
- Pixel 2 XL
- iPhone 5 SE
- iPhone 6/7/8
- iPhone 6/7/8 Plus
- iPhone X
- iPad
- iPad Pro

The screen was also adjusted through various sizes and breakpoints with the responsive option in developer tools. The website was also opened and checked on Samsung A20 & iPhone SE mobile devices as well as Dell xps 15, Lenovo Think Pad and Apple Macbook. The responsiveness was also tested on the browsers outlined above with no noted issues. Overall the website appeared as intended across each screen type. There were some intial errors particularly on iPhone5 screen size (320px width) with overflows of titles. However, an additional media query was added to address this and all screens less than 400px approximately. 

# Deployment

## How to run this project locally

The following **must be installed** on your machine:
- [PIP](https://pip.pypa.io/en/stable/installing/)
- [Python 3](https://www.python.org/downloads/)
- [Git](https://gist.github.com/derhuerst/1b15ff4652a867391f03)
- An account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or MongoDB running locally on your machine. 
    - How to set up your Mongo Atlas account [here](https://docs.atlas.mongodb.com/).

### Instructions
1. Save a copy of the github repository located at https://github.com/AJGreaves/familyhub by clicking the "download zip" button at the top of the page and extracting the zip file to your chosen folder. If you have Git installed on your system, you can clone the repository with the following command.
```
git clone https://github.com/AJGreaves/familyhub
```

2. If possible open a terminal session in the unzip folder or cd to the correct location.

3. A virtual environment is recommended for the Python interpreter, I recommend using Pythons built in virtual environment. Enter the command:
```
python -m .venv venv
```  
_NOTE: Your Python command may differ, such as python3 or py_

4. Activate the .venv with the command:
```
.venv\Scripts\activate 
```
_Again this **command may differ depending on your operating system**, please check the [Python Documentation on virtual environments](https://docs.python.org/3/library/venv.html) for further instructions._

4. If needed, Upgrade pip locally with
```
pip install --upgrade pip.
```

5. Install all required modules with the command 
```
pip -r requirements.txt.
```

6. In your local IDE create a file called `.env`.

7. Inside the .env file, create a SECRET_KEY variable and a MONGO_URI to link to your own database and links to AWS server.

8. You can now run the application with the command
```
python app.py
```

9. You can visit the website at `http://127.0.0.1:5000`

## Heroku Deployment

To deploy the website to heroku, take the following steps:

1. Create a `requirements.txt` file using the terminal command `pip freeze > requirements.txt`.

2. Create a `Procfile` with the terminal command `echo web: python app.py > Procfile`.

3. `git add` and `git commit` the new requirements and Procfile and then `git push` the project to GitHub.

3. Create a new app on the [Heroku website](https://dashboard.heroku.com/apps) by clicking the "New" button in your dashboard. Give it a name and set the region to Europe.

4. From the heroku dashboard of your newly created application, click on "Deploy" > "Deployment method" and select GitHub.

5. Confirm the linking of the heroku app to the correct GitHub repository.

6. In the heroku dashboard for the application, click on "Settings" > "Reveal Config Vars".

7. Set the following config vars:

| Key | Value |
 --- | ---
DEBUG | FALSE
IP | 0.0.0.0
MONGO_URI | `mongodb+srv://<username>:<password>@<cluster_name>-qtxun.mongodb.net/<database_name>?retryWrites=true&w=majority`
PORT | 5000
SECRET_KEY | mongodb secret key generated by user
S3_SECRET_ACCESS_KEY| AWS key
S3_ACCESS_KEY | aws key

- To get you MONGO_URI read the MongoDB Atlas documentation [here](https://docs.atlas.mongodb.com/)

8. In the heroku dashboard, click "Deploy".

9. In the "Manual Deployment" section of this page, made sure the master branch is selected and then click "Deploy Branch".

10. The site is now successfully deployed.

# Credits

## Content

- The content is by and large created by me but I did source free to use images for employ profile on unsplash credits listed below. 

- Robert: Photo by Ali Morshedlou on Unsplash
- Ruth: Photo by Annika Palmari on Unsplash
- John: Photo by Dragos Gontariu on Unsplash
- Graham: Photo by Austin Wade on Unsplash
- Sinead: Photo by Christopher Campbell on Unsplash
- barry: Photo by Robert Godwin on Unsplash
- Ian: Photo by bantersnaps on Unsplash
- Brian: Photo by Joseph Gonzalez on Unsplash
- Sheelagh: Photo by Patrik Velich on Unsplash

Though heavily adapted I did refer extensively to the task manager example within the course as part of my project. 

### Acknowledgements

I'd like to thank my mentor, Precious Ijege, for his time, advice and patience on this project. I should also thank various friends and family member who took time to review and provide feedback

## Disclaimer
The content of this website is educational purposes only.