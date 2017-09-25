#!/usr/bin/python
'''
Program to do a DNS resolution over a list of host stored in a text file
and the results are saved into an Excel File.

Usage: dns2excel.py -i hostsfile.txt -o dns_results.xlsx

Author: Rafael Alpizar L

Modules required: dnsknife, collections, pandas, openpyxl

Notes: DNS flags info in https://www.ietf.org/rfc/rfc1035

Version: 1.0

Change log:
2017-09-24 - First version
'''

try:
    from dnsknife.resolver import Resolver, system_resolver
    from dns import flags, opcode, rcode, rdataclass, rdatatype
    from datetime import datetime
    from collections import OrderedDict
    import argparse
    import pandas as pd
except Exception as e:
    print('\nPython module missing [ %s ]\n' % e.message)
    exit(1)

class ExcelFileError(Exception):
    pass


class DNSRecords():
    """Handle a list of DNS records to resolve
    This class have a default DNS records list and can be set
    from a list object o str object (comma separated)
    """
    _dns_records = None
    _DNS_RECORDS_DEFAULT = ['A', 'AAAA']

    def __init__(self, records=None):
        """Init DNS records list
        Keywords:
        records -- list or str
        """
        self._dns_records = self._DNS_RECORDS_DEFAULT

    def set_dns_records(self, records):
        """
        Keyword Arguments:
        records -- list or str

        Returns:
        int -- 0
        """
        if isinstance(records, str):
            self._dns_records = records.upper().split(',')
        elif isinstance(records, list):
            self._dns_records = records
        else:
            raise TypeError('DNS records must be a list type')

    def get_dns_records(self):
        """Return DNS records as list object
        Returns:
        list
        """
        return self._dns_records

    def __str__(self):
        """String Representation
        Returns:
        str
        """
        return ','.join(self.get_dns_records())

    def to_text(self):
        """String Representation
        """
        return self.__str__()


class DNSToExcel():

    _DNS_TIMEOUT_SECONDS = 5
    # used in case no DNSRecords class passed a parameter
    _DNS_RECORDS_RESOLVE = ['A', 'AAAA']
    _hosts_list = None
    _excel_file_name = None
    _dns_server = None
    _set_dns_server_custom = False
    _dns_table = list()
    _dns_records = list()

    def __init__(self, hosts_list,
                 excel_file_name, dns_server=None, dns_records=None):
        """Basic information for the class
        Ketword Argumnts:
        hosts_list      -- list
        excel_file_name -- str
        dns_server_ip   -- str
        dns_records     -- DNSRecords
        """
        self._set_hosts_list(hosts_list)
        self._set_excel_file_name(excel_file_name)
        self._set_dns_server(dns_server)
        if isinstance(dns_records, DNSRecords):
            self._dns_records = dns_records.get_dns_records()
        else:
            self._dns_records = self._DNS_RECORDS_RESOLVE

    def _set_hosts_list(self, hosts_list):
        """Sets the Hosts list verify type
        Keyword Arguments:
        hosts_list -- list

        Returns:
        int -- always 0
        """
        if not isinstance(hosts_list, list):
            raise TypeError(
                'Hosts list error, must be a list() instance')
        self._hosts_list = hosts_list

    def _set_excel_file_name(self, excel_file_name):
        """Sets the Excel File Name
        Keyword Arguments:
        excel_file_name -- str

        Returns:
        int -- always 0
        """
        if excel_file_name[-4:] != 'xlsx':
            raise ExcelFileError(
                'Excel file name extension error, it must end with "xlsx"')
        self._excel_file_name = excel_file_name
        return 0

    def _set_dns_server(self, dns_server_custom):
        """Sets the DNS Server
        Keyword Arguments:
        dns_server_ip -- str

        Returns:
        int -- always 0
        """
        # TODO: Handle IP format and raise exception is not valid
        if dns_server_custom is not None:
            self._set_dns_server_custom = True
            self._dns_server = dns_server_custom
        else:
            # self._dns_server = 'default'
            self._dns_server = ', '.join(system_resolver.nameservers)
        return 0
    
    def _message_to_dict(self, dns_message):
        """Return the DNS answer as a dictionaty
        Keyword Arguments:
        dns_message -- dns.Message.message object

        Returns:
        OrderedDict
        """
        try:
            # flags encoded variable
            fl = rcode.from_flags(dns_message.flags, dns_message.ednsflags)
            # general DNS response information
            dns_id = dns_message.id
            dns_opcode = opcode.to_text(opcode.from_flags(dns_message.flags))
            dns_rcode = rcode.to_text(fl)
            dns_flags = flags.to_text(dns_message.flags)
            dns_edns = dns_message.edns
            dns_eflags = flags.edns_to_text(dns_message.ednsflags)
            dns_payload = dns_message.payload
            # DNS answer section
            dns_answer = OrderedDict()
            # initial dns records counter
            record_counter = dict.fromkeys(self._dns_records, 0)
            record_counter['CNAME'] = 0
            for i in dns_message.answer:
                answer_type = rdatatype.to_text(i.rdtype)
                answer_class = rdataclass.to_text(i.rdclass)
                answer_ttl = i.ttl
                answer_value = list()
                for rd in i:
                    answer_value.append(rd.to_text())
                if answer_type not in record_counter:
                    record_counter[answer_type] = 1
                else:
                    record_counter[answer_type] += 1
                c = record_counter[answer_type]
                answer_type_name = "%s-%d" % (answer_type, c)
                answer_class_name = "%s-class%d" % (answer_type, c)
                answer_ttl_name = "%s-ttl%d" % (answer_type, c)
                dns_answer[answer_type_name] = '; '.join(answer_value)
                dns_answer[answer_class_name] = answer_class
                dns_answer[answer_ttl_name] = answer_ttl
            # building a complete dns response dictionaty
            dns_resp = OrderedDict()
            dns_resp['id'] = dns_id
            dns_resp['opcode'] = dns_opcode
            dns_resp['rcode'] = dns_rcode
            dns_resp['flags'] = dns_flags
            dns_resp['edns'] = dns_edns
            dns_resp['eflags'] = dns_eflags
            dns_resp['payload'] = dns_payload
            # adding answer
            dns_resp.update(dns_answer)
            # adding count of records added
            for record, count in record_counter.items():
                dns_resp[record+' records'] = count
        except:
             # print "Problem in _message_to_dict"
            raise

        return dns_resp

    def _dns_host_resolution(self, hostname, record='A', dns_server_ip=None):
        """Resolve one host and return as dictionaty

        Keyword Arguments:
        hostname -- str
        record   -- str (default 'A')
        dns_server_ip   -- str (default None)

        Return:
        OrderedDict
        """
        dns_response = OrderedDict()
        try:
            r = Resolver(timeout=self._DNS_TIMEOUT_SECONDS)
            if self._set_dns_server_custom:
                dns_query = r.query_at(hostname, record, self._dns_server)
            else:
                dns_query = r.query(hostname, record)
            q = dns_query.get()
            dns_response = self._message_to_dict(q.response)
        except:
            raise
        return dns_response

    def dns_process(self):
        """Do DNS resolution over entire hosts list

        Return:
        list of OrderedDict
        """
        try:
            for host in self._hosts_list:
                # print(host)
                for record in self._dns_records:
                    # print record
                    host_row = OrderedDict()
                    host_row['datetime'] = datetime.today()
                    host_row['dns_server'] = self._dns_server
                    host_row['hostname'] = host
                    host_row['status'] = ''
                    host_row['record'] = record
                    try:
                        res = self._dns_host_resolution(host, record)
                        host_row.update(res)
                        self._dns_table.append(host_row)
                        host_row['status'] = 'The DNS has responded'
                    except Exception as e:
                        # print('Problem at process' + e.message)
                        host_row['status'] = e.message
                        self._dns_table.append(host_row)
                    print('HOST: %s - [%s]{%s}' % (host_row['hostname'],
                                                   host_row['record'],
                                                   host_row['status']))
        except:
            raise
        return 0

    def to_excel(self):
        pd.DataFrame(data=self._dns_table).to_excel(
            self._excel_file_name, sheet_name='DNS Resolution')
        return 0


