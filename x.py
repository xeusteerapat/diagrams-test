from diagrams import Cluster, Diagram
from diagrams.aws.compute import EKS
from diagrams.aws.database import ElastiCache, Aurora, DMS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53
from diagrams.onprem.client import Users
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import Cognito
from diagrams.aws.security import IAM
from diagrams.aws.security import DS
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.analytics import ElasticsearchService

with Diagram("Clustered Web Services", show=False):
    dns = Route53("dns")
    load_balancer = ELB("Load Balancer")

    with Cluster("AWS"):
        svc_group = [EKS("web1"),
                     EKS("web2"),
                     EKS("web3")]
        
    with Cluster("On Prem"):
        on_prem_group = [EKS("web1"),
                     EKS("web2"),
                     EKS("web3")]

    with Cluster("DB Cluster"):
        db_primary = Aurora("userdb")
        db_primary - [Aurora("userdb ro")]
        db_migration_svc = DMS("Migration Service")

    with Cluster("Users"):
        users_group = [Users("Sellers"),
                     Users("Buyers"),
                     Users("Bankers")]

    cdn = CloudFront("Amazon CloudFront")
    memcached = ElastiCache("memcached")
    performance = Cloudwatch("AWS CloudWatch")
    static_content = S3("Amazon S3 for Static content")

    security = Cognito("Amazon Cognito")
    authentication = IAM("AWS IAM")
    directory_service = DS("Active Directory Services")

    elasticsearch = ElasticsearchService("Search")

    users_group >> dns
    cdn >> static_content
    dns >> cdn >> load_balancer >> svc_group
    load_balancer >> on_prem_group
    svc_group >> db_primary
    svc_group >> memcached
    memcached >> db_primary
    svc_group >> performance

    users_group >> security
    users_group >> authentication
    users_group >> directory_service

    db_primary >> db_migration_svc
    db_migration_svc >> elasticsearch
    
    svc_group >> elasticsearch