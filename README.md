# Script to do DNS resolution and it saves output to Excel format

## Introduction
This tool receives a list of hosts from a text file and its output is a Excel file ready for analysis.

## Prerequisites
In order to run this program you will need this install in your computer:

1. Python 3.6

1. pip
   ```bash
   Install pip (depends on your OS/distro)
   ```

1. Python modules: dnsknife, collections, pandas, openpyxl
   ```bash
   $ python 3 -m pip install --user collections
   $ python 3 -m pip install --user pandas
   $ python 3 -m pip install --user openpyxl
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

   The script output is:
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

   List file result:
   ```bash
   $ ls
   hostslist.txt   hostslist.xlsx
   ```

1. Open the Excel file: `hostsfile.xlsx`.

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

## Info about DNS flags (from RFC 1035, section 4.1.1)

The header contains the following fields:
```
                                    1  1  1  1  1  1
      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                      ID                       |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    QDCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ANCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    NSCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    |                    ARCOUNT                    |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

Some flags:
```
QR              A one bit field that specifies whether this message is a
                query (0), or a response (1).
				
AA              Authoritative Answer - this bit is valid in responses,
                and specifies that the responding name server is an
                authority for the domain name in question section.

                Note that the contents of the answer section may have
                multiple owner names because of aliases.  The AA bit
                corresponds to the name which matches the query name, or
                the first owner name in the answer section.

RD              Recursion Desired - this bit may be set in a query and
                is copied into the response.  If RD is set, it directs
                the name server to pursue the query recursively.
                Recursive query support is optional.

RA              Recursion Available - this be is set or cleared in a
                response, and denotes whether recursive query support is
                available in the name server.
```


[excel_img]: help/excel_img.png

