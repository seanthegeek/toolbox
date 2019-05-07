#!/usr/bin/env python3

"""Tests HTTPS certificates"""

import ssl
import csv
from argparse import ArgumentParser

import requests
import M2Crypto

__version__ = "1.0.0"


def get_cert(hostname, port=443):
    conn = ssl.create_connection((hostname, port))
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sock = context.wrap_socket(conn, server_hostname=hostname)
    certificate_str = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
    x509 = M2Crypto.X509.load_cert_string(certificate_str)

    return dict(issuer=x509.get_issuer().as_text(), subject=x509.get_subject().as_text(),
                not_valid_before=x509.get_not_before().get_datetime().isoformat(),
                not_valid_after=x509.get_not_after().get_datetime().isoformat(),
                fingerprint=x509.get_fingerprint(),
                cert=certificate_str)


def test_https(url):
    url = url.split("://")[-1].split("/")[0]
    port = 443
    url_parts = url.split(";")
    hostname = url_parts[0].lower()
    if len(url_parts) > 1:
        port = int(url_parts[1])
    url = "https://{0}".format(url)
    try:
        requests.get(url)
        return hostname, True, "", get_cert(hostname, port)
    except requests.exceptions.SSLError as e:
        try:
            return hostname, False, e.__str__(), get_cert(hostname, port)
        except Exception as e:
            return hostname, False, e.__str__(), None
    except Exception as e:
        return hostname, False, e.__str__(), None


def _main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="a path to a file containing a list of domains or URLs")
    parser.add_argument("output_file", help="the path of the output CSV file")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    args = parser.parse_args()
    with open(args.input_file) as input_file:
        with open(args.output_file, "w", newline="\n", encoding="utf-8") as output_file:
            fields = ["domain", "valid_cert", "error_message", "issuer", "subject",
                      "not_valid_before", "not_valid_after", "fingerprint"]
            writer = csv.DictWriter(output_file, fieldnames=fields)
            writer.writeheader()
            for line in input_file:
                line = line.strip()
                domain, valid_cert, error_message, cert = test_https(line)
                if cert is not None:
                    writer.writerow(dict(domain=domain, valid_cert=valid_cert, error_message=error_message,
                                         issuer=cert["issuer"], subject=cert["subject"],
                                         not_valid_before=cert["not_valid_before"],
                                         not_valid_after=cert["not_valid_after"],
                                         fingerprint=cert["fingerprint"]))
                else:
                    writer.writerow(dict(domain=domain, valid_cert=valid_cert, error_message=error_message))


if __name__ == "__main__":
    _main()
