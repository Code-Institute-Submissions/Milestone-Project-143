## Introduction

The idea for my Milestone 3 project was to create a Project Management tool. As an engineering consultant, I work as a project manager or as part of a project team on a daily basis. I find often PM software are overly complex and result in PMs not using the correctly (or at all!) which reduces efficiency and the accuracy of business forecasts and resourcing. I wanted to see if I could create something simplier and more useable. 

The live webpage can be found [here](). Note I have created restrictions based on admin rights. To avail of the admin rights and explore the full functionality of the webpage create a user name beginning with "admin_". 

## Table of Contents
1. [UX](#ux)
    - [Goals](#goals)
        - [Employee Goals](#employee-goals)
        - [Project Manager Goals](#project-manager-goals)
        - [Company Goals](#company-goals)
    - [User Stories](#user-stories)
        - [Visitor Stories](#employee-stories)
        - [Project Manager Stories](#project-manager-stories)
        - [Company/Admin Stories](#company-stories)
    - [Design Choices](#design)
    - [Wireframes](#wireframes)
    - [Flowchart](#flowchart)

2. [Features](#features)
    - [Existing Features](#existing-features)
        - [Elements on every Page](#elements-on-every-page)
        - [Home Page](#home-page)
        - ....
    - [Features Left to Implement](#features-left-to-implement)

3. [Information Architecture](#information-architecture)
    - [Database choice](#database-choice)
    - [Data Storage Types](#data-storage-types)
    - [Collections Data Structure](#collections-data-structure)
        - [1st Collection](#1st-collection)
        - ...

4. [Technologies Used](#technologies-used)

5. [Testing](#testing)

6. [Deployment](#deployment)
    - [Heroku Deployment](#heroku-deployment)
    - [How to run this project locally](#local-deployment)

7. [Credits](#credits)
    - [Content](#content)
    - [Media](#media)
    - [Code](#code)
    - [Acknowledgements](#acknowledgements)

8. [Disclaimer](#disclaimer)

----

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


# Testing 



# Deployment

## Local Deployment

### Instructions


## Heroku Deployment

# Credits

## Content

- The text, images, links and other data in the database was sourced from various local websites including but not limited to:

    - ....

- ....

## Media

### Images
- 

## Code

-.... 

## Acknowledgements

## Disclaimer
The content of this website is educational purposes only.