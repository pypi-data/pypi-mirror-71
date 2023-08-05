# pfp_lgbt.py

![Master](https://github.com/Weilbyte/pfp_lgbt.py/workflows/CI/badge.svg?branch=master) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/d0da4cffcb744674a69fbcee8253796d)](https://www.codacy.com/manual/Weilbyte/pfp_lgbt.py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Weilbyte/pfp_lgbt.py&amp;utm_campaign=Badge_Grade)

Python API Wrapper for https://pfp.lgbt/ 

Respects rate limits.

### Installing

To install the library you can run te following command
```py
python3 -m pip install pfp_lgbt.py
```

### Documentation
You can find the documentation on this repo's wiki.

### Examples
List the names of all available flags. 
```py
import pfp_lgbt

client = pfp_lgbt.Client() 

flags = client.flags() 
for flag in flags:
  print(flag.name)
```

Create a static image from URL, and manually save the bytes as file
```py
import pfp_lgbt 

client = pfp_lgbt.Client() 

flag = pfp_lgbt.Flag(name='nb') # Non-binary flag

# `Result` becomes bytes of result image
result = client.imageStatic('https://i.imgur.com/Ypw5pca.png', 'square', 'solid', flag)

with open('result.png', 'wb') as resfile:
  resfile.write(result)
```

Create animated image from URL, and save it to output file
```py 
import pfp_lgbt 

client = pfp_lgbt.Client() 

flag = pfp_lgbt.Flag(name='nb') # Non-binary flag

_ = client.imageAnimated('https://i.imgur.com/Ypw5pca.png', 'square', flag, output_file='output.gif')
```

