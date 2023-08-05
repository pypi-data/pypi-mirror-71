import boto3
import uuid
from navio.aws._common import dump
from navio.aws.services._session import AWSSession


class AWSACM(AWSSession):

    def __init__(self, **kwargs):
        super(
            self.__class__,
            self
        ).__init__(kwargs['profile_name'], kwargs.get('region_name', None))

    def find_cert_arn(self, **kwargs):
        cert_arn = None

        if 'domain_name' not in kwargs:
            raise Exception('Argument missing: domain_name')

        client = self.client('acm')

        cache_key = 'acm.certificates.{}.{}.{}'.format(
            self.region_name,
            self.profile_name,
            'ISSUED'
        )

        certificates_list = self.cache(cache_key)
        if certificates_list is None:
            certificates_list = list()

            paginator = client.get_paginator('list_certificates')
            page_iterator = paginator.paginate(CertificateStatuses=['ISSUED'])
            for page in page_iterator:
                if 'CertificateSummaryList' in page:
                    for cert in page['CertificateSummaryList']:
                        certificates_list.append(cert)

            self.cache(cache_key, certificates_list)

        for cert in certificates_list:
            cert_details = client.describe_certificate(CertificateArn=cert['CertificateArn'])
            for san in cert_details['Certificate']['SubjectAlternativeNames']:
                if san == kwargs['domain_name']:
                    if cert_arn is not None:
                        raise Exception(
                            'Multiple certificates with same domain name. ({}, {})'.format(
                                cert_arn, cert['CertificateArn']))
                    else:
                        cert_arn = cert['CertificateArn']
        return cert_arn

    def request_via_dns(self, **kwargs):
        if 'domain_name' not in kwargs:
            raise Exception('Argument missing: domain_name')

        if 'alternative_names' not in kwargs:
            raise Exception('Argument missing: alternative_names')

        client = self.client('acm')

        resp = client.request_certificate(
            DomainName=kwargs.get('domain_name'),
            SubjectAlternativeNames=kwargs.get('alternative_names'),
            ValidationMethod='DNS',
            IdempotencyToken=uuid.uuid4()
        )

        return resp

    def get_dns_validation_options(self, **kwargs):
        if 'certificate_arn' not in kwargs:
            raise Exception('Argument missing: certificate_arn')

        client = self.client('acm')

        resp = client.describe_certificate(
            CertificateArn=certificate_arn
        )

        return resp['Certificate']['DomainValidationOptions'][0]['ResourceRecord']
