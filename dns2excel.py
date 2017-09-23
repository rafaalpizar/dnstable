#!/usr/bin/python

'''
Program to do a DNS resolution over a list of host
reading from a text file and export the results into
a Excel File

Usage: dns2excel.py -i hostsfile.txt -o dns_results.xlsx

Author: Rafael Alpizar L

Change log:
2017-09-22 - First version
'''

from dnsknife.resolver import Resolver
from dns import flags, opcode, rcode, rdataclass, rdatatype
from dns.resolver import NoAnswer
import collections

class DNSToExcel():

    _DNS_TIMEOUT_SECONDS = 15
    _hosts_list = ''
    _excel_file_name = ''

    def __init__(self, hosts_list, excel_file_name):
        """Basic information for the class
        """

        self._hosts_list = hosts_list
        self._excel_file_name = excel_file_name

    def _message_to_dict(self, dns_message):
        """Return the DNS answer as a dictionaty
        Keyword Arguments:
        dns_message -- dns.Message.message object

        Returns:
        dict
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
            dns_answer = collections.OrderedDict()
            record_counter = collections.OrderedDict()
            for i in dns_message.answer:                
                answer_type = rdatatype.to_text(i.rdtype)
                answer_class = rdataclass.to_text(i.rdclass)
                answer_ttl = i.ttl
                print answer_ttl
                answer_value = list()
                for rd in i:
                    answer_value.append(rd.to_text())

                if answer_type not in record_counter:
                    record_counter.update({answer_type: 1})
                else:
                    record_counter[answer_type] += 1
                answer_type_name = "%s-%d" % (answer_type, record_counter[answer_type])
                answer_class_name = "%s-class%d" % (answer_type, record_counter[answer_type])
                answer_ttl_name = "%s-ttl%d" % (answer_type, record_counter[answer_type])
                dns_answer[answer_type_name] = '; '.join(answer_value)
                dns_answer[answer_class_name] = answer_class
                dns_answer[answer_ttl_name] = answer_ttl

            # building a complete dns response dictionaty
            dns_resp = collections.OrderedDict()
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
                dns_resp.update({"%s records" % record: count})

#            dns_resp.update(record_counter)
        except:
            print "Problem in _message_to_dict"
            raise

        return dns_resp

    def _dns_resolver(self, hostname, record='A', dns_server_ip=None):
        """Resolve one host and return as dictionaty

        Keyword Arguments:
        hostname -- str
        record   -- str (default 'A')
        dns_server_ip   -- str (default None)

        Return:
        dict
        """
        try:
            r = Resolver(timeout=self._DNS_TIMEOUT_SECONDS)
            if dns_server_ip is None:
                dns_query = r.query(hostname, record)
            else:
                dns_query = r.query_at(hostname, record, dns_server_ip)
            q = dns_query.get()
            dns_response = self._message_to_dict(q.response)
            print dns_response
        except NoAnswer as e:
            print "Problem at _dns_resolver: No DNS records"
            raise
        except Exception as e:
            print "Problem at _dns_resolver"
            print e
            raise
        return 0



def main(hosts_list, excel_file_name):
    """Run the program

    Keyword Arguments:
    hosts_list      -- file 
    excel_file_name -- str

    Returns
    int = 0
    """
    d = DNSToExcel(hosts_list, excel_file_name)
    d._dns_resolver('www.nike.com')
    

if __name__ == '__main__':
    hosts_list = open('list.txt', 'r')
    main(hosts_list, 'somefile.xlsx')
    hosts_list.close()
         
