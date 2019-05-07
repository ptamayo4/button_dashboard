# IoT Button Dashboard
This is a Django application that does a few things:

    - Allows creation of Project entities in database so we can test Lambda functions by using an Amazon Dash button, without paying $20 for the purpose-built IoT Button.
    - Monitors the network it's running on for Dash Button Presses.
    - Allows hot-swapping of bound lambda function to easily change the functionality of Dash Button

Note: This currently works for Mac only. Additional software is required for Windows and more testing is required.

In order to use the tool, first create a virtualenv

```
virtualenv venv --python=python3
```

Then go ahead and activate it:

```
Mac:
source venv/bin/activate
```

After that, go ahead and install all required packages by reading from the requirements.txt:

```
pip install -r requirements.txt
```

Finally, you should be able to run the server. But before you do so, make sure to make migrations so the database is prepped:

```
python manage.py makemigrations
python manage.py migrate
```

And run the server:

```
python manage.py runserver
```

You should find an ugly landing page at localhost:8000

The general flow will be to add a Project Name and a Lambda Endpoint. Then, you should see a Test link, a Bind link, and a Delete link appear in the table below. Testing will emulate the Button press by calling the Lambda Endpoint directly from the Django app. Binding will make it so the Dash Button will trigger a specific endpoint, and we can test pressing the button now.

All of the functionality can be tested without having a physical Amazon Dash button, simply by clicking the 'Test' link.
However, if you do have a handy Dash button lying around, there are a few more steps required and you can get the button working on your network.

1. Start the process of pairing a Dash Button using the Amazon mobile application.
2. Complete the binidng until the point where you choose a product, and then simply cancel the setup process.
3. The button will now be connected to the network, however won't arbitrarily order products now.
4. Using a tool like WireShark, we can monitor the network to get the MAC of the button at this point.
5. Look for the device whose Source contains 'Amazon', and then copy that MAC address and overwrite the BUTTON_MAC variable in views.py
6. At this point, the Django app will now be listening on the network for that specific button to fire, which in turn will call the Lambda function that the button has been bound to using the form at localhost:8000
