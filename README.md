# Script to do dns resolution and saves to excel: dns2excel.py

## Introduction
This tool receives a list of hosts from a text file and its output is a Excel file ready for analysis.

## Prerequisites
In order to run this program you will need this install in your computer:

1. Python 2.7

1. pip
   ```bash
   $ sudo easy_install pip
   ```

1. Python modules: dnsknife, collections, pandas, openpyxl
   ```bash
   $ pip install --user dnsknife
   $ pip install --user collections
   $ pip install --user pandas
   $ pip install --user openpyxl
   ```

## How to use it

1. Create a text file with a list of hosts, one by line, for example: `hostsfile.txt`.
   File contents:
   ```bash
   $ cat hostslist.txt 
   about.intuit.com
   academy.intuit.com
   enterprisesuite.intuit.com
   epp.ie.intuit.com
   healthcare.intuit.com
   ires.intuit.com
   lacerte.intuit.com
   m.intuit.com
   mycorporation.intuit.com
   paytrust.intuit.com
   ```

1. Execute the script as:
   ```bash
   $ ./dns2excel.py -i hostsfile.txt -o hostsfile.xlsx
   ```
1. Wait until the process complete.

   The result is:
   ```bash
   $ dns2excel.py -i hostslist.txt -o hostslist.xlsx
   ---------- DNS Resolution start ----------
   HOST: about.intuit.com - [A]{The DNS has responded}
   HOST: about.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: about.intuit.com. IN AAAA}
   HOST: academy.intuit.com - [A]{The DNS has responded}
   HOST: academy.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: academy.intuit.com. IN AAAA}
   HOST: enterprisesuite.intuit.com - [A]{The DNS has responded}
   HOST: enterprisesuite.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: enterprisesuite.intuit.com. IN AAAA}
   HOST: epp.ie.intuit.com - [A]{NXDOMAIN}
   HOST: epp.ie.intuit.com - [AAAA]{NXDOMAIN}
   HOST: healthcare.intuit.com - [A]{The DNS has responded}
   HOST: healthcare.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: healthcare.intuit.com. IN AAAA}
   HOST: ires.intuit.com - [A]{The DNS response does not contain an answer to the question: ires.intuit.com. IN A}
   HOST: ires.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: ires.intuit.com. IN AAAA}
   HOST: lacerte.intuit.com - [A]{The DNS has responded}
   HOST: lacerte.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: lacerte.intuit.com. IN AAAA}
   HOST: m.intuit.com - [A]{NXDOMAIN}
   HOST: m.intuit.com - [AAAA]{NXDOMAIN}
   HOST: mycorporation.intuit.com - [A]{The DNS has responded}
   HOST: mycorporation.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: mycorporation.intuit.com. IN AAAA}
   HOST: paytrust.intuit.com - [A]{The DNS has responded}
   HOST: paytrust.intuit.com - [AAAA]{The DNS response does not contain an answer to the question: paytrust.intuit.com. IN AAAA}
   ---------- Excel export start ----------
   ---------- Process end ----------
   ```

   List result:
   ```bash
   $ ls
   hostslist.txt   hostslist.xlsx
   ```

1. Open the Excel file: `hostsfile.txt`.
   Result Excel File:
   ![Excel screenshot][excel_img]   


## Additional options for the script
You can select from several options as shown below:
```bash
$ dns2excel.py --help
usage: dns2excel.py [-h] --in hosts_list_file_name --out excel_file_name
                    [--dnsserver ip|host] [--records rec1[,rec2,...]]
                    [--timeout seconds]

Creates an Excel file with a DNS resolutions over a list of hostnames readed
from a text file.

optional arguments:
  -h, --help            show this help message and exit
  --in hosts_list_file_name, -i hosts_list_file_name
                        This files contains the hosts to be resolved, one host
                        per line.
  --out excel_file_name, -o excel_file_name
                        This is the result xlsx file.
  --dnsserver ip|host, -d ip|host
                        Set a custom dns server to be used in the resolution.
  --records rec1[,rec2,...], -r rec1[,rec2,...]
                        Records to be queried to DNS server (default A,AAAA).
  --timeout seconds, -t seconds
                        Number of seconds to wait for a DNS response (default 5s).
```


## GIT

This link contains the source code and demo files:
<https://git.source.akamai.com/users/ralpizar/repos/dnstable>


[excel_img]: https://git.source.akamai.com/users/ralpizar/repos/dnstable/browse/help/excel_img.png
