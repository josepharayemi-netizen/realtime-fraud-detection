# AWS production mapping

Use Amazon MSK or Kinesis for transaction events, ECS Fargate for the scoring API and consumer, S3 for versioned model artifacts, DynamoDB for idempotent decisions, CloudWatch for metrics, and Secrets Manager for credentials. Deploy private subnets, encryption, least-privilege IAM, and VPC endpoints in production.
