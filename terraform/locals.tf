locals {

  private_subnets = [
    for subnet in data.aws_subnet.details : subnet.id
    if can(regex("(?i)private", lookup(subnet.tags, "Name", "")))
  ]
}