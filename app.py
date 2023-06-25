from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import CloudFront
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.integration import SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import Cognito
from diagrams.aws.security import IAM
from diagrams.aws.database import ElastiCache
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users

with Diagram("Web Application Infrastructure", show=False, direction="LR"):
    with Cluster("AWS Ecosystem"):
        with Cluster("Compute and Scaling"):
            ec2 = EC2("EC2 Instances")
            autoscaling = EC2("Auto Scaling")
            elb = ELB("Elastic Load Balancing")

        with Cluster("Database"):
            rds = RDS("Amazon RDS")
            elasticache = ElastiCache("Amazon ElastiCache")

        storage = S3("Amazon S3")
        cdn = CloudFront("Amazon CloudFront")
        search = ElasticsearchService("Amazon Elasticsearch Service")
        sns = SNS("Amazon SNS")
        caching = CloudFront("Amazon CloudFront")
        performance = Cloudwatch("Amazon CloudWatch")

        security = Cognito("Amazon Cognito")
        authentication = IAM("AWS IAM")

    with Cluster("Users"):
        sellers = Users("Sellers")
        buyers = Users("Buyers")
        bankers = Users("Bankers")

    sellers >> autoscaling >> elb
    buyers >> autoscaling >> elb
    bankers >> autoscaling >> elb
    elb >> ec2
    ec2 >> rds
    ec2 >> elasticache
    ec2 >> storage
    ec2 >> search
    ec2 >> sns
    ec2 << cdn
    ec2 << caching
    ec2 << performance
    sellers >> security
    buyers >> security
    bankers >> security
    sellers >> authentication
    buyers >> authentication
    bankers >> authentication

