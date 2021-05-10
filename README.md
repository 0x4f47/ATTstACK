# ATTstACK

Quick scripts for manipulating the MITRE ATT&CK Navigator layers

## Getting Started

All you need to do to get started is download/clone the scripts and run them against the downloaded Navigator layers to be combined.

### Prerequisites

In order to run this script you will need to have Python 3 and the following four modules:

```
import json
import glob
import os
import re
```

### Running the Combinator

In order to combine the layers, first you need to download them from https://attack.mitre.org/groups/ -- visit the above link, open each of the groups that you're interested in combining, and download their respective layers by clicking on the "MITRE ATT&CK Navigator Layer" --> "download" button on the top-right of the page.

Place all the downloaded layers into an appropriately named sub-folder in the same folder as the script.

Then, simply execute the script with Python and, as prompted, provide the name of the layer-containing subfolder, the output name, and description.

The resulting combined layer will be saved in the same folder as the script as "Name.json" (where the name is the one you provided when prompted).

## Contributing

This script is not a labour of love, I welcome all and any contributions to help improve it.

## Authors

* **Oleksiy Gayda** - *Initial work* - [ATTstACK](https://github.com/0x4f47/ATTstACK)

See also the list of [contributors](https://github.com/0x4f47/ATTstACK/contributors) who participated in this project.

## License

This project is licensed under the Apache-2.0 License

## Acknowledgments

* Undying gratitude to the MITRE team for making ATT&CK available to all of us