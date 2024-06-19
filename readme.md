# Run the Automation

First take the pull of Selenium standalone firefox image

```bash
docker pull selenium/standalone-firefox
```

For the Firefox image you can run the Selenium Grid

```bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:latest
```

Now you can run your selenium scripts in selenium grid!

```
python app/main.py
```