def main(hosts_file, excel_file_name, dns_server=None, dns_records=None):
    """Run the program

    Keyword Arguments:
    hosts_list      -- list
    excel_file_name -- str
    dns_server_ip   -- str (Default: None)

    Returns
    int = 0
    """
    hosts_list = hosts_file.read().splitlines()
    d = DNSToExcel(hosts_list, excel_file_name, dns_server=dns_server,
                   dns_records=dns_records)
    print('---------- DNS Resolution start ----------')
    d.dns_process()
    print('---------- Excel export start ----------')
    d.to_excel()
    print('---------- Process end ----------')



if __name__ == '__main__':
    try:
        # start the default DNSRecords
        dns_records = DNSRecords()
        # Parameters
        cmd_param = argparse.ArgumentParser(
            description='''
            Creates an Excel file with a DNS resolutions
            over a list of hostnames readed from a text file.''')
        cmd_param.add_argument('--in', '-i', dest='inputfile',
                               metavar='hosts_list_file_name',
                               type=file, required=True,
                               help='This files contains the hosts to be resolved, one host per line.')

        cmd_param.add_argument('--out', '-o', dest='xlsxfile',
                               metavar='excel_file_name', type=str,
                               required=True,
                               help='This is the result xlsx file.')

        cmd_param.add_argument('--dnsserver', '-d', dest='dnsserver',
                               metavar='ip|host', type=str,
                               required=False, default=None,
                               help='Set a custom dns server to be used in the resolution.')

        cmd_param.add_argument('--recods', '-r', dest='records',
                               metavar='rec1[,rec2,...]', type=str,
                               required=False, default=None,
                               help='Records to be queried to DNS server (default %s).' % dns_records.to_text())

        param = cmd_param.parse_args()
        hosts_file = param.inputfile
        excel_file = param.xlsxfile
        dns_server = param.dnsserver
        records_str = param.records
        if records_str is not None:
            dns_records.set_dns_records(records_str)

        print records_str
        print dns_records
        main(hosts_file, excel_file,
             dns_server=dns_server,
             dns_records=dns_records)
        hosts_file.close()
    except IOError as e:
        print(e)
    # except Exception as e:
    #     print(e.message)
    except:
        raise
