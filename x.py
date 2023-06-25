from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import ElastiCache, RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53
from diagrams.onprem.client import Users
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import Cognito
from diagrams.aws.security import IAM
from diagrams.aws.security import DS
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.elastic.elasticsearch import Elasticsearch

with Diagram("Clustered Web Services", show=False):
    dns = Route53("dns")
    load_balancer = ELB("Load Balancer")

    with Cluster("Services"):
        svc_group = [ECS("web1"),
                     ECS("web2"),
                     ECS("web3")]

    with Cluster("DB Cluster"):
        db_primary = RDS("userdb")
        db_primary - [RDS("userdb ro")]

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

    elasticsearch = Elasticsearch("Search")

    users_group >> dns
    cdn >> static_content
    dns >> cdn >> load_balancer >> svc_group
    svc_group >> db_primary
    svc_group >> memcached
    memcached >> db_primary
    svc_group >> performance

    users_group >> security
    users_group >> authentication
    users_group >> directory_service

    elasticsearch >> db_primary
    svc_group >> elasticsearch