resource "aws_s3_bucket" "this" {
  bucket = "${local.full_project_name}-bucket"
  tags   = merge({ name = "Mynalabs-ASR-S3-Bucket" }, local.tags)
}

resource "aws_s3_bucket_acl" "this" {
  bucket = aws_s3_bucket.this.id
  acl    = "public-read"
}

resource "aws_iam_user" "s3" {
  name = "mynalabs-user"
  tags = merge({ name = "Mynalabs-ASR-S3-User" }, local.tags)
}

resource "aws_iam_user_policy" "s3" {
  name = "mynalabs-asr-s3-policy"
  user = aws_iam_user.s3.name

  policy = <<-EOF
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": "*"
        }
    ]
  }
  EOF
}
