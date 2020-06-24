# Sherit

## Pages

### Classes

    /

* Students (general users) see here a list of the classes in which there is content for them.  The links are: 

    * `/files/class`

* Users also see a list of the classes that they can edit. The links are: 
 
    * Manage: `/manage/class/` (only for users who own the class)
    * Members: `/members/class` ()

* There is a button to create a new class, leading to `/create`

### Files (two related pages)

    /files/class
    /share/class/student@email.edu

* The page displays a list of files for that class, either for the current logged-in user, or (if the logged in user is an editor of the page) for the student specified on the URL. 
* If the user is an editor of the page, there is also a button to upload files to the page.

The page is developed via a vue component that lists the files in the page. 

### Class member list

    /members/class
    
* The instructor sees a list of students in the class, and can click on each one, and go to `/folder/class/student@email.edu`.
* There is a button to upload a file to the whole class. 

### Class management

    /manage/class

This page is only visible to the instructor who created the page (not to others who can also add content to it).

* The instructor sees a list of other people who can manage the page, and can edit that list.
* The API key for the class is listed.  There is a button to randomly change it.
* The class name can be changed.

### Create class

    /create
    
A user can create a page to manage, and becomes the master of that page.  Once done, this redirects to `/manage/class`

## Database

### ClassManagers

* User
* Class ID (internally, the db refers to classes by ID)
* is_owner (boolean)
* Class creation date (for sorting)

### Class (ndb record)

* Class ID
* Class name
* API key for uploads

### File

* Class ID
* Student email
* File ID in GCS
* File name
* Mime type
* Upload date

### Queries

* List of classes where a user has files: 
    File join Class (to get the class name)
* List of classes one manages:
    ClassManagers join Class (to get the class name)
* List of files for a student in a class:
    File join Class
