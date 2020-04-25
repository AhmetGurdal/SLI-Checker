# SLI-Checker
Spam Link Injection Attack website checker
```
python SLISearcher.py -h
usage: SLISearcher.py [-h] [-u  | -U ] [-a | -g | -i | -ig] [-s  | -S ] [-r]
                      [-l] [-o]

Description: Check for the Spam Link Injection. Only most popular mechanisms
are added. You can edit the settings. Json file to add or delete mechanisms
Ex: python SLISearcher.py -u https://www.google.com -r -l 2 -o output.txt

optional arguments:
  -h, --help       show this help message and exit
  -u , --url       Url to check
  -U , --urlfile   sum the integers (Default: find the max)
  -a, --all        Show all secure and insecure links
  -g, --group      Group by services
  -i, --insecure   Show just insecure links
  -ig, --igroup    (Default Choose) - Show just insecure links grouped by
                   services
  -s , --slink     Secure link
  -S , --sfile     Secure links file
  -r, --recursive  Active recursive search
  -l , --limit     Limit resurive search deep (Default: infinite)
  -o , --output    Output result into a file.
  ```
  Example:
  Recursive limited by 2 sub links.
  ```
  python SLISearcher.py -u https://this-page-intentionally-left-blank.org/ -r -l 2
  ```
