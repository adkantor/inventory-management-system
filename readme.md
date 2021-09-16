# **Inventory Management System** <br/> *Capstone Project for CS50's Web Programming with Python and JavaScript*

## Description of the application
The application serves as an inventory management system of an imaginary scrap metal trading company. The application allows
- recording partners (vendors and customers),
- recording of material groups and materials,
- recording transactions (receipt and sale of materials),
- recording transaction related documents (goods receipt notes and goods delivery notes)
- PDF generation for such documents,
- recording employees with different permissions to this system and
- producing interactive reports (dasboard with multiple charts, daily-weekly-monthly summary reports and filterable transaction list).

Speciality of the business is that prices (both buying and selling) are not predetermined in the database but are negotiated transaction by transaction. Therefore different prices are to be manually recorded for each transaction.

Although many functions were implemented in this capstone project, a real-life application would require much more functionalities. Missing function are for example:
- ability to manually record special transactions, such as counting surplus/loss, with proper views and related documents
- fully traceable records (for each transaction record who and when did any change).  

## <br/>Goals of the project
My goal for this project was not only to implement the subtleties of the course syllabus but to go well beyond it and experiment with areas touched only superficially or not at all.

A list of such goals preliminary set up for this project:
- use of *PostgreSQL* as backend database
- use of *Docker* for development environment
- use of *Bokeh* to produce interactive charts
- use of *Bootstrap Table* to produce interactive tables
- advanced authentication using *django-allauth* including email notifications (also using Django's signal dispatcher)
- use of *xhtml2pdf* to prepare PDF documents
- use of Django's *permission* system to manage who has access to which views
- tinker with class based views
- make some more complicated forms involving *formsets* and finetuning *django-crispy-forms*
- make the app *production-ready*, including application of the needed security settings

Part of the above goals and their implementation was heavily inspired by the great books of ***William S. Vincent***:
- [Django for Beginners](https://djangoforbeginners.com/)
- [Django for Professionals](https://djangoforprofessionals.com/)


## <br/>Distinctiveness and Complexity
I believe this app, being an *Enterprise System*, is **distinctive** enough from other projects in the course, especially from the e-commerce project. Here, transactions happen outside of the app (vs. an e-commerce app), this application serves for recording such transactions and its main purpose is not the transactioning itself but to support the workflow (e.g. produce official documents) and gratify reporting needs of management.

The **complexity** of this app goes well beyond the complexity of other projects in the course:
- it involves 6 applications (plus django-allauth's built-in 'accounts' application)
- it contains 9 models
- it involves 40+ views, some of them with complex forms, plus some other endpoints to serve async requests
- it contains many complex queries to support reporting function
- makes use of several Django functions (e.g. permissions, signals) and external libraries to support functional requirements
- contains 100+ tests
- contains 170+ files

## <br/>How to run the application
### <br/>Build images and run with Docker
In the root directory, run command 
>```docker-compose up -d --build```

### <br/>Run without Docker, using pip
Within your virual environment, run commands:
>```python -m pip install requirements.txt```<br/>
>```python manage.py runserver```


## <br/>Functional overview of the application.

### ***Homepage*** (Navbar: Home)
This is a simple static landing page for the authenticated users, no actions are available here.


### ***Management of Goods Receipt Notes*** (Navbar: Goods Receipt)
On this page the user finds an ordered list of all Goods Receipt Notes (*hereinafter GRNs*), with the latest GRN on the top. Two available actions here: 
- create new GRN by clicking the respective button;
- view details of a GRN by clicking on the row of the chosen GRN.

When creating new GRN
- user has to supply the document-level data (e.g. date, vendor);
- user can add one or more transactions, each with their respective transaction-level data (e.g. material, weight, unit price).

Clicking on a record, the user is redirected to the page showing the details of the GRN. The available actions here by clicking on one of the buttons:
- Modify the document;
- Delete the document;
- Go back to the list view;
- Create a PDF document (if not yet exists) or view the existing PDF (if already created).


### ***Management of Goods Delivery Notes*** (Navbar: Goods Delivery)
On this page the user finds an ordered list of all Goods Delivery Notes (*hereinafter GDNs*), with the latest GDN on the top. Two available actions here: 
- create new GDN by clicking the respective button;
- view details of a GDN by clicking on the row of the chosen GDN.

When creating new GDN
- user has to supply the document-level data (e.g. date, customer);
- user can add one or more transactions, each with their respective transaction-level data (e.g. material, weight, unit price).

Clicking on a record, the user is redirected to the page showing the details of the GDN. The available actions here by clicking on one of the buttons:
- Modify the document;
- Delete the document;
- Go back to the list view;
- Create a PDF document (if not yet exists) or view the existing PDF (if already created).


### ***Vendor master data*** (Navbar: Master Data > Vendors)
On this page the user finds a list of all vendors in alphabetical order. Two available actions here: 
- create new vendor by clicking the respective button;
- view details of a vendor by clicking on the row of the chosen vendor.

Clicking on a record, the user is redirected to the page showing the details of the vendor. The available actions here by clicking on one of the buttons:
- Modify the vendor data;
- Delete the vendor;
- Go back to the list view;


### ***Customer master data*** (Navbar: Master Data > Customers)
On this page the user finds a list of all customers in alphabetical order. Two available actions here: 
- create new customer by clicking the respective button - accessible only to users with proper permission;
- view details of a customer by clicking on the row of the chosen customer.

Clicking on a record, the user is redirected to the page showing the details of the customer. The available actions here by clicking on one of the buttons:
- Modify the customer data - accessible only to users with proper permission;
- Delete the customer - accessible only to users with proper permission;
- Go back to the list view;


### ***Material group master data*** (Navbar: Master Data > Material Groups)
On this page the user finds a list of all material groups in alphabetical order. Two available actions here: 
- create new material group by clicking the respective button - accessible only to users with proper permission;
- view details of a material group by clicking on the row of the chosen material group.

Clicking on a record, the user is redirected to the page showing the details of the material group. The available actions here by clicking on one of the buttons:
- Modify the material group data - accessible only to users with proper permission;
- Delete the material group - accessible only to users with proper permission;
- Go back to the list view;


### ***Material master data*** (Navbar: Master Data > Materials)
On this page the user finds a list of all materials in alphabetical order. Two available actions here: 
- create new material by clicking the respective button - accessible only to users with proper permission;
- view details of a material by clicking on the row of the chosen material.

Clicking on a record, the user is redirected to the page showing the details of the material. The available actions here by clicking on one of the buttons:
- Modify the material data - accessible only to users with proper permission;
- Delete the material - accessible only to users with proper permission;
- Go back to the list view;


### ***Dashboard*** (Navbar: Reports > Dashboard) - accessible only to users with proper permission
This is an interactive dashboard withs charts and tables. Users can change views by clicking on tabs of the chart and can gain supplementary information by hovering over chart elements.

Available charts/tables
- *Summary Sales and Purchases*: multi-level piechart showing the composition of the sales / purchases of the last 30 days by material and by material group.
- *Stock levels*: barchart showing daily stock levels for the chosen material group
- *Weekly Sales and Purchases*: stacked barchart showing the total value of weekly sales and purchases and their balance (margin) as a line graph.
- *User statuses*: table showing all users and their respective last login time.


### ***Transaction report*** (Navbar: Reports > Transaction report) - accessible only to users with proper permission
This is an itemized list of all transactions. The list can be filtered in many ways using the form on the page, as well as sorted by any of the columns by clicking on the header of the respective column.


### ***Summary report*** (Navbar: Reports > Summary report) - accessible only to users with proper permission
This is a summary view of the business: transactions are grouped by the chosen resolution (daily-weekly-monthly) and data is filterable in many ways.

The report, for each record, shows:
- starting/ending date of the period
- opening / closing inventory balance
- opening / closing inventory value
- opening / closing unit price
- total weight of purchased / sold items
- total value of purchased / sold items
- average unit price of purchased / sold items. 


### ***Employee administration*** (Navbar: Employee Admin) - accessible only to users with proper permission
On this page the user finds a list of all users (employees of the company) in alphabetical order. Two available actions here: 
- create new employee (=signup new user) by clicking the respective button;
- view details of an employee by clicking on the row of the chosen employee.

Clicking on a record, the user is redirected to the page showing the details of the employee. The available actions here by clicking on one of the buttons:
- Modify the employee data - username and email data cannot be modified;
- Delete the employee - a user is not allowed to delete itself;
- Go back to the list view;

When creating a new user, a password should not be given. Instead, an email notification is sent to the newly-created user prompting it to set its password. Furthermore, permission group applicable for the user is to be set here.


### ***Profile page*** (Navbar: Profile picture on the right side > Profile)
On this page the user can see its personal data: name, username, email address, permission groups, profile photo. Available actions here:
- Edit personal data: only first/last name and profile picture can be modified by the user.
- Change password
- manage email-addresses: user can add/remove email addresses here
- go back to previous view


## <br/>Overview of the files

>Note: files added automatically that were not modified (e.g. migration files, \_\_init \_\_.py, apps.py) are not listed below.

### <br/>Root-folder files
- ***Dockerfile*** and ***docker-compose.yml***: serve to build and run Docker image, handle virual environment, installation of required packages and volumes (database and code) to attach to
- ***Pipfile*** and ***Pipfile.lock***: serve to manage virual environment and installation of required packages, using *Pipenv* tool
- ***requirements.txt***: serve to install required packages, using *pip*
- ***manage.py***: Django's command-line utility

### <br/>Project-level files
#### ***ims\_project*** folder
- ***settings.py***: several settings were added to serve the app, among others:
    - templates directory moved to a central location in the root folder
    - settings for media and static directories
    - settings related to postgres database
    - settings related to *django-allauth* authentications library and settings related to email notifications (as per current settings emails are not actually sent out - no email sending service provider is set - but instead they are outputted to the command line console)
    - settings related to *django-crispy-forms*
- ***urls.py***: contains top-level paths for local apps, django admin and user management


#### ***media*** folder
This is the directory for
- uploaded profile pictures
- generated PDF documents (Goods Receipt Notes and Goods Delivery Notes).


#### ***static/css*** folder
- ***dashboard.css***: styling for the dashboard within *reports* app.
- ***navbar-top-fixed.css***: styling for navbar.
- ***summary_report.css***: styling for the summary report within *reports* app.


#### ***static/img*** folder
- ***favicon.ico***: favicon for the site.
- ***logo.png***: logo image for the site.
- ***profile_picture_placeholder.png***: placeholder image if no profile picture exists for the user.


#### ***static/js*** folder
- ***dashboard.js***: JavaScript code responsible for updating dasboard charts.
- ***jquery.formset.js***: JavaScript code responsible for user-friendly handling of formsets (adding/removing form elements) of Goods Receipt/Delivery Notes views. The code was originally written by *Stanislaus Madueke* (see credits within the file) but some corrections needed to be done in order to properly handle deletions.
- ***pdf_generation.js***: JavaScript code responsible for launching pdf generation / pdf file opening and asynchronously updating a button (design and functionality) on the page.
- ***summary_report.js***: JavaScript code responsible for populating the form for the summary report and updating the report based on parameters selected by the user on the form.
- ***transactions_report.js***: JavaScript code responsible for populating the form for the transaction report and updating the report based on parameters selected by the user on the form.


#### ***templates*** folder
Contains templates for the views.

The templates within the ***templates/account*** subfolder override built-in templates of *django-allauth*. The templates with `.txt` extension (within ***templates/account/email***) are templates of email messages.

Generally, 5 templates exist for each model to support list view and CRUD (Create-Read-Update-Delete) functions.

The ***reports*** app has 3 templates for the 3 views (dashboard, summary report, transaction report) plus 2 templates supporting the dashboard view: ***dashboard_content.html*** and ***dashboard_table.html***. When rendering the dashboard, on the frontend the JavaScript code makes async requests, on the backend the support templates are first rendered (Bokeh charts or tables) then returned to the caller functions, then the raw html code is sent back to the frontend where the JS code puts them in their respective div. 

#### ***templatetags*** folder
Responsible for registering custom template tags. In this case one such tag is used: `startswith`. This tag is used in multiple templates to support conditional rendering according to the start of URL name (e.g. within ***partner_detail.html*** the wording of some elements are different if the URL nape starts with `vendor` or if it starts with `customer`).


### <br/>***documents*** app
>This app represents documents (Goods Receipt Notes and Goods Delivery Notes). Each document relates to one or more transactions (inbound or outbound, depending on the document) as well as a partner (vendor or customer, depending on the document). Also, apart from the UUID of the record, each document has a human readable unique, monotonically increasing ID, e.g. *GRN2021/000126*

- ***admin.py***: includes some customization to admin site views and registration of related models.
- ***custom\_layout\_objects.py***: includes a class to support complex forms.
- ***forms.py***: contains app related forms, mainly as customization of *django-crispy-form*-s.
- ***models.py***: incudes models *GoodsReceiptNote* and *GoodsDispatchNote* and related static methods and utility functions (e.g. to support generation of PDF files).
- ***render.py***: contains a utility function to support PDF rendering from html template, using *xhtml2pdf* library.
- ***tests.py***: contains unit tests to check 
    - the model itself
    - all views, tested each as logged-out user, logged-in user without special permission and, if applicable, user with special permission.
- ***urls.py***: contains paths for each view.
- ***views.py***: contains endpoint for each view (mainly as class-based views) as well as endpoint for PDF generation and rendering.


### <br/>***inventories*** app
>This app represents inventory items (Materials), their grouping (Material Groups) and their movements (Transactions). A material can have one sole parent group (e.g. alu can > aluminium) or no parent group. A transaction always applies to one material, has a type (on either inbound or outbound), has a partner (Customer or Vendor, depending on the type) and may or may not attached to a document (Goods Receipt Note or Goods Delivery Note, depending on the type).

- ***admin.py***: includes registration of related models
- ***models.py***: incudes models *MaterialGroup*, *Material* and *Transaction* and related static methods and utility functions (e.g. to support different reporting views).
- ***tests.py***: contains unit tests to check 
    - the model itself
    - all views, tested each as logged-out user, logged-in user without special permission and, if applicable, user with special permission.
- ***urls.py***: contains paths for each view.
- ***views.py***: contains endpoint for each view (class-based views).


### <br/>***pages*** app
>This app contains one sole view serving as a static landing page (homepage) for logged in users.

- ***tests.py***: contains unit tests to check the view as logged-out user and logged-in user.
- ***urls.py***: contains paths for the view.
- ***views.py***: contains endpoint for the view (class-based view).


### <br/>***partners*** app
>This app represents partners (Customers or Vendors).

- ***admin.py***: includes registration of related models
- ***models.py***: incudes models *Vendor* and *Customer*, both inherited from parent class *Partner* and related static methods and utility functions (e.g. to get full address from multiple fields).
- ***tests.py***: contains unit tests to check 
    - the model itself
    - all views, tested each as logged-out user, logged-in user without special permission and, if applicable, user with special permission.
- ***urls.py***: contains paths for each view.
- ***views.py***: contains endpoint for each view (class-based views).


### <br/>***reports*** app
>This app represents three different interactive management reports:
> - a dashboard with charts showing inventory levels, sales and purchases and user statuses;
> - a summary report showing opening-closing balances and inventory movements (both volume and value) summarized by a selected window (daily-weekly-monthly) and by level (selected material or material group).
> - an itemized transaction report showing all transactions, filterable by date, material, material group, type, also sortable by each dimension.

- ***models.py***: exceptionally, this app does not contain database models but only utility functions to serve reports, each returning its result in a serialized form (dictionary).
- ***tests.py***: contains unit tests to check 
    - utility and support functions
    - all views, tested each as logged-out user, logged-in user without special permission and, if applicable, user with special permission.
- ***urls.py***: contains paths for each view and API routes (asynchronously serving reports)
- ***views.py***: contains endpoint for each view (class-based views for page views and function based views for API routes).


### <br/>***users*** app
>This app represents users of the app (employees of the company). It is also responsible for user management e.g. signup of new users.<br/>
>Special customisation were needed as new users cannot sign-up themselves but only another employee with proper permission (e.g. a manager) can create new user profiles. Therefore passwords are not set by the creator but a password reset is done immediately and an email notification is sent to the newly-created user.

- ***adapter.py***: placeholder for customization of *django-allauth* functionalities. Currently it has no special functionality.
- ***admin.py***: includes some customization to admin site views and registration of related models. Here, we also restrict access of the admin login page to already authenticated users. The reason behind is that the normal admin login comes round the authentication procedure of *django-allauth*. With this setting *django-allauth* gatekeeping is always enforced.
- ***apps.py***: includes initialization of user related signals.
- ***forms.py***: some of the built-in forms of *django-allauth* are overridden here (inclusion of new fields, omit password fields, send signal at creation in order to reset password.)
- ***models.py***: incudes model *CustomUser* and related static methods and utility functions (e.g. to get full name from multiple fields or to get status info in a serialized form to be consumed by a report).
- ***signals.py***: contains a signal receiver that performs reset of password and sends out a notification email.
- ***tests.py***: contains unit tests to check 
    - the model itself
    - all views, tested each as logged-out user, logged-in user without special permission and, if applicable, user with special permission.
- ***urls.py***: contains paths for each view.
- ***views.py***: contains endpoint for each view (class-based views).