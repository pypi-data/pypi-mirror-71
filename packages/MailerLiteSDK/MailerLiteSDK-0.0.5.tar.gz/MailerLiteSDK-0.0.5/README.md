This is a very early project for mailer lite



# USAGE
step 1:
Create a connect with your MailerLite API Key
```python
from MailerLiteSDK import MailerClient
mailer = MailerClient(api_key=os.getenv('MAILER_API_KEY'))
```

Step 2: 
Let user be subscriber first
```python
mailer.subscribe(email=sample_email)
>>>>>>> ad4c11537def6cf60f845ec13ab23e3c9bb74b9c
```




### REF
api document: https://developers.mailerlite.com/reference#update-subscriber

### UPLOAD TO PYPI
```
# change setup.py version
python setup.py sdist
twine upload -r pypi dist/* --verbose
```