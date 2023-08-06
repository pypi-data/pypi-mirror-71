# confyaml
Python package to deal with configuration files in YAML

# Usage

```python
from confyaml import Config

# Assumes you have a file called config.yaml
config = Config()
# But you can also pass the path of other yaml file
other_config = Config("other_config.yaml")

# Parameters can be accessed in three different ways:
print(config.a)
print(config["a"])
print(config.get("a"))
# If the parameter does not exist, AttributeError will be raised

# Parameters can be set in three different ways:
config.a = "b"
config.set("a", "c")
config["a"] = "e"

# You can save your changes to the yaml file
# If you pass an extra argument, it will save the yaml file on that path
config.save("new_config.yaml")
```

# Tests

Unittests available on the "test" folder. You can run them using this:

```bash
 python -m unittest tests.test1.GetSetSaveTest
 python -m unittest tests.test1.SanityTest
```

# References
[This Stack Overflow answer](https://stackoverflow.com/a/60227528/3363527) helped me to figure
out how to transform the YAML file into a object accessible with dot (.) operator

[This blog post](http://byatool.com/uncategorized/simple-property-merge-for-python-objects/) helped me on merging the yaml file
with the Config object
