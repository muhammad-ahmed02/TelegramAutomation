# Run the Automation

First take the pull of Selenium standalone chrome image
``` bash
docker pull selenium/standalone-chrome
```
Or you can use Selenium standalone firefox image
``` bash
docker pull selenium/standalone-firefox
```

For the Chrome image you can run the Selenium Grid
``` bash
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
```
And for FireFox image you can run it with:
``` bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:latest
```

Now you can run your selenium scripts in selenium grid!
```
python app/main.py
```
