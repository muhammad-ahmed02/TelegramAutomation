# Run the Automation

First take the pull of Selenium standalone chrome image
``` bash
docker pull selenium/standalone-chrome
```

With the following image you can run the Selenium Grid
``` bash
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
```

 Now you can run your selenium scripts in selenium grid!
```
python app/main.py
```
