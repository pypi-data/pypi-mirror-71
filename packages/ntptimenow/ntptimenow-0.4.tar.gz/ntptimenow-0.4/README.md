# ntptimenow
Python NTP time now

## Install

```sh
pip install ntptimenow
```

## Used

```python
from ntptimenow import NTPTimeNow

now = NTPTimeNow().ntp_update() # It's datetime.
```

**API**

```python
NTPTimeNow(poolservers:str='time.kku.ac.th',version:int=3)
```
- poolservers is `NTP Server`. (default is `time.kku.ac.th`)
- version is version of  `NTP Server`. (default is `3`)

```python
ntp_now()
```

return datetime.datetime