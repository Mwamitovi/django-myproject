
As adapted from th django-cookbook

Django apps (utils for different functionalities that are shared throughout the project)

a locale directory for your project translations if it is multilingual;

a Fabric deployment script named fabfile.py,

the externals directory for external dependencies that are included in this project if you decide not to use pip requirements:
	- libs directory -- for the Python modules that are required by your project, for example, boto, Requests, Twython, Whoosh, and so on.
	- apps directory -- for third-party Django apps, for example, django-cms, django-haystack, django-storages, and so on.
	
		Note: I highly recommend that you create the README.txt files in the libs and apps directories, 
		      where you mention what each module is for, what the used version or revision is, and where it is taken from.

create the requirements directory with these text files: 
	- base.txt for shared modules, 
	- dev.txt for development environment, 
	- test.txt for testing environment, 
	- staging.txt for staging environment, 
	- and prod.txt for production.

In your project's Python package, myproject, 
	- create the media directory for project uploads,
	- should contain your project settings, the settings.py and conf directories ie. myproject/conf/...
		(read about this in the Configuring settings for development, testing, staging, and production environments recipe), 
			- base.py: should have the shared settings (as inititated by django)
			- all the other settings under myproject/conf/... should extend the 'base.py'
			- myproject/settings.py should extend any of the conf/... eg. from .conf.dev import *
			
		- By default, the Django management commands use the settings from myproject/settings.py. 
		  Using the method that is defined in this setup, we can keep all the required non-sensitive settings for all 
		  environments under version control in the conf directory.
		  Whereas, the settings.py file itself would be ignored by version control and will only contain the settings that are necessary 
		  for the current development, testing, staging, or production environments.
			
		
	- And have the urls.py URL configuration.

	- the site_static directory for project-specific static files,
		- create the site directory as a namespace for sitespecific static files. Then, separate the separated static files in directories in it:
				For instance, scss for Sass files (optional), css for the generated minified Cascading Style Sheets, img for styling images and logos, 
				 js for JavaScript, and any third-party module combining all types of files such as the tinymce rich-text editor.
		- Besides the site directory, the site_static directory might also contain overwritten static directories of third-party apps, 
				for example, cms overwriting static files from Django CMS. 
				To generate the CSS files from Sass and minify the JavaScript files, you can use the CodeKit or 
				Prepros applications with a graphical user interface.

	- the static directory for collected static files,

	- the tmp directory for the upload procedure,

	- the templates directory for project templates: And put your templates that are separated by the apps in your templates directory. 
		- If a template file represents a page (for example, change_item.html or item_list.html), then directly put it in the app's template directory. 
		- If the template is included in another template (for example, similar_items.html), put it in the includes subdirectory. 
		- Also, your templates directory can contain a directory called utils for globally reusable snippets, such as pagination, language chooser, and others.
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	