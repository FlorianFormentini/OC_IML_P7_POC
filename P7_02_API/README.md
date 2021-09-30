# [Hera-Project](https://hera-project.herokuapp.com)
All features are documented on the `/api` route : https://hera-project.herokuapp.com/api/
## Run the app (local) :

**Run :** `$ python manage.py run`
**Execute tests :** `$ python manage.py test`

- To change the app enviromnent, you have to modify two environment variables stored in the **`.flaskenv`** file: `FLASK_ENV` and `HERAPROJECT_ENV`
    - `FLASK_APP=app` - Define the app package, do not change it.
    - `FLASK_ENV : {'development', 'production'}` - Define the app environment. Need to be loaded before the app instance creation.
    - `CONFIG_ENV : {'dev', 'prod'}` - Used configuration (a third type `'test'` also exist but it's automatically set when testing).


- You also need to create a **`.env`** file containing thes environnment variables :
    - `SECRET_KEY=[dev_secret_key]` - The key to send in the requests header to verify the users
    - `FB_VERIFY_TOKEN=[facebook_verify_token]` - The key to verify the Facebook App
    - `PAGE_ACCESS_TOKEN=[facebook_page_access_token]` - The key to verify the Facebook Page
    - `GOOGLE_APPLICATION_CREDENTIALS=[local_path_to_GC_credentials_json]` - Path to the json file with all Google Cloud credentials

### Database migrations
`$ flask db init` (only the first time to create the local DB)  

```bash
$ flask db migrate -m "some migration msg"
$ flask manage.py db upgrade
```


### Run the tests
`$ python manage.py test`

### Deploy new features
Currently the app is hosted on a Heroku server with continuous deployment. It means that after every changes on the master branch, Heroku is pushing to a remote repository.  
After some changes in the develop branch :  
```bash
$ git add -A
$ git commit -m "some commit message"
$ git checkout master
$ git merge develop
```
After a few seconds, the new version is deployed online.  
The first deploy and the host configuration are detailled in the official documentation.


