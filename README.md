# SLI-Checker
Spam Link Injection Attack website checker

[Protocols](https://books.google.com.tr/books?id=uD7jBwAAQBAJ&pg=PA253&lpg=PA253&dq=https,http,file,ftp,news,nntp,gopher,telnet,cid,mid,afs,prospero,x-exec&source=bl&ots=VmytUNc6nP&sig=ACfU3U16MvRlw8pXigQG95kNtCI0XCzOqw&hl=tr&sa=X&ved=2ahUKEwihj_jFrYvpAhWHxIsKHdbkDzEQ6AEwAnoECAkQAQ#v=onepage&q=https%2Chttp%2Cfile%2Cftp%2Cnews%2Cnntp%2Cgopher%2Ctelnet%2Ccid%2Cmid%2Cafs%2Cprospero%2Cx-exec&f=false)
[Reserved characters](https://tools.ietf.org/html/rfc3986#section-2.2)
You can put the urls you want to search line by line in the file.
However, because of the reserved characters in a url.
The file for the predefined secure links should be in this format:
If you want to define secure links for a domain you already defined as url link or in the url file

Format of the Secure_list.txt file.
```
<Defined url - 1> :: <Secure link or domain - 1> | <Secure link or domain - 2>
<Defined url - 2> :: <Secure link or domain - 1> | <Secure link or domain - 2> | <Secure link or domain - 3>

```

Example Secure_list.txt [File](https://github.com/AhmetGurdal/SLI-Checker/blob/master/Examples/secure_test.txt)
```
http://www.google.com :: https://maps.google.com.tr | https://play.google.com | https://www.youtube.com
```

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
  Examples:
  ```
  python SLISearcher.py -u https://this-page-intentionally-left-blank.org/ -r -l 2
  python SLISearcher.py -U link_file.txt -S secure_links
  
  ```
