from aws_cdk import (
    # Duration,
    Stack, Duration, Tags
    # aws_sqs as sqs,
)
from aws_cdk.aws_ecr_assets import DockerImageAsset
from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr as ecr,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm
)

class {{cookiecutter.project.name|replace(' ', '')|replace('-', '')|replace('_', '')|capitalize}}Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc.from_lookup(self, "{{cookiecutter.deployment.cdk.vpc_name}}",
                                  vpc_id="{{cookiecutter.deployment.cdk.vpc_id}}")
        security_group = ec2.SecurityGroup(self,
                                           "{{cookiecutter.deployment.cdk.security_group_name}}",
                                           vpc=vpc,
                                           security_group_name="{{cookiecutter.deployment.cdk.security_group_name}}",
                                           allow_all_outbound=True,
                                           description="Security Group for ECS Deployment")
        security_group.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(8000),
                                        description="Django Inbound Rule")

        cluster = ecs.Cluster.from_cluster_attributes(self,
                                                      "{{cookiecutter.deployment.cdk.cluster_name}}",
                                                      cluster_name="{{cookiecutter.deployment.cdk.cluster_name}}", vpc=vpc,
                                                      security_groups=[security_group])
        loadbalancer_service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "sakshammittal-fargate",
                                                                                  cluster=cluster,  # Required
                                                                                  cpu={{cookiecutter.deployment.cdk.loadbalancer.cpu}},  # Default is 256
                                                                                  desired_count={{cookiecutter.deployment.cdk.loadbalancer.desired_count}},  # Default is 1
                                                                                  task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                                                      image=ecs.ContainerImage.from_docker_image_asset(
                                                                                          asset=DockerImageAsset(self,
                                                                                                                 id="{{cookiecutter.project.name|replace(' ', '')|replace('-', '')|replace('_', '')|lower}}-image",
                                                                                                                 directory='../')
                                                                                      ),
                                                                                      container_port=8000,
                                                                                      container_name="{{cookiecutter.project.name|replace(' ', '')|replace('-', '')|replace('_', '')|lower}}-container"
                                                                                  ),
                                                                                  memory_limit_mib={{cookiecutter.deployment.cdk.loadbalancer.memory_limit_mib}},
                                                                                  max_healthy_percent={{cookiecutter.deployment.cdk.loadbalancer.max_healthy_percent}},
                                                                                  min_healthy_percent={{cookiecutter.deployment.cdk.loadbalancer.min_healthy_percent}},
                                                                                  # Default is 512
                                                                                  public_load_balancer=True,
                                                                                  certificate=acm.Certificate.from_certificate_arn(
                                                                                      self, "DomainCertificate",
                                                                                      certificate_arn="{{cookiecutter.deployment.cdk.loadbalancer.certificate_arn}}"
                                                                                  )
                                                                                  )
        scalable_target = loadbalancer_service.service.auto_scale_task_count(
            min_capacity={{cookiecutter.deployment.cdk.loadbalancer.auto_scale_task_count.min_capacity}},
            max_capacity={{cookiecutter.deployment.cdk.loadbalancer.auto_scale_task_count.max_capacity}}
        )
        scalable_target.scale_on_cpu_utilization("CpuScaling",
                                                 target_utilization_percent={{cookiecutter.deployment.cdk.loadbalancer.target_cpu_utilization_percent}}
                                                 )

        scalable_target.scale_on_memory_utilization("MemoryScaling",
                                                    target_utilization_percent={{cookiecutter.deployment.cdk.loadbalancer.target_memory_utilization_percent}}
                                                    )
        loadbalancer_service.target_group.configure_health_check(
            enabled=True,
            healthy_threshold_count={{cookiecutter.deployment.cdk.loadbalancer.health_check.healthy_threshold_count}},
            path='/',
            interval=Duration.seconds({{cookiecutter.deployment.cdk.loadbalancer.health_check.interval_secs}}),
            timeout=Duration.seconds({{cookiecutter.deployment.cdk.loadbalancer.health_check.timeout_secs}})
        )

        route53.ARecord(self, "AliasRecord",
                        record_name='{{cookiecutter.deployment.cdk.domain_record.record_name}}',
                        zone=route53.HostedZone.from_lookup(
                            self,
                            "HostedZone",
                            domain_name="{{cookiecutter.deployment.cdk.domain_record.domain_name}}"
                        ),
                        ttl=Duration.minutes({{cookiecutter.deployment.cdk.domain_record.ttl_minutes}}),
                        target=route53.RecordTarget.from_alias(
                            targets.LoadBalancerTarget(loadbalancer_service.load_balancer)),
                        )

        Tags.of(self).add("Owner", "{{cookiecutter.project.owner}}")
        Tags.of(self).add("AD", "sakshammittal")
        Tags.of(self).add("Email", "{{cookiecutter.project.contact_email}}")
        Tags.of(self).add("Quarter", "TU-22")
        Tags.of(self).add("Project", "{{cookiecutter.project.name}}")
